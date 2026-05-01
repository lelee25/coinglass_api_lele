"""
Smoke test Coinalyze API (free tier, 40 rpm).

Probe sistematico di tutti gli endpoint pubblici dell'API Coinalyze v1
per validare disponibilità con la chiave free tier dell'utente.

Endpoint coperti (basati su https://api.coinalyze.net/v1/doc/):
- Discovery: /exchanges, /future-markets, /spot-markets
- Snapshot: /open-interest, /funding-rate, /predicted-funding-rate
- History: /open-interest-history, /funding-rate-history,
           /predicted-funding-rate-history, /liquidation-history,
           /long-short-ratio-history, /ohlcv-history, /large-orders
- Aggregate: /aggregated-open-interest, /aggregated-funding-rate

Uso:
    python3 tests/smoke_coinalyze.py [--out cz_report.md]

Note:
- Free tier: 40 calls/min, ~1.5s safe spacing.
- Auth: query param `api_key=...`.
- Base URL: https://api.coinalyze.net/v1
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


BASE_URL = "https://api.coinalyze.net/v1"
RATE_LIMIT_RPM = 35  # 87% di 40
SLEEP_BETWEEN = 60.0 / RATE_LIMIT_RPM  # ~1.7s
TIMEOUT = 20.0


@dataclasses.dataclass
class ProbeResult:
    name: str
    path: str
    params: dict[str, Any]
    http_status: int | None
    classification: str
    sample: str
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


def http_get(path: str, params: dict[str, Any], api_key: str) -> tuple[int | None, Any, int]:
    qp = {k: v for k, v in (params or {}).items() if v is not None}
    qp["api_key"] = api_key
    url = f"{BASE_URL}{path}?{urllib.parse.urlencode(qp)}"
    started = time.time()
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT) as resp:
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


def classify(http_status: int | None, body: Any) -> tuple[str, str]:
    if http_status is None:
        return "ERROR", "no response"
    if http_status == 404:
        return "NOT_FOUND", "HTTP 404"
    if http_status == 401:
        return "ERROR", "HTTP 401 unauthorized"
    if http_status == 429:
        return "RATE_LIMIT", "HTTP 429"
    if http_status == 400:
        msg = (body or {}).get("message", "") if isinstance(body, dict) else ""
        return "BAD_PARAMS", msg or "HTTP 400"
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


# Lista probe completa per Coinalyze v1
NOW = int(time.time())
DAY_AGO = NOW - 86400
WEEK_AGO = NOW - 7 * 86400

# Symbol Coinalyze: BTCUSDT_PERP.A = Binance perp
BTC_BINANCE = "BTCUSDT_PERP.A"
ETH_BINANCE = "ETHUSDT_PERP.A"
BTC_OKX = "BTCUSDT.3"
BTC_BYBIT = "BTCUSDT.6"

PROBES: list[dict[str, Any]] = [
    # === DISCOVERY ===
    {"name": "exchanges", "path": "/exchanges", "params": {}},
    {"name": "future-markets", "path": "/future-markets", "params": {}},
    {"name": "spot-markets", "path": "/spot-markets", "params": {}},

    # === SNAPSHOT ===
    {"name": "open-interest BTC binance", "path": "/open-interest",
     "params": {"symbols": BTC_BINANCE, "convert_to_usd": "true"}},
    {"name": "open-interest multi-exchange", "path": "/open-interest",
     "params": {"symbols": f"{BTC_BINANCE},{BTC_OKX},{BTC_BYBIT}", "convert_to_usd": "true"}},
    {"name": "funding-rate BTC binance", "path": "/funding-rate",
     "params": {"symbols": BTC_BINANCE}},
    {"name": "predicted-funding-rate (★ unico)", "path": "/predicted-funding-rate",
     "params": {"symbols": BTC_BINANCE}},

    # === HISTORY OHLC ===
    {"name": "ohlcv-history BTC 1h", "path": "/ohlcv-history",
     "params": {"symbols": BTC_BINANCE, "interval": "1hour", "from": DAY_AGO, "to": NOW}},
    {"name": "ohlcv-history BTC 1d", "path": "/ohlcv-history",
     "params": {"symbols": BTC_BINANCE, "interval": "daily", "from": WEEK_AGO, "to": NOW}},
    {"name": "ohlcv-history BTC 1m intraday", "path": "/ohlcv-history",
     "params": {"symbols": BTC_BINANCE, "interval": "1min", "from": NOW - 3600, "to": NOW}},

    # === OI HISTORY ===
    {"name": "open-interest-history BTC 1h", "path": "/open-interest-history",
     "params": {"symbols": BTC_BINANCE, "interval": "1hour", "from": DAY_AGO, "to": NOW,
                "convert_to_usd": "true"}},
    {"name": "open-interest-history BTC 5m", "path": "/open-interest-history",
     "params": {"symbols": BTC_BINANCE, "interval": "5min", "from": NOW - 7200, "to": NOW,
                "convert_to_usd": "true"}},

    # === FUNDING HISTORY ===
    {"name": "funding-rate-history BTC 1h", "path": "/funding-rate-history",
     "params": {"symbols": BTC_BINANCE, "interval": "1hour", "from": DAY_AGO, "to": NOW}},
    {"name": "predicted-funding-rate-history (★)", "path": "/predicted-funding-rate-history",
     "params": {"symbols": BTC_BINANCE, "interval": "1hour", "from": DAY_AGO, "to": NOW}},

    # === LIQUIDATION HISTORY ===
    {"name": "liquidation-history BTC 1h", "path": "/liquidation-history",
     "params": {"symbols": BTC_BINANCE, "interval": "1hour", "from": DAY_AGO, "to": NOW,
                "convert_to_usd": "true"}},
    {"name": "liquidation-history multi-symbol", "path": "/liquidation-history",
     "params": {"symbols": f"{BTC_BINANCE},{BTC_OKX},{BTC_BYBIT}", "interval": "1hour",
                "from": DAY_AGO, "to": NOW, "convert_to_usd": "true"}},

    # === LONG-SHORT RATIO ===
    {"name": "long-short-ratio-history", "path": "/long-short-ratio-history",
     "params": {"symbols": BTC_BINANCE, "interval": "1hour", "from": DAY_AGO, "to": NOW}},

    # === LARGE ORDERS / TAKER (potrebbero non esistere) ===
    {"name": "large-orders BTC", "path": "/large-orders",
     "params": {"symbols": BTC_BINANCE}},
    # Coinalyze potrebbe avere endpoint CVD: testiamolo (non documentato pubblicamente)
    {"name": "cvd-history (test)", "path": "/cvd-history",
     "params": {"symbols": BTC_BINANCE, "interval": "1hour", "from": DAY_AGO, "to": NOW}},

    # === MULTI-ASSET ===
    {"name": "open-interest ETH binance", "path": "/open-interest",
     "params": {"symbols": ETH_BINANCE, "convert_to_usd": "true"}},
    {"name": "funding-rate ETH binance", "path": "/funding-rate",
     "params": {"symbols": ETH_BINANCE}},
]


def run_probes(api_key: str) -> list[ProbeResult]:
    results: list[ProbeResult] = []
    total = len(PROBES)
    for i, probe in enumerate(PROBES, 1):
        sys.stderr.write(f"[{i:02d}/{total}] {probe['name']:<55s} ")
        sys.stderr.flush()
        status, body, elapsed = http_get(probe["path"], probe.get("params") or {}, api_key)
        cls, msg = classify(status, body)
        if cls == "RATE_LIMIT":
            time.sleep(5.0)
            status, body, elapsed = http_get(probe["path"], probe.get("params") or {}, api_key)
            cls, msg = classify(status, body)
        sample = short_sample(body)
        results.append(ProbeResult(
            name=probe["name"], path=probe["path"], params=probe.get("params") or {},
            http_status=status, classification=cls, sample=sample, elapsed_ms=elapsed,
        ))
        sys.stderr.write(f"{cls:<16s} ({elapsed} ms) {sample[:60]}\n")
        time.sleep(SLEEP_BETWEEN)
    return results


def render_md(results: list[ProbeResult]) -> str:
    by_cls: dict[str, list[ProbeResult]] = {}
    for r in results:
        by_cls.setdefault(r.classification, []).append(r)

    out: list[str] = []
    out.append("# Coinalyze API smoke-test report")
    out.append("")
    out.append(f"Run: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    out.append(f"Base URL: `{BASE_URL}` — auth via `?api_key=...`")
    out.append(f"Probes: **{len(results)}**, rate ~{RATE_LIMIT_RPM} rpm (free tier 40 rpm)")
    out.append("")

    out.append("## Sintesi")
    out.append("")
    out.append("| Classe | Conteggio |")
    out.append("|---|---:|")
    for cls in ("AVAILABLE", "AVAILABLE_EMPTY", "BAD_PARAMS", "ERROR", "NOT_FOUND", "RATE_LIMIT"):
        out.append(f"| {cls} | {len(by_cls.get(cls, []))} |")
    out.append("")

    out.append("## Dettaglio")
    out.append("")
    out.append("| Endpoint | Path | Class | HTTP | ms | Sample |")
    out.append("|---|---|---|---|---:|---|")
    for r in results:
        out.append(f"| `{r.name}` | `{r.path}` | **{r.classification}** | {r.http_status} | {r.elapsed_ms} | {r.sample[:80]} |")
    out.append("")

    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("cz_report.md"))
    args = parser.parse_args()

    env = load_env(Path(__file__).parent.parent / ".env")
    api_key = env.get("COINALYZE_API_KEY") or os.environ.get("COINALYZE_API_KEY")
    if not api_key:
        sys.stderr.write("ERROR: COINALYZE_API_KEY non impostato\n")
        return 2

    sys.stderr.write(f"Eseguo {len(PROBES)} probe Coinalyze (~{len(PROBES) * SLEEP_BETWEEN / 60:.1f} min)\n\n")
    results = run_probes(api_key)

    md = render_md(results)
    args.out.write_text(md, encoding="utf-8")
    sys.stderr.write(f"\nReport: {args.out}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
