"""
Smoke test Hyperliquid native API (gratis, no auth).

Hyperliquid è perp DEX onchain con API public POST /info gratuita senza auth.
Validato 2026-05-01: 6 endpoint AVAILABLE, copre asset universe + prices +
contexts + funding + per-wallet state.

Ruolo nel sistema gex-agentkit:
- Sostituisce CoinGlass /api/hyperliquid/* (gated Standard)
- Fornisce dati OI/funding/premium per 230 asset perp (incluso BTC, ETH, alts)
- Per-wallet state via clearinghouseState (per whale-onchain-monitor)

LIMITAZIONI:
- /info non espone "leaderboard" come tipo public — solo via dashboard scraping
- Per identificare top wallets serve whitelist manuale o scrape

API: https://api.hyperliquid.xyz/info (POST)
Docs: https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint

Uso:
    python3 tests/test_hyperliquid.py [--out hl_report.md]
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import sys
import time
from pathlib import Path
from typing import Any
import urllib.error
import urllib.request


HL_INFO_URL = "https://api.hyperliquid.xyz/info"
TIMEOUT = 15.0


@dataclasses.dataclass
class ProbeResult:
    name: str
    body: dict[str, Any]
    http_status: int | None
    classification: str
    sample: str
    elapsed_ms: int
    response_size_bytes: int


def post_json(body: dict[str, Any], timeout: float = TIMEOUT) -> tuple[int | None, Any, int, int]:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(HL_INFO_URL, data=data, method="POST",
                                  headers={"Content-Type": "application/json"})
    started = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            elapsed = int((time.time() - started) * 1000)
            return resp.status, json.loads(raw.decode("utf-8")), elapsed, len(raw)
    except urllib.error.HTTPError as e:
        elapsed = int((time.time() - started) * 1000)
        try:
            return e.code, e.read().decode("utf-8")[:300], elapsed, 0
        except Exception:
            return e.code, None, elapsed, 0
    except Exception as e:
        elapsed = int((time.time() - started) * 1000)
        return None, {"_error": str(e)}, elapsed, 0


def classify(http_status: int | None, body: Any) -> tuple[str, str]:
    if http_status is None:
        return "ERROR", "no response"
    if http_status == 404:
        return "NOT_FOUND", "HTTP 404"
    if http_status >= 500:
        return "ERROR", f"HTTP {http_status}"
    if http_status == 200:
        if body is None:
            return "ERROR", "empty body"
        if isinstance(body, list) and not body:
            return "AVAILABLE_EMPTY", ""
        if isinstance(body, dict) and not body:
            return "AVAILABLE_EMPTY", ""
        return "AVAILABLE", ""
    return "ERROR", f"HTTP {http_status}"


def short_sample(body: Any) -> str:
    if isinstance(body, list):
        s = f"list[{len(body)}]"
        if body and isinstance(body[0], dict):
            keys = list(body[0].keys())[:6]
            s += " keys=" + ",".join(keys)
        return s
    if isinstance(body, dict):
        keys = list(body.keys())[:6]
        return "dict keys=" + ",".join(keys)
    return str(type(body).__name__)


# Wallet pubblico noto Hyperliquid per test clearinghouseState/openOrders
TEST_WALLET = "0xf1fdb8c4ddf1e89a88c0adfba31fb39e1b1bfbd5"

PROBES: list[dict[str, Any]] = [
    {"name": "meta (universe 230 asset)", "body": {"type": "meta"}},
    {"name": "allMids (current prices)", "body": {"type": "allMids"}},
    {"name": "metaAndAssetCtxs (OI/funding/premium per asset)",
     "body": {"type": "metaAndAssetCtxs"}},
    {"name": "fundingHistory BTC 24h",
     "body": {"type": "fundingHistory", "coin": "BTC",
              "startTime": int(time.time() * 1000) - 86400000}},
    {"name": "clearinghouseState wallet test",
     "body": {"type": "clearinghouseState", "user": TEST_WALLET}},
    {"name": "openOrders wallet test",
     "body": {"type": "openOrders", "user": TEST_WALLET}},
    # Tentativi che potrebbero non essere disponibili public:
    {"name": "userFills wallet test (limit 100)",
     "body": {"type": "userFills", "user": TEST_WALLET}},
    {"name": "candleSnapshot BTC 1h",
     "body": {"type": "candleSnapshot",
              "req": {"coin": "BTC", "interval": "1h",
                      "startTime": int(time.time() * 1000) - 86400000,
                      "endTime": int(time.time() * 1000)}}},
    {"name": "l2Book BTC (orderbook)",
     "body": {"type": "l2Book", "coin": "BTC"}},
    {"name": "userVaultEquities wallet",
     "body": {"type": "userVaultEquities", "user": TEST_WALLET}},
]


def run_probes() -> list[ProbeResult]:
    results: list[ProbeResult] = []
    total = len(PROBES)
    for i, probe in enumerate(PROBES, 1):
        sys.stderr.write(f"[{i:02d}/{total}] {probe['name']:<50s} ")
        sys.stderr.flush()
        status, body, elapsed, size = post_json(probe["body"])
        cls, msg = classify(status, body)
        sample = short_sample(body) if cls.startswith("AVAILABLE") else (msg or "")
        results.append(ProbeResult(
            name=probe["name"], body=probe["body"], http_status=status,
            classification=cls, sample=sample, elapsed_ms=elapsed,
            response_size_bytes=size,
        ))
        sys.stderr.write(f"{cls:<16s} ({elapsed} ms, {size} b)\n")
        time.sleep(0.5)  # Hyperliquid rate limit safe
    return results


def render_md(results: list[ProbeResult]) -> str:
    out: list[str] = []
    out.append("# Hyperliquid Native API smoke-test report")
    out.append("")
    out.append(f"Run: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    out.append(f"Endpoint: `{HL_INFO_URL}` (POST, no auth)")
    out.append(f"Probes: **{len(results)}**")
    out.append("")

    by_cls: dict[str, list[ProbeResult]] = {}
    for r in results:
        by_cls.setdefault(r.classification, []).append(r)

    out.append("## Sintesi")
    out.append("")
    out.append("| Classe | Conteggio |")
    out.append("|---|---:|")
    for cls in ("AVAILABLE", "AVAILABLE_EMPTY", "NOT_FOUND", "ERROR"):
        out.append(f"| {cls} | {len(by_cls.get(cls, []))} |")
    out.append("")

    out.append("## Dettaglio")
    out.append("")
    out.append("| Endpoint | Class | HTTP | ms | Size | Sample |")
    out.append("|---|---|---|---:|---:|---|")
    for r in results:
        out.append(f"| `{r.name}` | **{r.classification}** | {r.http_status} | {r.elapsed_ms} | {r.response_size_bytes} | {r.sample[:80]} |")
    out.append("")

    out.append("## Note operative")
    out.append("")
    out.append("- Hyperliquid `/info` POST è **gratis e non richiede auth**")
    out.append("- 230 asset disponibili nel universe (BTC, ETH, ATOM, MATIC, DYDX, e altri)")
    out.append("- `metaAndAssetCtxs` espone in singola call: OI, funding, premium, oracle, mark, mid price per ogni asset")
    out.append("- `fundingHistory` ritorna ~24 sample per 24h (granularità oraria)")
    out.append("- Per-wallet state richiede address pubblico (Hyperliquid è onchain perp, gli address sono pubblici per design)")
    out.append("- **NON disponibile come API public**: leaderboard top traders. Va via scraping dashboard https://app.hyperliquid.xyz/leaderboard")
    out.append("")
    out.append("## Uso nel sistema gex-agentkit")
    out.append("")
    out.append("- `whale-onchain-monitor`: usa `clearinghouseState` per top 20 wallet whitelisted + `metaAndAssetCtxs` per OI delta cross-asset")
    out.append("- `gex-liquidation-forecast`: usa `metaAndAssetCtxs.openInterest` per cross-validation con CoinGlass exchange-list")
    out.append("- `funding-arb-detector`: aggiunge Hyperliquid come 4° venue ai 3 esistenti (Binance, Bybit, OKX) — basis comparison cross-DEX/CEX")

    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("hl_report.md"))
    args = parser.parse_args()

    sys.stderr.write(f"Eseguo {len(PROBES)} probe Hyperliquid native API\n\n")
    results = run_probes()

    md = render_md(results)
    args.out.write_text(md, encoding="utf-8")
    sys.stderr.write(f"\nReport: {args.out}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
