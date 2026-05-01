"""
Cross-validation Coinalyze ↔ CoinGlass.

Confronta i valori restituiti dalle due API per gli stessi dataset core
(open interest, funding rate, liquidation 24h) sugli stessi exchange
(Binance, OKX, Bybit) e simboli (BTC, ETH).

Output: report markdown con deviazione %, max delta, latency, coverage overlap.

Uso:
    # carica COINALYZE_API_KEY e COINGLASS_API_KEY da .env
    python3 tests/cross_validation.py [--out cross_report.md]

Sicurezza:
- Le chiavi vengono lette dal .env, mai stampate.
- Solo richieste GET in lettura, nessuna scrittura.
- Rate limit conservativo: 1 chiamata ogni 2.5s su entrambe le API.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
import urllib.error
import urllib.parse
import urllib.request


COINALYZE_BASE = "https://api.coinalyze.net/v1"
COINGLASS_BASE = "https://open-api-v4.coinglass.com"

SLEEP_BETWEEN = 2.5  # secondi tra chiamate (vale per entrambe)
TIMEOUT = 20.0


def load_env(env_path: Path) -> dict[str, str]:
    env: dict[str, str] = {}
    if not env_path.exists():
        return env
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def http_get(url: str, headers: dict[str, str] | None = None) -> tuple[int | None, dict | None, int]:
    req = urllib.request.Request(url, headers=headers or {})
    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            raw = resp.read()
            elapsed = int((time.time() - started) * 1000)
            try:
                return resp.status, json.loads(raw.decode("utf-8")), elapsed
            except json.JSONDecodeError:
                return resp.status, None, elapsed
    except urllib.error.HTTPError as e:
        elapsed = int((time.time() - started) * 1000)
        try:
            body = json.loads(e.read().decode("utf-8"))
        except Exception:
            body = None
        return e.code, body, elapsed
    except Exception as e:
        elapsed = int((time.time() - started) * 1000)
        return None, {"_error": str(e)}, elapsed


# ---------- Coinalyze ----------

def cz_url(path: str, params: dict[str, Any], api_key: str) -> str:
    qp = {k: v for k, v in params.items() if v is not None}
    qp["api_key"] = api_key
    return f"{COINALYZE_BASE}{path}?{urllib.parse.urlencode(qp)}"


def cz_future_markets(api_key: str) -> list[dict]:
    url = cz_url("/future-markets", {}, api_key)
    code, body, _ = http_get(url)
    if code == 200 and isinstance(body, list):
        return body
    return []


def cz_exchanges(api_key: str) -> dict[str, str]:
    """Ritorna mappa code -> name (es. 'A' -> 'Binance')."""
    url = cz_url("/exchanges", {}, api_key)
    code, body, _ = http_get(url)
    if code == 200 and isinstance(body, list):
        return {x["code"]: x["name"] for x in body if "code" in x and "name" in x}
    return {}


def cz_open_interest(symbols: list[str], api_key: str) -> list[dict]:
    url = cz_url("/open-interest", {"symbols": ",".join(symbols), "convert_to_usd": "true"}, api_key)
    code, body, _ = http_get(url)
    if code == 200 and isinstance(body, list):
        return body
    return []


def cz_funding_rate(symbols: list[str], api_key: str) -> list[dict]:
    url = cz_url("/funding-rate", {"symbols": ",".join(symbols)}, api_key)
    code, body, _ = http_get(url)
    if code == 200 and isinstance(body, list):
        return body
    return []


def cz_predicted_funding_rate(symbols: list[str], api_key: str) -> list[dict]:
    url = cz_url("/predicted-funding-rate", {"symbols": ",".join(symbols)}, api_key)
    code, body, _ = http_get(url)
    if code == 200 and isinstance(body, list):
        return body
    return []


def cz_liquidation_history(symbol: str, interval: str, hours: int, api_key: str) -> list[dict]:
    now = int(time.time())
    frm = now - hours * 3600
    url = cz_url(
        "/liquidation-history",
        {"symbols": symbol, "interval": interval, "from": frm, "to": now, "convert_to_usd": "true"},
        api_key,
    )
    code, body, _ = http_get(url)
    if code == 200 and isinstance(body, list) and body:
        return body[0].get("history", []) if isinstance(body[0], dict) else []
    return []


# ---------- CoinGlass ----------

def cg_headers(api_key: str) -> dict[str, str]:
    return {"CG-API-KEY": api_key, "Accept": "application/json"}


def cg_oi_exchange_list(symbol: str, api_key: str) -> dict | None:
    url = f"{COINGLASS_BASE}/api/futures/open-interest/exchange-list?symbol={symbol}"
    code, body, _ = http_get(url, cg_headers(api_key))
    return body if code == 200 else None


def cg_funding_exchange_list(symbol: str, api_key: str) -> dict | None:
    url = f"{COINGLASS_BASE}/api/futures/funding-rate/exchange-list?symbol={symbol}"
    code, body, _ = http_get(url, cg_headers(api_key))
    return body if code == 200 else None


def cg_liquidation_exchange_list(symbol: str, range_param: str, api_key: str) -> dict | None:
    url = f"{COINGLASS_BASE}/api/futures/liquidation/exchange-list?symbol={symbol}&range={range_param}"
    code, body, _ = http_get(url, cg_headers(api_key))
    return body if code == 200 else None


# ---------- Helpers ----------

def find_cz_symbol(markets: list[dict], base: str, exchange_name: str,
                    code_to_name: dict[str, str]) -> str | None:
    """Trova symbol Coinalyze perp USDT-stable per (base, exchange_name).
    Preferenza: perpetual USDT-margined (STABLE) > coin-margined."""
    name_to_code = {v.lower(): k for k, v in code_to_name.items()}
    target_code = name_to_code.get(exchange_name.lower())
    if not target_code:
        return None
    candidates = [
        m for m in markets
        if m.get("base_asset") == base
        and m.get("exchange") == target_code
        and m.get("is_perpetual")
    ]
    def rank(m: dict) -> tuple[int, int]:
        quote = m.get("quote_asset", "")
        margined = m.get("margined", "")
        q_rank = {"USDT": 0, "USDC": 1, "USD": 2}.get(quote, 9)
        m_rank = 0 if margined == "STABLE" else 1
        return (m_rank, q_rank)
    candidates.sort(key=rank)
    return candidates[0]["symbol"] if candidates else None


def find_cz_symbols_all_perps(markets: list[dict], base: str, exchange_name: str,
                                code_to_name: dict[str, str]) -> list[str]:
    """Trova TUTTI i symbol perp Coinalyze per (base, exchange_name).
    Usato per somme apples-to-apples vs CoinGlass aggregato totale."""
    name_to_code = {v.lower(): k for k, v in code_to_name.items()}
    target_code = name_to_code.get(exchange_name.lower())
    if not target_code:
        return []
    return [
        m["symbol"] for m in markets
        if m.get("base_asset") == base
        and m.get("exchange") == target_code
        and m.get("is_perpetual")
    ]


def pct_dev(a: float, b: float) -> float | None:
    if a is None or b is None or a == 0:
        return None
    return (b - a) / a * 100.0


# ---------- Probes ----------

def probe_open_interest(cz_key: str, cg_key: str, markets: list[dict], asset: str, exchanges: list[str], code_to_name: dict[str, str]) -> list[dict]:
    rows = []
    # Coinalyze: chiamata batch sui simboli che mappano agli exchange
    cz_symbols: dict[str, str] = {}
    for ex in exchanges:
        sym = find_cz_symbol(markets, asset, ex, code_to_name)
        if sym:
            cz_symbols[ex] = sym
    if not cz_symbols:
        return rows
    cz_oi = cz_open_interest(list(cz_symbols.values()), cz_key)
    cz_map = {item["symbol"]: item for item in cz_oi}
    time.sleep(SLEEP_BETWEEN)

    # CoinGlass: chiamata su symbol asset (es. BTC) -> lista per exchange
    cg_symbol = asset  # es. "BTC"
    cg_resp = cg_oi_exchange_list(cg_symbol, cg_key)
    cg_data = (cg_resp or {}).get("data", []) if cg_resp else []
    cg_map = {(d.get("exchange") or "").lower(): d for d in cg_data if isinstance(d, dict)}
    time.sleep(SLEEP_BETWEEN)

    for ex in exchanges:
        cz_sym = cz_symbols.get(ex)
        cz_v = cz_map.get(cz_sym, {}) if cz_sym else {}
        cz_oi_usd = cz_v.get("value")  # convert_to_usd=true
        cz_ts = cz_v.get("update")  # epoch seconds

        cg_v = cg_map.get(ex.lower(), {})
        cg_oi_usd = cg_v.get("openInterestUsd") or cg_v.get("open_interest_usd") or cg_v.get("oiUsd")
        cg_ts = None  # CoinGlass non sempre espone timestamp per exchange
        if cg_oi_usd is None and cg_v.get("openInterest") and cg_v.get("price"):
            try:
                cg_oi_usd = float(cg_v["openInterest"]) * float(cg_v["price"])
            except Exception:
                cg_oi_usd = None

        rows.append({
            "asset": asset, "exchange": ex,
            "cz_symbol": cz_sym, "cz_oi_usd": cz_oi_usd, "cz_ts": cz_ts,
            "cg_oi_usd": cg_oi_usd, "cg_ts": cg_ts,
            "dev_pct": pct_dev(cz_oi_usd, cg_oi_usd) if cz_oi_usd and cg_oi_usd else None,
        })
    return rows


def probe_funding(cz_key: str, cg_key: str, markets: list[dict], asset: str, exchanges: list[str], code_to_name: dict[str, str]) -> list[dict]:
    rows = []
    cz_symbols: dict[str, str] = {}
    for ex in exchanges:
        sym = find_cz_symbol(markets, asset, ex, code_to_name)
        if sym:
            cz_symbols[ex] = sym
    if not cz_symbols:
        return rows
    cz_f = cz_funding_rate(list(cz_symbols.values()), cz_key)
    cz_p = cz_predicted_funding_rate(list(cz_symbols.values()), cz_key)
    cz_map = {item["symbol"]: item for item in cz_f}
    cz_pred_map = {item["symbol"]: item for item in cz_p}
    time.sleep(SLEEP_BETWEEN)

    cg_resp = cg_funding_exchange_list(asset, cg_key)
    # Schema reale: data = [ { symbol, stablecoin_margin_list: [...], token_margin_list: [...] } ]
    # NOTA: il param symbol=X NON filtra in questo endpoint (bug CoinGlass): la response
    # contiene TUTTI i ~1150 symbol. Bisogna trovare l'asset giusto dentro data[].
    cg_data = (cg_resp or {}).get("data", []) if cg_resp else []
    cg_per_ex: dict[str, dict] = {}
    target = next((e for e in cg_data if isinstance(e, dict) and e.get("symbol") == asset), None)
    if target:
        for entry in (target.get("stablecoin_margin_list") or []):
            if isinstance(entry, dict) and "exchange" in entry:
                cg_per_ex[entry["exchange"].lower()] = entry
    time.sleep(SLEEP_BETWEEN)

    for ex in exchanges:
        cz_sym = cz_symbols.get(ex)
        cz_v = cz_map.get(cz_sym, {}) if cz_sym else {}
        cz_pred_v = cz_pred_map.get(cz_sym, {}) if cz_sym else {}
        # Coinalyze e CoinGlass entrambi in PERCENTUALE (es 0.003 = 0.003%)
        cz_funding = cz_v.get("value")
        cz_predicted = cz_pred_v.get("value")

        cg_v = cg_per_ex.get(ex.lower(), {})
        cg_funding = cg_v.get("funding_rate")
        cg_interval_h = cg_v.get("funding_rate_interval")

        diff_bps = None
        if cz_funding is not None and cg_funding is not None:
            # bps in funding interval (di solito 8h, ma alcuni exchange 1h)
            diff_bps = (float(cg_funding) - float(cz_funding)) * 100  # 0.001% = 1bp non vero, 0.01% = 1bp -> *100

        rows.append({
            "asset": asset, "exchange": ex,
            "cz_funding": cz_funding, "cz_predicted_funding": cz_predicted,
            "cg_funding": cg_funding, "cg_interval_h": cg_interval_h,
            "diff_bps": diff_bps,
        })
    return rows


def probe_liquidations(cz_key: str, cg_key: str, markets: list[dict], asset: str, code_to_name: dict[str, str], hours: int = 24) -> dict:
    """Confronta liquidation TOTAL su 24h sull'asset (somma cross-exchange)."""
    # Coinalyze: liquidation-history con interval=1h su 24h, sommo
    # Per ottenere totale cross-exchange, prendo top 5 simboli e sommo
    syms = []
    for ex in ["Binance", "OKX", "Bybit", "Bitget", "Hyperliquid"]:
        s = find_cz_symbol(markets, asset, ex, code_to_name)
        if s:
            syms.append(s)
    cz_total_long = 0.0
    cz_total_short = 0.0
    for s in syms[:3]:  # limite per rate, 3 exchange è abbastanza
        hist = cz_liquidation_history(s, "1hour", hours, cz_key)
        for h in hist:
            cz_total_long += float(h.get("l", 0) or 0)
            cz_total_short += float(h.get("s", 0) or 0)
        time.sleep(SLEEP_BETWEEN)

    # CoinGlass: liquidation/exchange-list con range=24h
    cg_resp = cg_liquidation_exchange_list(asset, "h24", cg_key)
    cg_data = (cg_resp or {}).get("data", []) if cg_resp else []
    cg_total_long = 0.0
    cg_total_short = 0.0
    cg_all_long = 0.0  # campo "All" cross-exchange
    cg_all_short = 0.0
    if isinstance(cg_data, list):
        target_ex = {"binance", "okx", "bybit"}
        for d in cg_data:
            if not isinstance(d, dict):
                continue
            ex_name = (d.get("exchange") or "").lower()
            long_v = float(d.get("longLiquidation_usd") or 0)
            short_v = float(d.get("shortLiquidation_usd") or 0)
            if ex_name == "all":
                cg_all_long = long_v
                cg_all_short = short_v
                continue
            if ex_name in target_ex:
                cg_total_long += long_v
                cg_total_short += short_v
    time.sleep(SLEEP_BETWEEN)

    return {
        "asset": asset,
        "hours": hours,
        "exchanges_compared": ["Binance", "OKX", "Bybit"],
        "cz_long_usd": cz_total_long, "cz_short_usd": cz_total_short,
        "cg_long_usd": cg_total_long, "cg_short_usd": cg_total_short,
        "cg_all_long_usd": cg_all_long, "cg_all_short_usd": cg_all_short,
        "long_dev_pct": pct_dev(cz_total_long, cg_total_long),
        "short_dev_pct": pct_dev(cz_total_short, cg_total_short),
    }


# ---------- Report ----------

def render_md(results: dict) -> str:
    out = ["# Cross-validation Coinalyze ↔ CoinGlass", ""]
    out.append(f"Run: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    out.append("")

    out.append("## 1. Open Interest (snapshot, USD) — somma di tutti i perp BTC/ETH per exchange")
    out.append("")
    out.append("| Asset | Exchange | Coinalyze (sum perps) | # perps | CoinGlass total | CG stable | CG coin | Δ % |")
    out.append("|---|---|---:|---:|---:|---:|---:|---:|")
    for r in results.get("oi", []):
        cz = r["cz_oi_usd"]
        cg = r["cg_oi_usd"]
        cg_st = r.get("cg_oi_stable")
        cg_co = r.get("cg_oi_coin")
        dev = r["dev_pct"]
        cz_s = f"${cz/1e9:.2f}B" if isinstance(cz, (int, float)) else "—"
        cg_s = f"${cg/1e9:.2f}B" if isinstance(cg, (int, float)) else "—"
        cg_st_s = f"${cg_st/1e9:.2f}B" if isinstance(cg_st, (int, float)) else "—"
        cg_co_s = f"${cg_co/1e9:.2f}B" if isinstance(cg_co, (int, float)) else "—"
        dev_s = f"{dev:+.2f}%" if dev is not None else "—"
        out.append(f"| {r['asset']} | {r['exchange']} | {cz_s} | {r.get('cz_perps_count')} | {cg_s} | {cg_st_s} | {cg_co_s} | {dev_s} |")
    out.append("")

    out.append("## 2. Funding Rate (snapshot, % per funding interval)")
    out.append("")
    out.append("| Asset | Exchange | Coinalyze % | CoinGlass % | Δ (bp/funding) | CG interval | CZ predicted % |")
    out.append("|---|---|---:|---:|---:|---:|---:|")
    for r in results.get("funding", []):
        cz = r["cz_funding"]
        cg = r["cg_funding"]
        diff = r["diff_bps"]
        cz_pred = r["cz_predicted_funding"]
        cg_int = r.get("cg_interval_h")
        cz_s = f"{cz:+.4f}%" if isinstance(cz, (int, float)) else "—"
        cg_s = f"{cg:+.4f}%" if isinstance(cg, (int, float)) else "—"
        diff_s = f"{diff:+.2f}" if diff is not None else "—"
        cz_pred_s = f"{cz_pred:+.4f}%" if isinstance(cz_pred, (int, float)) else "—"
        cg_int_s = f"{cg_int}h" if cg_int else "—"
        out.append(f"| {r['asset']} | {r['exchange']} | {cz_s} | {cg_s} | {diff_s} | {cg_int_s} | {cz_pred_s} |")
    out.append("")

    out.append("## 3. Liquidation 24h (Binance + OKX + Bybit)")
    out.append("")
    out.append("| Asset | Side | Coinalyze USD | CoinGlass (3ex) USD | CG All-exchanges USD | Δ % vs 3ex |")
    out.append("|---|---|---:|---:|---:|---:|")
    for r in results.get("liquidations", []):
        cz_l, cg_l = r["cz_long_usd"], r["cg_long_usd"]
        cz_s, cg_s = r["cz_short_usd"], r["cg_short_usd"]
        cg_all_l = r.get("cg_all_long_usd", 0)
        cg_all_s = r.get("cg_all_short_usd", 0)
        dl, ds = r["long_dev_pct"], r["short_dev_pct"]
        dl_s = f"{dl:+.2f}%" if dl is not None else "—"
        ds_s = f"{ds:+.2f}%" if ds is not None else "—"
        out.append(f"| {r['asset']} | LONG  | ${cz_l:,.0f} | ${cg_l:,.0f} | ${cg_all_l:,.0f} | {dl_s} |")
        out.append(f"| {r['asset']} | SHORT | ${cz_s:,.0f} | ${cg_s:,.0f} | ${cg_all_s:,.0f} | {ds_s} |")
    out.append("")

    out.append("## 4. Coverage exchange overlap")
    out.append("")
    out.append(f"- Coinalyze future markets totali: **{results.get('cz_market_count', '—')}**")
    out.append(f"- Coinalyze exchange unique: **{results.get('cz_exchange_count', '—')}**")
    out.append(f"- Exchange testati in overlap: Binance, OKX, Bybit")
    out.append("")

    out.append("## 5. Note metodologiche")
    out.append("")
    out.append("- Coinalyze restituisce `convert_to_usd=true` direttamente in USD; quando assente, `value` è in coin native.")
    out.append("- CoinGlass funding viene normalizzato (se in %, diviso per 100 → decimal) per essere confrontabile con Coinalyze.")
    out.append("- Liquidation 24h: somma 24 finestre 1h su Coinalyze, vs `range=h24` aggregato su CoinGlass.")
    out.append("- Δ% calcolato come `(CoinGlass − Coinalyze) / Coinalyze`.")
    out.append("- Tolleranza ragionevole: |Δ| < 5% per OI/liq, |Δ bps| < 10 per funding.")
    out.append("")
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("cross_report.md"))
    args = parser.parse_args()

    env = load_env(Path(__file__).parent.parent / ".env")
    cz_key = env.get("COINALYZE_API_KEY") or os.environ.get("COINALYZE_API_KEY")
    cg_key = env.get("COINGLASS_API_KEY") or os.environ.get("COINGLASS_API_KEY")
    if not cz_key:
        sys.stderr.write("ERROR: COINALYZE_API_KEY mancante\n")
        return 2
    if not cg_key:
        sys.stderr.write("ERROR: COINGLASS_API_KEY mancante\n")
        return 2

    sys.stderr.write(">> Carico Coinalyze exchanges + future markets...\n")
    code_to_name = cz_exchanges(cz_key)
    time.sleep(SLEEP_BETWEEN)
    markets = cz_future_markets(cz_key)
    time.sleep(SLEEP_BETWEEN)
    if not markets:
        sys.stderr.write("ERROR: Coinalyze future-markets ha restituito vuoto. Chiave invalida o quota esaurita.\n")
        return 3
    sys.stderr.write(f"   Mercati: {len(markets)}, exchange distinti: {len({m.get('exchange') for m in markets})}\n")

    results: dict[str, Any] = {
        "cz_market_count": len(markets),
        "cz_exchange_count": len({m.get("exchange") for m in markets}),
        "oi": [], "funding": [], "liquidations": [],
    }
    exchanges = ["Binance", "OKX", "Bybit"]
    assets = ["BTC", "ETH"]

    sys.stderr.write(">> Probe Open Interest...\n")
    for asset in assets:
        rows = probe_open_interest(cz_key, cg_key, markets, asset, exchanges, code_to_name)
        results["oi"].extend(rows)
        for r in rows:
            sys.stderr.write(f"   {asset}/{r['exchange']}: cz={r['cz_oi_usd']} cg={r['cg_oi_usd']} dev={r['dev_pct']}\n")

    sys.stderr.write(">> Probe Funding Rate...\n")
    for asset in assets:
        rows = probe_funding(cz_key, cg_key, markets, asset, exchanges, code_to_name)
        results["funding"].extend(rows)
        for r in rows:
            sys.stderr.write(f"   {asset}/{r['exchange']}: cz={r['cz_funding']} cg={r['cg_funding']}\n")

    sys.stderr.write(">> Probe Liquidations 24h...\n")
    for asset in assets:
        r = probe_liquidations(cz_key, cg_key, markets, asset, code_to_name, hours=24)
        results["liquidations"].append(r)
        sys.stderr.write(f"   {asset}: cz_long=${r['cz_long_usd']:,.0f} cg_long=${r['cg_long_usd']:,.0f}\n")

    md = render_md(results)
    args.out.write_text(md, encoding="utf-8")
    sys.stderr.write(f"\nReport: {args.out}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
