"""
Smoke test CoinGecko Demo API.

Probe gli endpoint principali con la chiave Demo per validare:
- Quali endpoint funzionano davvero su Demo
- Quali sono PAID-ONLY (codice errore 10005)
- Coverage GeckoTerminal Onchain (gratis su Demo)
- Latenza tipica
- Schema response (sample keys)

Uso:
    export COINGECKO_API_KEY=...   # da .env
    python3 tests/smoke_coingecko.py [--out cg_report.md]

Note:
- Rate limit Demo = 30 rpm, budget 10k credits/mese.
- Lo script usa 1 chiamata ogni 2.2s (~27 rpm safe).
- Hostname Demo: https://api.coingecko.com/api/v3
- Header Demo: x-cg-demo-api-key
- Codice 10005 = endpoint richiede Pro tier
- Codice 10011 = chiave Demo su URL Pro (errore configurazione)
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import sys
import time
from pathlib import Path
from typing import Any
import urllib.error
import urllib.parse
import urllib.request


BASE_URL = "https://api.coingecko.com/api/v3"
RATE_LIMIT_RPM = 27
SLEEP_BETWEEN = 60.0 / RATE_LIMIT_RPM  # ~2.2s
TIMEOUT = 20.0


@dataclasses.dataclass
class ProbeResult:
    name: str
    path: str
    params: dict[str, Any]
    http_status: int | None
    body_code: int | None
    body_msg: str | None
    classification: str
    sample_keys: list[str]
    elapsed_ms: int


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


def http_get(path: str, params: dict[str, Any], api_key: str, timeout: float = TIMEOUT) -> tuple[int | None, Any, int]:
    qp = {k: v for k, v in (params or {}).items() if v is not None}
    url = BASE_URL + path
    if qp:
        url += "?" + urllib.parse.urlencode(qp)
    req = urllib.request.Request(url, headers={
        "x-cg-demo-api-key": api_key,
        "Accept": "application/json",
        "User-Agent": "gex-agentkit-smoke-cg/1.0",
    })
    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
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
    except Exception:
        elapsed = int((time.time() - started) * 1000)
        return None, None, elapsed


def classify(http_status: int | None, body: Any) -> tuple[str, int | None, str | None]:
    """CoinGecko codici noti:
      401 → No API key
      429 → Rate limit
      10005 → Paid plan required
      10010 → Pro key su Demo URL
      10011 → Demo key su Pro URL
    """
    if http_status is None:
        return "ERROR", None, "no response"
    if http_status == 404:
        return "NOT_FOUND", None, "HTTP 404"

    # CoinGecko espone errori in {"status": {"error_code": N, "error_message": "..."}}
    err_code = None
    err_msg = None
    if isinstance(body, dict):
        if "status" in body and isinstance(body["status"], dict):
            err_code = body["status"].get("error_code")
            err_msg = body["status"].get("error_message")
        elif "error" in body and isinstance(body["error"], str):
            err_msg = body["error"]

    if http_status == 200 and err_code is None:
        # data presente?
        if body is None:
            return "ERROR", None, "empty body"
        if isinstance(body, list) and not body:
            return "AVAILABLE_EMPTY", None, None
        if isinstance(body, dict) and not body:
            return "AVAILABLE_EMPTY", None, None
        return "AVAILABLE", None, None

    if http_status == 401:
        return "ERROR", err_code, err_msg or "no api key"
    if http_status == 429:
        return "RATE_LIMIT", err_code, err_msg
    if err_code == 10005:
        return "GATED", err_code, err_msg or "Paid plan required"
    if err_code in (10010, 10011):
        return "ERROR", err_code, err_msg or "wrong base URL for key type"
    if http_status == 400:
        return "BAD_PARAMS", err_code, err_msg
    return "ERROR", err_code, err_msg


def sample_keys(body: Any, max_keys: int = 8) -> list[str]:
    if isinstance(body, list) and body:
        first = body[0]
        if isinstance(first, dict):
            return sorted(first.keys())[:max_keys]
    if isinstance(body, dict):
        return sorted(body.keys())[:max_keys]
    return []


# Lista endpoint da probare. Group by area.
PROBES: list[dict[str, Any]] = [
    # === HEALTH & ACCOUNT ===
    {"name": "ping", "path": "/ping", "params": {}},
    {"name": "key (account info & usage)", "path": "/key", "params": {}},

    # === SIMPLE ===
    {"name": "simple/price BTC,ETH", "path": "/simple/price",
     "params": {"ids": "bitcoin,ethereum", "vs_currencies": "usd",
                "include_market_cap": "true", "include_24hr_vol": "true",
                "include_24hr_change": "true", "include_last_updated_at": "true"}},
    {"name": "simple/supported_vs_currencies", "path": "/simple/supported_vs_currencies", "params": {}},
    {"name": "simple/token_price (USDT eth)", "path": "/simple/token_price/ethereum",
     "params": {"contract_addresses": "0xdac17f958d2ee523a2206206994597c13d831ec7",
                "vs_currencies": "usd"}},

    # === COINS — discovery & list ===
    {"name": "coins/list (universe)", "path": "/coins/list", "params": {"include_platform": "false"}},
    {"name": "coins/list/new (latest 200)", "path": "/coins/list/new", "params": {}},
    {"name": "coins/markets Top 250", "path": "/coins/markets",
     "params": {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 250, "page": 1,
                "sparkline": "false",
                "price_change_percentage": "1h,24h,7d"}},
    {"name": "coins/top_gainers_losers (PAID?)", "path": "/coins/top_gainers_losers",
     "params": {"vs_currency": "usd", "duration": "24h"}},

    # === COIN DETAIL ===
    {"name": "coins/{id} bitcoin", "path": "/coins/bitcoin",
     "params": {"localization": "false", "tickers": "false",
                "community_data": "false", "developer_data": "false"}},
    {"name": "coins/{id}/tickers BTC", "path": "/coins/bitcoin/tickers", "params": {"page": 1}},
    {"name": "coins/{id}/market_chart 30d", "path": "/coins/bitcoin/market_chart",
     "params": {"vs_currency": "usd", "days": 30}},
    {"name": "coins/{id}/market_chart/range", "path": "/coins/bitcoin/market_chart/range",
     "params": {"vs_currency": "usd",
                "from": int(time.time()) - 30*86400, "to": int(time.time())}},
    {"name": "coins/{id}/ohlc 30d", "path": "/coins/bitcoin/ohlc",
     "params": {"vs_currency": "usd", "days": 30}},
    {"name": "coins/{id}/ohlc/range (PAID?)", "path": "/coins/bitcoin/ohlc/range",
     "params": {"vs_currency": "usd",
                "from": int(time.time()) - 7*86400, "to": int(time.time()),
                "interval": "hourly"}},
    {"name": "coins/{id}/circulating_supply_chart (PAID?)", "path": "/coins/bitcoin/circulating_supply_chart",
     "params": {"days": 30}},
    {"name": "coins/{id}/history (DD-MM-YYYY)", "path": "/coins/bitcoin/history",
     "params": {"date": time.strftime("%d-%m-%Y", time.gmtime(time.time() - 7*86400))}},

    # === DISCOVERY ===
    {"name": "search/trending", "path": "/search/trending", "params": {}},
    {"name": "search?query=solana", "path": "/search", "params": {"query": "solana"}},

    # === CATEGORIES ===
    {"name": "coins/categories/list", "path": "/coins/categories/list", "params": {}},
    {"name": "coins/categories", "path": "/coins/categories",
     "params": {"order": "market_cap_change_24h_desc"}},

    # === GLOBAL ===
    {"name": "global", "path": "/global", "params": {}},
    {"name": "global/decentralized_finance_defi", "path": "/global/decentralized_finance_defi", "params": {}},
    {"name": "global/market_cap_chart (PAID?)", "path": "/global/market_cap_chart",
     "params": {"days": 30}},

    # === EXCHANGES ===
    {"name": "exchanges (page1)", "path": "/exchanges", "params": {"per_page": 50, "page": 1}},
    {"name": "exchanges/list", "path": "/exchanges/list", "params": {}},
    {"name": "exchanges/{id}/tickers Binance", "path": "/exchanges/binance/tickers",
     "params": {"page": 1, "depth": "false"}},

    # === DERIVATIVES ===
    {"name": "derivatives", "path": "/derivatives", "params": {}},
    {"name": "derivatives/exchanges", "path": "/derivatives/exchanges", "params": {}},

    # === COMPANIES (PUBLIC TREASURY) ===
    {"name": "companies/public_treasury bitcoin", "path": "/companies/public_treasury/bitcoin", "params": {}},

    # === NFTS (informativi) ===
    {"name": "nfts/list", "path": "/nfts/list", "params": {"per_page": 10, "page": 1}},

    # === ASSET PLATFORMS ===
    {"name": "asset_platforms", "path": "/asset_platforms", "params": {}},

    # === ON-CHAIN (GeckoTerminal) ===
    {"name": "onchain/networks", "path": "/onchain/networks", "params": {}},
    {"name": "onchain/networks/eth/dexes", "path": "/onchain/networks/eth/dexes", "params": {}},
    {"name": "onchain/networks/trending_pools", "path": "/onchain/networks/trending_pools", "params": {}},
    {"name": "onchain/networks/eth/new_pools", "path": "/onchain/networks/eth/new_pools", "params": {}},
    {"name": "onchain/networks/eth/trending_pools", "path": "/onchain/networks/eth/trending_pools", "params": {}},
    {"name": "onchain/pools/megafilter", "path": "/onchain/pools/megafilter",
     "params": {"sort": "h24_volume_usd_desc"}},
    {"name": "onchain/simple/networks/eth/token_price USDT", "path": "/onchain/simple/networks/eth/token_price/0xdac17f958d2ee523a2206206994597c13d831ec7", "params": {}},
    {"name": "onchain/networks/eth/tokens/{addr} USDT", "path": "/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7", "params": {}},
    {"name": "onchain/networks/eth/tokens/{addr}/info", "path": "/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/info", "params": {}},
    {"name": "onchain/networks/eth/tokens/{addr}/top_holders (PAID?)", "path": "/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/top_holders", "params": {}},
    {"name": "onchain/networks/eth/tokens/{addr}/holders_chart", "path": "/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/holders_chart", "params": {"days": 7}},
    {"name": "onchain/networks/eth/tokens/{addr}/top_traders", "path": "/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/top_traders", "params": {"days": 1}},
    # un pool noto USDT/USDC su Uniswap v3
    {"name": "onchain/networks/eth/pools/{addr}/trades", "path": "/onchain/networks/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/trades", "params": {}},
    {"name": "onchain/networks/eth/pools/{addr}/ohlcv/hour", "path": "/onchain/networks/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/ohlcv/hour", "params": {}},

    # === §22.6 — endpoint llms.txt mai testati ===
    # COIN BY CONTRACT: WBTC su ethereum
    {"name": "coins/{id}/contract/{addr} WBTC", "path": "/coins/ethereum/contract/0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",
     "params": {}},
    {"name": "coins/{id}/contract/{addr}/market_chart 30d", "path": "/coins/ethereum/contract/0x2260fac5e5542a773aa44fbcfedf7c193bc2c599/market_chart",
     "params": {"vs_currency": "usd", "days": 30}},
    {"name": "coins/{id}/contract/{addr}/market_chart/range", "path": "/coins/ethereum/contract/0x2260fac5e5542a773aa44fbcfedf7c193bc2c599/market_chart/range",
     "params": {"vs_currency": "usd",
                "from": int(time.time()) - 7*86400, "to": int(time.time())}},

    # === ENTITIES / PUBLIC TREASURY ===
    # entities/list espone slug autoritativi; usare quelli (non "microstrategy" — slug rinominato)
    {"name": "entities/list", "path": "/entities/list", "params": {}},
    {"name": "public_treasury/{entity_id} tesla", "path": "/public_treasury/tesla", "params": {}},
    {"name": "public_treasury/{entity_id}/transaction_history", "path": "/public_treasury/tesla/transaction_history", "params": {}},
    # NOTA: /public_treasury/{entity}/holding_chart e /{entity}/public_treasury/{coin_id}
    # promessi dall'llms.txt ma in realtà NON ESISTONO su Demo (verificato: HTTP 404 con entity reale).

    # === ONCHAIN BATCH / DISCOVERY (llms.txt) ===
    {"name": "onchain/networks/eth/pools/multi/{addrs}", "path": "/onchain/networks/eth/pools/multi/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640,0xcbcdf9626bc03e24f779434178a73a0b4bad62ed", "params": {}},
    {"name": "onchain/networks/eth/tokens/multi/{addrs}", "path": "/onchain/networks/eth/tokens/multi/0xdac17f958d2ee523a2206206994597c13d831ec7,0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", "params": {}},
    {"name": "onchain/tokens/info_recently_updated", "path": "/onchain/tokens/info_recently_updated", "params": {}},
    {"name": "onchain/networks/eth/pools/{addr}/info", "path": "/onchain/networks/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/info", "params": {}},
    {"name": "onchain/search/pools?query=ETH", "path": "/onchain/search/pools",
     "params": {"query": "ETH", "network": "eth"}},
    {"name": "onchain/networks/eth/dexes/{dex}/pools", "path": "/onchain/networks/eth/dexes/uniswap_v3/pools", "params": {}},
    {"name": "onchain/networks/eth/tokens/{addr}/pools", "path": "/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/pools", "params": {}},

    # === EXCHANGE RATES & TOKEN LISTS ===
    {"name": "exchange_rates", "path": "/exchange_rates", "params": {}},
    {"name": "token_lists/ethereum/all.json", "path": "/token_lists/ethereum/all.json", "params": {}},
]


def run_probes(api_key: str) -> list[ProbeResult]:
    results: list[ProbeResult] = []
    total = len(PROBES)
    for i, probe in enumerate(PROBES, 1):
        sys.stderr.write(f"[{i:02d}/{total}] {probe['name']:<60s} ")
        sys.stderr.flush()
        status, body, elapsed = http_get(probe["path"], probe.get("params") or {}, api_key)
        cls, code, msg = classify(status, body)
        # un retry su rate-limit
        if cls == "RATE_LIMIT":
            sys.stderr.write("⏳ rate-limited, attendo 5s e ritento...\n")
            time.sleep(5.0)
            status, body, elapsed = http_get(probe["path"], probe.get("params") or {}, api_key)
            cls, code, msg = classify(status, body)
        keys = sample_keys(body)
        results.append(ProbeResult(
            name=probe["name"], path=probe["path"], params=probe.get("params") or {},
            http_status=status, body_code=code, body_msg=msg,
            classification=cls, sample_keys=keys, elapsed_ms=elapsed,
        ))
        sys.stderr.write(f"{cls:<16s} ({elapsed} ms)\n")
        time.sleep(SLEEP_BETWEEN)
    return results


def render_md(results: list[ProbeResult]) -> str:
    by_cls: dict[str, list[ProbeResult]] = {}
    for r in results:
        by_cls.setdefault(r.classification, []).append(r)

    out: list[str] = []
    out.append("# CoinGecko Demo API smoke-test report")
    out.append("")
    out.append(f"Run: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    out.append(f"Base URL: `{BASE_URL}` — header `x-cg-demo-api-key`")
    out.append(f"Probes: **{len(results)}**, rate ~{RATE_LIMIT_RPM} rpm")
    out.append("")

    out.append("## Sintesi per classificazione")
    out.append("")
    out.append("| Classe | Conteggio |")
    out.append("|---|---:|")
    for cls in ("AVAILABLE", "AVAILABLE_EMPTY", "GATED", "RATE_LIMIT", "BAD_PARAMS", "ERROR", "NOT_FOUND"):
        out.append(f"| {cls} | {len(by_cls.get(cls, []))} |")
    out.append("")

    out.append("## Dettaglio")
    out.append("")
    out.append("| Endpoint | Path | Class | code | msg | ms | sample keys |")
    out.append("|---|---|---|---|---|---:|---|")
    for r in results:
        msg = (r.body_msg or "").replace("|", "\\|")[:60]
        keys = ", ".join(r.sample_keys[:6]) if r.sample_keys else "—"
        out.append(f"| `{r.name}` | `{r.path}` | **{r.classification}** | {r.body_code or '—'} | {msg} | {r.elapsed_ms} | {keys} |")
    out.append("")

    if "GATED" in by_cls:
        out.append("## Endpoint GATED (richiedono Pro tier)")
        out.append("")
        out.append("Su Demo questi NON funzionano. Il prompt CoinGecko ne menzionava alcuni come PAID-ONLY (top_gainers_losers, market_cap_chart). Verifichiamoli.")
        out.append("")
        for r in by_cls["GATED"]:
            out.append(f"- `{r.name}` → code {r.body_code} {r.body_msg}")
        out.append("")

    if "ERROR" in by_cls or "NOT_FOUND" in by_cls:
        out.append("## ERROR / NOT_FOUND")
        out.append("")
        for r in (by_cls.get("ERROR", []) + by_cls.get("NOT_FOUND", [])):
            out.append(f"- `{r.name}` ({r.path}): HTTP {r.http_status} code={r.body_code} msg={r.body_msg}")
        out.append("")

    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("cg_report.md"))
    args = parser.parse_args()

    env = load_env(Path(__file__).parent.parent / ".env")
    api_key = env.get("COINGECKO_API_KEY") or os.environ.get("COINGECKO_API_KEY")
    if not api_key:
        sys.stderr.write("ERROR: COINGECKO_API_KEY non impostato\n")
        return 2

    sys.stderr.write(f"Eseguo {len(PROBES)} probe su Demo (~{len(PROBES) * SLEEP_BETWEEN / 60:.1f} min)\n\n")
    results = run_probes(api_key)

    md = render_md(results)
    args.out.write_text(md, encoding="utf-8")
    sys.stderr.write(f"\nReport: {args.out}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
