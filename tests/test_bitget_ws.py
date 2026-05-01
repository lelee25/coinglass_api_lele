"""
Verifica empirica del Bitget WebSocket pubblico (v2).

Connette al WS pubblico Bitget e riceve ticker BTCUSDT in tempo reale.
Confronta in parallelo col WS Binance per misurare:
- Latenza di ricezione tick
- Spread Bitget ↔ Binance (bps)
- Stabilità della connessione

Bitget WS v2 docs: https://www.bitget.com/api-doc/common/websocket-intro

Uso:
    python3 tests/test_bitget_ws.py [--seconds 30]
"""

from __future__ import annotations

import argparse
import asyncio
import json
import statistics
import sys
import time
from typing import Any


BITGET_PUBLIC_WS = "wss://ws.bitget.com/v2/ws/public"
BINANCE_FUTURES_WS = "wss://fstream.binance.com/ws/btcusdt@bookTicker"


async def bitget_stream(symbol: str, inst_type: str, duration: float, prices: dict):
    """Si connette a Bitget WS pubblico e raccoglie tick BTCUSDT per `duration` secondi."""
    import websockets

    sub = {
        "op": "subscribe",
        "args": [{
            "instType": inst_type,
            "channel": "ticker",
            "instId": symbol,
        }],
    }

    start = time.time()
    msg_count = 0
    last_ping = start
    sample_event = None

    try:
        async with websockets.connect(BITGET_PUBLIC_WS, ping_interval=None) as ws:
            connected_at = time.time()
            print(f"[Bitget] CONNECTED in {(connected_at - start)*1000:.0f} ms")

            await ws.send(json.dumps(sub))
            print(f"[Bitget] sent subscribe: {json.dumps(sub)}")

            while time.time() - start < duration:
                # heartbeat applicativo ogni 30s
                if time.time() - last_ping > 25:
                    await ws.send("ping")
                    last_ping = time.time()

                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=2.0)
                except asyncio.TimeoutError:
                    continue

                if raw == "pong":
                    continue

                try:
                    msg = json.loads(raw)
                except json.JSONDecodeError:
                    print(f"[Bitget] non-json: {raw[:100]}")
                    continue

                # Subscribe ack: {"event":"subscribe","arg":{...}}
                if msg.get("event") == "subscribe":
                    print(f"[Bitget] subscribe ACK ricevuto")
                    continue
                if msg.get("event") == "error":
                    print(f"[Bitget] ERROR: {msg}")
                    return

                # Tick data: {"action":"snapshot|update","arg":{...},"data":[{...}]}
                if msg.get("action") in ("snapshot", "update") and msg.get("data"):
                    tick = msg["data"][0]
                    last = float(tick.get("lastPr") or 0)
                    bid = float(tick.get("bidPr") or 0)
                    ask = float(tick.get("askPr") or 0)
                    ts = int(tick.get("ts") or 0)
                    msg_count += 1
                    if sample_event is None:
                        sample_event = tick
                        print(f"[Bitget] PRIMO TICK: last={last} bid={bid} ask={ask} ts={ts}")
                    prices.setdefault("bitget", []).append({
                        "last": last, "bid": bid, "ask": ask,
                        "ts_exchange": ts, "ts_local": time.time(),
                    })

            print(f"[Bitget] TOTALE: {msg_count} tick ricevuti in {duration:.0f}s "
                  f"({msg_count/duration:.1f} tick/s)")
            if sample_event:
                print(f"[Bitget] schema fields: {sorted(sample_event.keys())}")
    except Exception as e:
        print(f"[Bitget] EXCEPTION: {type(e).__name__}: {e}")


async def binance_stream(duration: float, prices: dict):
    """Stream Binance Futures USDM bookTicker BTCUSDT per confronto."""
    import websockets

    start = time.time()
    msg_count = 0

    try:
        async with websockets.connect(BINANCE_FUTURES_WS, ping_interval=None) as ws:
            print(f"[Binance] CONNECTED in {(time.time()-start)*1000:.0f} ms")
            while time.time() - start < duration:
                try:
                    raw = await asyncio.wait_for(ws.recv(), timeout=2.0)
                except asyncio.TimeoutError:
                    continue
                msg = json.loads(raw)
                bid = float(msg.get("b", 0))
                ask = float(msg.get("a", 0))
                ts = int(msg.get("E") or msg.get("T") or 0)
                msg_count += 1
                prices.setdefault("binance", []).append({
                    "bid": bid, "ask": ask, "mid": (bid + ask) / 2,
                    "ts_exchange": ts, "ts_local": time.time(),
                })
            print(f"[Binance] TOTALE: {msg_count} tick in {duration:.0f}s")
    except Exception as e:
        print(f"[Binance] EXCEPTION: {type(e).__name__}: {e}")


async def main(seconds: float):
    print(f"=== Bitget vs Binance WS comparison — {seconds}s di stream ===\n")
    prices: dict = {}

    await asyncio.gather(
        bitget_stream("BTCUSDT", "USDT-FUTURES", seconds, prices),
        binance_stream(seconds, prices),
    )

    print("\n=== Analisi ===")

    bg = prices.get("bitget", [])
    bn = prices.get("binance", [])

    if not bg:
        print("FAIL: Bitget non ha ricevuto tick — il WebSocket NON funziona o subscribe sbagliato")
        return 2
    if not bn:
        print("WARN: Binance non ha ricevuto tick (probabilmente firewall/network)")

    print(f"Bitget tick rate: {len(bg)/seconds:.1f}/s")
    if bn:
        print(f"Binance tick rate: {len(bn)/seconds:.1f}/s")

    # Last sample
    if bg:
        last_bg = bg[-1]
        bg_mid = (last_bg["bid"] + last_bg["ask"]) / 2
        print(f"\n[Bitget] last tick: bid={last_bg['bid']:.2f} ask={last_bg['ask']:.2f} mid={bg_mid:.2f}")
    if bn:
        last_bn = bn[-1]
        print(f"[Binance] last tick: bid={last_bn['bid']:.2f} ask={last_bn['ask']:.2f} mid={last_bn['mid']:.2f}")

    # Spread Bitget ↔ Binance — pair tick per timestamp
    if bg and bn:
        bg_mid_avg = statistics.mean((p["bid"] + p["ask"]) / 2 for p in bg if p["bid"] > 0)
        bn_mid_avg = statistics.mean(p["mid"] for p in bn if p["mid"] > 0)
        spread_abs = bn_mid_avg - bg_mid_avg
        spread_bps = (spread_abs / bg_mid_avg) * 10000
        print(f"\n[Confronto] Bitget mid avg: ${bg_mid_avg:,.2f}")
        print(f"[Confronto] Binance mid avg: ${bn_mid_avg:,.2f}")
        print(f"[Confronto] Spread Binance - Bitget: ${spread_abs:+,.2f} ({spread_bps:+.2f} bps)")
        print(f"[Confronto] Implicazione: SL/TP su Bitget basati su prezzo Binance "
              f"divergono di ~{abs(spread_bps):.0f} bps, "
              f"= ${abs(spread_abs):.2f} su {bg_mid_avg:.0f}")

    print("\n=== Verdetto WS Bitget pubblico ===")
    if bg and len(bg) > 5:
        print("✅ FUNZIONA — connessione stabile, dati real-time, no auth richiesta, gratis")
    else:
        print("❌ NON FUNZIONA — verificare URL/subscribe/network")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=float, default=20.0, help="durata stream")
    args = parser.parse_args()
    raise SystemExit(asyncio.run(main(args.seconds)))
