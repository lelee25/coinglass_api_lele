"""
Price feeds WebSocket — Binance + Bitget pubblici, no auth.

Modulo riutilizzabile per il Claude server. Verificato empiricamente
2026-04-30 (vedi tests/test_bitget_ws.py): entrambi i WS pubblici funzionano,
nessuna chiave richiesta, costo zero.

Pattern di integrazione consigliato:
- Bitget = canonical price per la venue di esecuzione (no mismatch su SL/TP)
- Binance = riferimento secondario per cross-validation o se Bitget non
  quota un asset specifico

API:
    feeds = PriceFeedManager()
    feeds.add_trigger("BTCUSDT", "ABOVE", 78200, on_breakout)
    feeds.add_trigger("BTCUSDT", "BELOW", 76500, on_breakdown)
    asyncio.run(feeds.run_bitget(["BTCUSDT", "ETHUSDT"]))
"""

from __future__ import annotations

import asyncio
import dataclasses
import json
import time
from typing import Any, Awaitable, Callable


BITGET_PUBLIC_WS = "wss://ws.bitget.com/v2/ws/public"
BINANCE_FUTURES_WS = "wss://fstream.binance.com/ws"
BINANCE_SPOT_WS = "wss://stream.binance.com:9443/ws"


@dataclasses.dataclass
class PriceTick:
    venue: str          # "bitget" | "binance"
    symbol: str
    last: float
    bid: float
    ask: float
    ts_exchange: int    # ms epoch dall'exchange
    ts_local: float     # time.time() locale
    funding_rate: float | None = None
    mark_price: float | None = None
    raw: dict | None = None


@dataclasses.dataclass
class Trigger:
    symbol: str
    side: str           # "ABOVE" | "BELOW"
    price: float
    callback: Callable[[PriceTick, "Trigger"], Awaitable[None]]
    triggered: bool = False
    ttl: float | None = None  # epoch dopo cui trigger scade


class PriceFeedManager:
    """Gestisce trigger di prezzo + dispatch su tick ricevuti."""

    def __init__(self) -> None:
        self.last_price: dict[str, PriceTick] = {}  # key = "venue:symbol"
        self.triggers: list[Trigger] = []
        self._on_tick: Callable[[PriceTick], Awaitable[None]] | None = None

    def add_trigger(
        self,
        symbol: str,
        side: str,
        price: float,
        callback: Callable[[PriceTick, Trigger], Awaitable[None]],
        ttl_seconds: float | None = None,
    ) -> Trigger:
        assert side in ("ABOVE", "BELOW"), "side must be ABOVE|BELOW"
        t = Trigger(symbol=symbol, side=side, price=price, callback=callback,
                    ttl=time.time() + ttl_seconds if ttl_seconds else None)
        self.triggers.append(t)
        return t

    def on_tick(self, fn: Callable[[PriceTick], Awaitable[None]]) -> None:
        self._on_tick = fn

    async def _dispatch(self, tick: PriceTick, venue: str) -> None:
        key = f"{venue}:{tick.symbol}"
        prev = self.last_price.get(key)
        self.last_price[key] = tick

        if self._on_tick:
            try:
                await self._on_tick(tick)
            except Exception as e:
                print(f"[on_tick callback error] {e}")

        # Trigger check (only on prev->current crossing)
        if prev is None:
            return
        for trig in list(self.triggers):
            if trig.triggered or trig.symbol != tick.symbol:
                continue
            if trig.ttl and time.time() > trig.ttl:
                trig.triggered = True
                continue

            crossed_up = trig.side == "ABOVE" and prev.last < trig.price <= tick.last
            crossed_down = trig.side == "BELOW" and prev.last > trig.price >= tick.last
            if crossed_up or crossed_down:
                trig.triggered = True
                try:
                    await trig.callback(tick, trig)
                except Exception as e:
                    print(f"[trigger callback error] {e}")

    # ---------- Bitget ----------

    async def run_bitget(self, symbols: list[str], inst_type: str = "USDT-FUTURES") -> None:
        """Stream Bitget per N simboli. Bitget v2 docs:
        https://www.bitget.com/api-doc/common/websocket-intro
        """
        import websockets
        sub = {
            "op": "subscribe",
            "args": [{"instType": inst_type, "channel": "ticker", "instId": s} for s in symbols],
        }
        while True:  # auto-reconnect
            try:
                async with websockets.connect(BITGET_PUBLIC_WS, ping_interval=None) as ws:
                    await ws.send(json.dumps(sub))
                    last_ping = time.time()
                    async for raw in ws:
                        if time.time() - last_ping > 25:
                            await ws.send("ping")
                            last_ping = time.time()
                        if raw == "pong":
                            continue
                        try:
                            msg = json.loads(raw)
                        except Exception:
                            continue
                        if msg.get("event") == "error":
                            print(f"[bitget] error: {msg}")
                            continue
                        if msg.get("action") in ("snapshot", "update") and msg.get("data"):
                            for d in msg["data"]:
                                tick = PriceTick(
                                    venue="bitget",
                                    symbol=d.get("instId", ""),
                                    last=float(d.get("lastPr") or 0),
                                    bid=float(d.get("bidPr") or 0),
                                    ask=float(d.get("askPr") or 0),
                                    ts_exchange=int(d.get("ts") or 0),
                                    ts_local=time.time(),
                                    funding_rate=float(d["fundingRate"]) if d.get("fundingRate") else None,
                                    mark_price=float(d["markPrice"]) if d.get("markPrice") else None,
                                    raw=d,
                                )
                                await self._dispatch(tick, "bitget")
            except Exception as e:
                print(f"[bitget reconnect] {type(e).__name__}: {e}")
                await asyncio.sleep(2.0)

    # ---------- Binance ----------

    async def run_binance(self, symbols: list[str], market: str = "futures") -> None:
        """Stream Binance bookTicker (best bid/ask top-of-book)."""
        import websockets
        base = BINANCE_FUTURES_WS if market == "futures" else BINANCE_SPOT_WS
        streams = "/".join(f"{s.lower()}@bookTicker" for s in symbols)
        url = f"{base}/{streams}" if len(symbols) == 1 else f"{base.replace('/ws','/stream')}?streams={streams}"
        # Per single symbol Binance WS supporta /ws/<stream> direttamente
        if len(symbols) == 1:
            url = f"{base}/{symbols[0].lower()}@bookTicker"

        while True:
            try:
                async with websockets.connect(url, ping_interval=20) as ws:
                    async for raw in ws:
                        msg = json.loads(raw)
                        # Combined stream: {"stream": "...", "data": {...}}
                        data = msg.get("data", msg)
                        sym = (data.get("s") or "").upper()
                        bid = float(data.get("b", 0))
                        ask = float(data.get("a", 0))
                        ts = int(data.get("E") or data.get("T") or int(time.time() * 1000))
                        tick = PriceTick(
                            venue="binance",
                            symbol=sym,
                            last=(bid + ask) / 2,
                            bid=bid, ask=ask,
                            ts_exchange=ts, ts_local=time.time(),
                            raw=data,
                        )
                        await self._dispatch(tick, "binance")
            except Exception as e:
                print(f"[binance reconnect] {type(e).__name__}: {e}")
                await asyncio.sleep(2.0)


# ---------- Quick demo ----------

async def _demo() -> None:
    feeds = PriceFeedManager()

    async def on_trig(tick: PriceTick, trig: Trigger) -> None:
        print(f"🚨 TRIGGER {trig.side} {trig.symbol} @ {trig.price} — current={tick.last} venue={tick.venue}")

    async def log_tick(tick: PriceTick) -> None:
        if int(tick.ts_local) % 5 == 0:  # log ogni ~5s
            print(f"[{tick.venue}] {tick.symbol} last={tick.last:.2f} bid={tick.bid:.2f} ask={tick.ask:.2f}")

    feeds.on_tick(log_tick)

    # Esempio: trigger 1% sopra/sotto il prezzo iniziale
    feeds.add_trigger("BTCUSDT", "ABOVE", 80000.0, on_trig)
    feeds.add_trigger("BTCUSDT", "BELOW", 75000.0, on_trig)

    print("Streaming Bitget BTCUSDT perp + Binance BTCUSDT futures per 30s...")
    try:
        await asyncio.wait_for(
            asyncio.gather(
                feeds.run_bitget(["BTCUSDT"]),
                feeds.run_binance(["BTCUSDT"], market="futures"),
            ),
            timeout=30.0,
        )
    except asyncio.TimeoutError:
        pass
    print(f"Demo terminato. Triggers fired: {sum(1 for t in feeds.triggers if t.triggered)}")


if __name__ == "__main__":
    asyncio.run(_demo())
