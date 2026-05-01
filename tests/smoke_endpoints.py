"""
Smoke test CoinGlass API per piano Hobbyist.

Usa la chiave reale (env COINGLASS_API_KEY) per probare gli endpoint marcati
"DA VERIFICARE CON KEY" in INTEGRATION-NOTES.md, oltre a un set di control
endpoint sicuramente disponibili. Produce un report markdown classificando
ogni endpoint come AVAILABLE / GATED / ERROR / NOT_FOUND.

Uso:
    export COINGLASS_API_KEY=...
    python tests/smoke_endpoints.py [--out report.md] [--ws]

Note:
- Rate limit reale Hobbyist = 30 rpm. Lo script chiama 1 endpoint ogni 2.5s
  (24 rpm effettivi) per stare tranquilli.
- Codice 0 + data non vuoto = AVAILABLE.
- Codice 40001 con msg che contiene "upgrade"/"plan" = GATED.
- Codice 50001 = RATE_LIMIT (lo script attende e ritenta una volta).
- HTTP 4xx o code != 0 senza upgrade hint = ERROR.
- Lo script NON modifica nulla del frontend o dello stato server: read-only.
"""

from __future__ import annotations

import argparse
import asyncio
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


BASE_URL = "https://open-api-v4.coinglass.com"
WS_URL = "wss://open-api-v4.coinglass.com/ws"
RATE_LIMIT_RPM = 24  # 80% di 30 rpm Hobbyist
SLEEP_BETWEEN = 60.0 / RATE_LIMIT_RPM  # 2.5s


@dataclasses.dataclass
class ProbeResult:
    name: str
    method: str
    path: str
    params: dict[str, Any]
    http_status: int | None
    body_code: str | None
    body_msg: str | None
    classification: str  # AVAILABLE | GATED | ERROR | NOT_FOUND | RATE_LIMIT
    sample_keys: list[str]
    elapsed_ms: int


def classify(http_status: int | None, body: dict | None) -> tuple[str, str | None, str | None]:
    if http_status is None:
        return "ERROR", None, "no response"
    if http_status == 404:
        return "NOT_FOUND", None, "HTTP 404"
    if not body:
        return "ERROR", None, f"HTTP {http_status} no body"

    code = str(body.get("code", ""))
    msg = body.get("msg", "")
    msg_lower = (msg or "").lower()

    if code == "0":
        data = body.get("data")
        if data is None or (isinstance(data, list) and len(data) == 0):
            return "AVAILABLE_EMPTY", code, msg
        return "AVAILABLE", code, msg

    if code == "50001":
        return "RATE_LIMIT", code, msg

    # CoinGlass usa 401 per "Upgrade plan" e 403 per "interval not available"
    # entrambi sono gating per il piano Hobbyist
    if any(kw in msg_lower for kw in ("upgrade", "plan", "tier", "subscribe", "permission")):
        return "GATED", code, msg
    if "interval is not available" in msg_lower or "not available for your current api" in msg_lower:
        return "GATED_INTERVAL", code, msg
    if code in ("400",) or "required" in msg_lower or "parameter" in msg_lower:
        return "BAD_PARAMS", code, msg
    if code == "30001":
        return "ERROR", code, msg

    return "ERROR", code, msg


def http_get(path: str, params: dict[str, Any], api_key: str, timeout: float = 20.0) -> tuple[int | None, dict | None, int]:
    url = BASE_URL + path
    if params:
        url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None})
    req = urllib.request.Request(
        url,
        headers={
            "CG-API-KEY": api_key,
            "Accept": "application/json",
            "User-Agent": "gex-agentkit-smoke/1.0",
        },
    )
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


def sample_keys(body: dict | None, depth: int = 2) -> list[str]:
    if not body:
        return []
    data = body.get("data")
    if isinstance(data, list) and data:
        first = data[0]
        if isinstance(first, dict):
            return sorted(list(first.keys()))[:depth * 8]
    if isinstance(data, dict):
        return sorted(list(data.keys()))[:depth * 8]
    return []


PROBES: list[dict[str, Any]] = [
    # === CONTROL: dovrebbero funzionare su Hobbyist ===
    {"name": "supported-coins", "path": "/api/futures/supported-coins", "params": {}},
    {"name": "supported-exchange-pairs", "path": "/api/futures/supported-exchange-pairs", "params": {}},
    {"name": "coins-markets", "path": "/api/futures/coins-markets", "params": {}},
    {"name": "open-interest-history-1h", "path": "/api/futures/open-interest/history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "funding-rate-history", "path": "/api/futures/funding-rate/history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "liquidation-aggregated-history", "path": "/api/futures/liquidation/aggregated-history",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100, "exchange_list": "Binance,OKX,Bybit"}},
    {"name": "global-long-short-account-ratio", "path": "/api/futures/global-long-short-account-ratio/history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "cgdi-index-history", "path": "/api/futures/cgdi-index/history",
     "params": {"interval": "4h", "limit": 100}},

    # === ETF: dovrebbe funzionare ===
    {"name": "etf-bitcoin-list", "path": "/api/etf/bitcoin/list", "params": {}},
    {"name": "etf-bitcoin-flow-history", "path": "/api/etf/bitcoin/flow-history", "params": {}},
    {"name": "etf-bitcoin-net-assets-history", "path": "/api/etf/bitcoin/net-assets/history", "params": {}},
    {"name": "etf-bitcoin-premium-discount-history", "path": "/api/etf/bitcoin/premium-discount/history", "params": {}},
    {"name": "etf-ethereum-list", "path": "/api/etf/ethereum/list", "params": {}},
    {"name": "etf-hong-kong-bitcoin-flow-history", "path": "/api/hk-etf/bitcoin/flow-history", "params": {}},

    # === DA VERIFICARE: probabile gating Standard+ ===
    {"name": "futures-rsi-list", "path": "/api/futures/rsi/list", "params": {}},
    {"name": "orderbook-history", "path": "/api/futures/orderbook/history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "orderbook-large-limit-order", "path": "/api/futures/orderbook/large-limit-order",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance"}},
    {"name": "orderbook-large-limit-order-history", "path": "/api/futures/orderbook/large-limit-order-history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "footprint", "path": "/api/futures/volume/footprint-history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "liquidation-heatmap-model1-1y", "path": "/api/futures/liquidation/heatmap/model1",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "range": "1y"}},
    {"name": "liquidation-heatmap-model1-180d", "path": "/api/futures/liquidation/heatmap/model1",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "range": "180d"}},
    {"name": "liquidation-heatmap-model2-180d", "path": "/api/futures/liquidation/heatmap/model2",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "range": "180d"}},
    {"name": "liquidation-heatmap-model3-180d", "path": "/api/futures/liquidation/heatmap/model3",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "range": "180d"}},
    {"name": "liquidation-aggregated-heatmap-model3", "path": "/api/futures/liquidation/aggregated-heatmap/model3",
     "params": {"symbol": "BTC", "range": "180d"}},

    # === HYPERLIQUID ===
    {"name": "hyperliquid-whale-alert", "path": "/api/hyperliquid/whale-alert", "params": {"symbol": "BTC"}},
    {"name": "hyperliquid-whale-position", "path": "/api/hyperliquid/whale-position", "params": {"symbol": "BTC"}},

    # === CVD (mancanti dal documento originale) ===
    {"name": "cvd-history", "path": "/api/futures/cvd/history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "aggregated-cvd-history", "path": "/api/futures/aggregated-cvd/history",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100}},

    # === TAKER (verifica se il path /v2/ è reale) ===
    {"name": "taker-buy-sell-volume-history", "path": "/api/futures/taker-buy-sell-volume/history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "taker-buy-sell-volume-history-v2", "path": "/api/futures/v2/taker-buy-sell-volume/history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "aggregated-taker-buy-sell-volume", "path": "/api/futures/aggregated-taker-buy-sell-volume/history",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100, "exchange_list": "Binance,OKX,Bybit"}},

    # === OPTIONS ===
    {"name": "option-info", "path": "/api/option/info", "params": {"symbol": "BTC"}},
    {"name": "option-max-pain", "path": "/api/option/max-pain", "params": {"symbol": "BTC", "exchange": "Deribit"}},
    {"name": "option-exchange-oi-history", "path": "/api/option/exchange-oi-history",
     "params": {"symbol": "BTC", "range": "4h", "unit": "USD"}},

    # === MACRO/OTHER ===
    {"name": "coinbase-premium-index", "path": "/api/coinbase-premium-index",
     "params": {"interval": "4h", "limit": 100}},
    {"name": "fear-greed-history", "path": "/api/index/fear-greed-history", "params": {}},
    {"name": "stable-coin-marketcap-history", "path": "/api/index/stableCoin-marketCap-history", "params": {}},
    {"name": "exchange-balance-list", "path": "/api/exchange/balance/list", "params": {"symbol": "BTC"}},

    # === INDICI V3 LEGACY (potrebbero essere stati rimossi silenziosamente) ===
    {"name": "index-ahr999", "path": "/api/index/ahr999", "params": {}},
    {"name": "index-puell-multiple", "path": "/api/index/puell-multiple", "params": {}},
    {"name": "index-golden-ratio-multiplier", "path": "/api/index/golden-ratio-multiplier", "params": {}},
    {"name": "index-pi-cycle", "path": "/api/index/pi-cycle-indicator", "params": {}},
    {"name": "index-stock-flow", "path": "/api/index/stock-flow", "params": {}},
    {"name": "index-bitcoin-rainbow", "path": "/api/index/bitcoin/rainbow-chart", "params": {}},
    {"name": "index-bitcoin-bubble-index", "path": "/api/index/bitcoin/bubble-index", "params": {}},

    # === ACCOUNT (verifica quota e piano) ===
    {"name": "user-account-subscription", "path": "/api/user/account/subscription", "params": {}},

    # === FUTURES — extended coverage ===
    {"name": "futures-pairs-markets", "path": "/api/futures/pairs-markets",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance"}},
    {"name": "futures-price-ohlc-history", "path": "/api/futures/price/history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "futures-exchange-rank", "path": "/api/futures/exchange-rank", "params": {}},
    {"name": "futures-delisted-pairs", "path": "/api/futures/delisted-exchange-pairs", "params": {}},
    {"name": "futures-supported-exchanges", "path": "/api/futures/supported-exchanges", "params": {}},
    {"name": "futures-funding-rate-oi-weight", "path": "/api/futures/funding-rate/oi-weight-history",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100}},
    {"name": "futures-funding-rate-vol-weight", "path": "/api/futures/funding-rate/vol-weight-history",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100}},
    {"name": "futures-funding-rate-cumulative", "path": "/api/futures/funding-rate/accumulated-exchange-list",
     "params": {"symbol": "BTC", "range": "1d"}},
    {"name": "futures-top-long-short-account-ratio", "path": "/api/futures/top-long-short-account-ratio/history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "futures-top-long-short-position-ratio", "path": "/api/futures/top-long-short-position-ratio/history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "futures-coin-aggregated-orderbook", "path": "/api/futures/orderbook/aggregated-ask-bids-history",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100, "exchange_list": "Binance,OKX,Bybit", "range": "1"}},
    {"name": "futures-aggregated-taker-buy-sell-volume-fix", "path": "/api/futures/aggregated-taker-buy-sell-volume/history",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100, "exchange_list": "Binance,OKX,Bybit"}},
    {"name": "futures-liquidation-aggregated-history-fix", "path": "/api/futures/liquidation/aggregated-history",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100}},

    # === SPOTS ===
    {"name": "spot-supported-coins", "path": "/api/spot/supported-coins", "params": {}},
    {"name": "spot-supported-exchange-pairs", "path": "/api/spot/supported-exchange-pairs", "params": {}},
    {"name": "spot-pairs-markets", "path": "/api/spot/pairs-markets",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance"}},
    {"name": "spot-price-history", "path": "/api/spot/price/history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "spot-orderbook-ask-bids", "path": "/api/spot/orderbook/ask-bids-history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "spot-aggregated-orderbook", "path": "/api/spot/orderbook/aggregated-ask-bids-history",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100, "exchange_list": "Binance,OKX,Bybit", "range": "1"}},
    {"name": "spot-coin-taker-buy-sell-history", "path": "/api/spot/aggregated-taker-buy-sell-volume/history",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100, "exchange_list": "Binance,OKX,Bybit"}},
    {"name": "spot-pair-taker-buy-sell-history", "path": "/api/spot/taker-buy-sell-volume/history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},

    # === OPTIONS — extended ===
    {"name": "option-info-fix", "path": "/api/option/info", "params": {"symbol": "BTC"}},
    {"name": "option-exchange-vol-history", "path": "/api/option/exchange-vol-history",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100}},
    {"name": "option-exchange-oi-history-fix", "path": "/api/option/exchange-oi-history",
     "params": {"symbol": "BTC", "range": "4h", "unit": "USD"}},

    # === ETF — extended (path corretti dal catalog) ===
    {"name": "etf-bitcoin-net-assets-fix", "path": "/api/etf/bitcoin/net-assets/history", "params": {}},
    {"name": "etf-bitcoin-premium-discount-fix", "path": "/api/etf/bitcoin/premium-discount/history", "params": {"ticker": "IBIT"}},
    {"name": "etf-bitcoin-history", "path": "/api/etf/bitcoin/history", "params": {"ticker": "IBIT"}},
    {"name": "etf-bitcoin-price-history", "path": "/api/etf/bitcoin/price/history", "params": {"ticker": "IBIT", "range": "1d"}},
    {"name": "etf-bitcoin-detail", "path": "/api/etf/bitcoin/detail", "params": {"ticker": "IBIT"}},
    {"name": "etf-hk-bitcoin-flow-fix", "path": "/api/hk-etf/bitcoin/flow-history", "params": {}},
    {"name": "etf-ethereum-flow-history", "path": "/api/etf/ethereum/flow-history", "params": {}},
    {"name": "etf-ethereum-net-assets", "path": "/api/etf/ethereum/net-assets/history", "params": {}},
    {"name": "etf-grayscale-holdings", "path": "/api/grayscale/holdings-list", "params": {}},
    {"name": "etf-solana-flow-history", "path": "/api/etf/solana/flow-history", "params": {}},
    {"name": "etf-xrp-flow-history", "path": "/api/etf/xrp/flow-history", "params": {}},

    # === ON-CHAIN — extended ===
    {"name": "exchange-assets", "path": "/api/exchange/assets", "params": {"exchange": "Binance"}},
    {"name": "exchange-balance-chart", "path": "/api/exchange/balance/chart",
     "params": {"symbol": "BTC", "exchange": "Binance"}},
    {"name": "exchange-onchain-transfers-erc20", "path": "/api/exchange/chain/tx/list",
     "params": {"symbol": "USDT", "min_usd": "1000000"}},

    # === INDIC — extended (path corretti dal catalog: kebab-case) ===
    {"name": "indic-futures-basis", "path": "/api/futures/basis/history",
     "params": {"exchange": "Binance", "symbol": "BTC", "interval": "4h", "limit": 100}},
    {"name": "indic-puell-multiple-fix", "path": "/api/index/puell-multiple", "params": {}},
    {"name": "indic-golden-ratio-fix", "path": "/api/index/golden-ratio-multiplier", "params": {}},
    {"name": "indic-pi-cycle-fix", "path": "/api/index/pi-cycle-indicator", "params": {}},
    {"name": "indic-stock-flow-fix", "path": "/api/index/stock-flow", "params": {}},
    {"name": "indic-bitcoin-bubble-fix", "path": "/api/index/bitcoin/bubble-index", "params": {}},
    {"name": "indic-bitcoin-profitable-days", "path": "/api/index/bitcoin/profitable-days", "params": {}},
    {"name": "indic-bull-market-peak", "path": "/api/bull-market-peak-indicator", "params": {}},
    {"name": "indic-2y-ma-multiplier", "path": "/api/index/2-year-ma-multiplier", "params": {}},
    {"name": "indic-200w-ma-heatmap", "path": "/api/index/200-week-moving-average-heatmap", "params": {}},
    {"name": "indic-cdri-index", "path": "/api/futures/cdri-index/history",
     "params": {"interval": "4h", "limit": 100}},
    {"name": "indic-bitfinex-margin-long-short", "path": "/api/bitfinex-margin-long-short",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100}},
    {"name": "indic-borrow-interest-rate", "path": "/api/borrow-interest-rate/history",
     "params": {"symbol": "BTC", "exchange": "Binance", "interval": "4h", "limit": 100}},

    # === OTHER ===
    {"name": "other-economic-calendar", "path": "/api/calendar/economic-data", "params": {}},
    {"name": "other-news-list", "path": "/api/article/list", "params": {"page": 1, "per_page": 10, "language": "en"}},

    # === ENDPOINT ESTRATTI DALLA DOC UFFICIALE 2026-04-30 (mai testati prima) ===
    {"name": "futures-coins-price-change", "path": "/api/futures/coins-price-change", "params": {}},
    {"name": "oi-aggregated-history", "path": "/api/futures/open-interest/aggregated-history",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100, "exchange_list": "Binance,OKX,Bybit"}},
    {"name": "oi-aggregated-stablecoin-history", "path": "/api/futures/open-interest/aggregated-stablecoin-history",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100}},
    {"name": "oi-aggregated-coin-margin-history", "path": "/api/futures/open-interest/aggregated-coin-margin-history",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100}},
    {"name": "oi-exchange-history-chart", "path": "/api/futures/open-interest/exchange-history-chart",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100}},
    {"name": "funding-rate-arbitrage", "path": "/api/futures/funding-rate/arbitrage", "params": {"symbol": "BTC"}},
    {"name": "taker-buy-sell-exchange-list", "path": "/api/futures/taker-buy-sell-volume/exchange-list",
     "params": {"symbol": "BTC", "range": "h24"}},
    {"name": "net-position-history", "path": "/api/futures/net-position/history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "net-position-v2-history", "path": "/api/futures/v2/net-position/history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "liq-aggregated-heatmap-model1", "path": "/api/futures/liquidation/aggregated-heatmap/model1",
     "params": {"symbol": "BTC", "range": "180d"}},
    {"name": "liq-aggregated-heatmap-model2", "path": "/api/futures/liquidation/aggregated-heatmap/model2",
     "params": {"symbol": "BTC", "range": "180d"}},
    {"name": "liq-pair-map", "path": "/api/futures/liquidation/map",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance"}},
    {"name": "liq-aggregated-map", "path": "/api/futures/liquidation/aggregated-map", "params": {"symbol": "BTC"}},
    {"name": "liq-max-pain", "path": "/api/futures/liquidation/max-pain",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance"}},
    {"name": "hyperliquid-position", "path": "/api/hyperliquid/position", "params": {"symbol": "BTC"}},
    {"name": "hyperliquid-user-position", "path": "/api/hyperliquid/user-position",
     "params": {"address": "0x5078c2fbea2b2ad61bc840bc023e35fce56bedb6"}},
    {"name": "hyperliquid-wallet-pnl-dist", "path": "/api/hyperliquid/wallet/pnl-distribution", "params": {}},
    {"name": "hyperliquid-global-l-s-account", "path": "/api/hyperliquid/global-long-short-account-ratio/history",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100}},
    {"name": "futures-netflow-list", "path": "/api/futures/netflow-list", "params": {}},
    {"name": "futures-coin-netflow-typo", "path": "/api/furures/coin/netflow",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100}},
    {"name": "futures-coin-netflow-fix", "path": "/api/futures/coin/netflow",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100}},
    {"name": "spot-coins-markets", "path": "/api/spot/coins-markets", "params": {}},
    {"name": "spot-orderbook-history", "path": "/api/spot/orderbook/history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "spot-large-limit-order", "path": "/api/spot/orderbook/large-limit-order",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance"}},
    {"name": "spot-large-limit-order-history", "path": "/api/spot/orderbook/large-limit-order-history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "spot-footprint", "path": "/api/spot/volume/footprint-history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "spot-cvd-history", "path": "/api/spot/cvd/history",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h", "limit": 100}},
    {"name": "spot-aggregated-cvd", "path": "/api/spot/aggregated-cvd/history",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100, "exchange_list": "Binance,OKX,Coinbase"}},
    {"name": "spot-netflow-list", "path": "/api/spot/netflow-list", "params": {}},
    {"name": "spot-coin-netflow", "path": "/api/spot/coin/netflow",
     "params": {"symbol": "BTC", "interval": "4h", "limit": 100}},
    {"name": "onchain-exchange-assets-transparency", "path": "/api/exchange_assets_transparency/list", "params": {}},
    {"name": "onchain-token-unlock-list", "path": "/api/coin/unlock-list", "params": {}},
    {"name": "onchain-token-vesting", "path": "/api/coin/vesting", "params": {"symbol": "ARB"}},
    {"name": "onchain-whale-transfer", "path": "/api/chain/v2/whale-transfer",
     "params": {"symbol": "BTC", "min_usd": 1000000}},
    {"name": "etf-bitcoin-aum", "path": "/api/etf/bitcoin/aum", "params": {}},
    {"name": "etf-grayscale-premium", "path": "/api/grayscale/premium-history", "params": {}},
    {"name": "indic-td-sequential", "path": "/api/futures/indicators/td",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h"}},
    {"name": "indic-coin-atr-list", "path": "/api/futures/avg-true-range/list", "params": {}},
    {"name": "indic-pair-atr", "path": "/api/futures/indicators/avg-true-range",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h"}},
    {"name": "indic-whale-index", "path": "/api/futures/whale-index/history",
     "params": {"interval": "4h", "limit": 100}},
    {"name": "indic-ma-native", "path": "/api/futures/indicators/ma",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h"}},
    {"name": "indic-ema-native", "path": "/api/futures/indicators/ema",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h"}},
    {"name": "indic-rsi-native", "path": "/api/futures/indicators/rsi",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h"}},
    {"name": "indic-macd-native", "path": "/api/futures/indicators/macd",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h"}},
    {"name": "indic-boll-native", "path": "/api/futures/indicators/boll",
     "params": {"symbol": "BTCUSDT", "exchange": "Binance", "interval": "4h"}},
    {"name": "indic-macd-list", "path": "/api/futures/macd/list", "params": {}},
    {"name": "indic-bitcoin-sth-sopr", "path": "/api/index/bitcoin-sth-sopr", "params": {}},
    {"name": "indic-bitcoin-lth-sopr", "path": "/api/index/bitcoin-lth-sopr", "params": {}},
    {"name": "indic-bitcoin-sth-realized-price", "path": "/api/index/bitcoin-sth-realized-price", "params": {}},
    {"name": "indic-bitcoin-lth-realized-price", "path": "/api/index/bitcoin-lth-realized-price", "params": {}},
    {"name": "indic-bitcoin-rhodl-ratio", "path": "/api/index/bitcoin-rhodl-ratio", "params": {}},
    {"name": "indic-bitcoin-sth-supply", "path": "/api/index/bitcoin-short-term-holder-supply", "params": {}},
    {"name": "indic-bitcoin-lth-supply", "path": "/api/index/bitcoin-long-term-holder-supply", "params": {}},
    {"name": "indic-bitcoin-new-addresses", "path": "/api/index/bitcoin-new-addresses", "params": {}},
    {"name": "indic-bitcoin-active-addresses", "path": "/api/index/bitcoin-active-addresses", "params": {}},
    {"name": "indic-bitcoin-reserve-risk", "path": "/api/index/bitcoin-reserve-risk", "params": {}},
    {"name": "indic-bitcoin-nupl", "path": "/api/index/bitcoin-net-unrealized-profit-loss", "params": {}},
    {"name": "indic-bitcoin-correlation", "path": "/api/index/bitcoin-correlation", "params": {}},
    {"name": "indic-bitcoin-bmo", "path": "/api/index/bitcoin-macro-oscillator", "params": {}},
    {"name": "indic-options-futures-oi-ratio", "path": "/api/index/option-vs-futures-oi-ratio", "params": {}},
    {"name": "indic-altcoin-season", "path": "/api/index/altcoin-season", "params": {}},
    {"name": "indic-btc-vs-global-m2", "path": "/api/index/bitcoin-vs-global-m2-growth", "params": {}},
    {"name": "indic-btc-vs-us-m2", "path": "/api/index/bitcoin-vs-us-m2-growth", "params": {}},
    {"name": "indic-bitcoin-dominance", "path": "/api/index/bitcoin-dominance", "params": {}},
    {"name": "indic-futures-spot-volume-ratio", "path": "/api/futures_spot_volume_ratio", "params": {}},

    # === NUOVI ENDPOINT scoperti dal llms.txt CoinGlass (mai testati prima) ===
    {"name": "btc-correlations-traditional", "path": "/api/index/bitcoin-correlation",
     "params": {}},  # GLD/IWM/QQQ/SPY/TLT correlations
    {"name": "indic-td-list-multicoin", "path": "/api/futures/td/list", "params": {}},
    {"name": "indic-ma-list-multicoin", "path": "/api/futures/ma/list", "params": {}},
    {"name": "indic-ema-list-multicoin", "path": "/api/futures/ema/list", "params": {}},
    {"name": "indic-rsi-list-pair", "path": "/api/futures/rsi/list", "params": {}},  # già testato
    {"name": "spot-coin-market-data-history", "path": "/api/spot/coin-market-data/history",
     "params": {"symbol": "BTC"}},
    {"name": "instruments-matrix", "path": "/api/futures/instruments", "params": {}},
]


def run_rest_probes(api_key: str) -> list[ProbeResult]:
    results: list[ProbeResult] = []
    total = len(PROBES)
    for i, probe in enumerate(PROBES, 1):
        sys.stderr.write(f"[{i:02d}/{total}] {probe['name']:<45s} ")
        sys.stderr.flush()
        status, body, elapsed = http_get(probe["path"], probe["params"], api_key)
        cls, code, msg = classify(status, body)
        if cls == "RATE_LIMIT":
            sys.stderr.write("⏳ rate-limited, waiting 5s and retrying...\n")
            time.sleep(5.0)
            status, body, elapsed = http_get(probe["path"], probe["params"], api_key)
            cls, code, msg = classify(status, body)
        keys = sample_keys(body)
        results.append(ProbeResult(
            name=probe["name"],
            method="GET",
            path=probe["path"],
            params=probe["params"],
            http_status=status,
            body_code=code,
            body_msg=msg,
            classification=cls,
            sample_keys=keys,
            elapsed_ms=elapsed,
        ))
        sys.stderr.write(f"{cls:<16s} ({elapsed} ms)\n")
        time.sleep(SLEEP_BETWEEN)
    return results


async def probe_websocket(api_key: str, channels: list[str], per_channel_timeout: float = 12.0) -> dict[str, Any]:
    """Probe ciascun canale WS singolarmente per identificare quali sono gated.
    Ritorna un dict {channel: {connected, subscribed_ack, messages, sample, error}}.
    """
    try:
        import websockets  # type: ignore
    except ImportError:
        return {"error": "Modulo `websockets` non installato. Installa con: pip install websockets"}

    summary: dict[str, Any] = {"url": WS_URL, "channels": {}}

    for ch in channels:
        ch_summary: dict[str, Any] = {"connected": False, "subscribed_ack": None, "messages_received": 0, "sample": [], "error": None}
        try:
            async with websockets.connect(WS_URL, additional_headers={"CG-API-KEY": api_key}, open_timeout=10) as ws:
                ch_summary["connected"] = True
                await ws.send(json.dumps({"op": "subscribe", "args": [ch]}))
                msgs: list[str] = []
                deadline = time.time() + per_channel_timeout
                while time.time() < deadline and len(msgs) < 5:
                    remaining = deadline - time.time()
                    if remaining <= 0:
                        break
                    try:
                        msg = await asyncio.wait_for(ws.recv(), timeout=remaining)
                        msgs.append(msg[:500] if isinstance(msg, str) else str(msg)[:500])
                    except asyncio.TimeoutError:
                        break
                ch_summary["messages_received"] = len(msgs)
                ch_summary["sample"] = msgs[:3]
                # Heuristica: primo msg con "subscribe"/"ack"/"error"/"upgrade" → segnale di gating o ack
                if msgs:
                    first = msgs[0].lower()
                    if "upgrade" in first or "tier" in first or "plan" in first or "permission" in first:
                        ch_summary["subscribed_ack"] = "GATED"
                    elif '"event":"subscribe"' in first or 'success' in first:
                        ch_summary["subscribed_ack"] = "OK"
                    else:
                        ch_summary["subscribed_ack"] = "DATA"
        except Exception as e:
            ch_summary["error"] = f"{type(e).__name__}: {e}"
        summary["channels"][ch] = ch_summary
        # Ritardo tra canali per non saturare
        await asyncio.sleep(1.0)
    return summary


def render_markdown(rest_results: list[ProbeResult], ws_summary: dict | None) -> str:
    by_cls: dict[str, list[ProbeResult]] = {}
    for r in rest_results:
        by_cls.setdefault(r.classification, []).append(r)

    out: list[str] = []
    out.append("# CoinGlass smoke-test report — Hobbyist plan")
    out.append("")
    out.append(f"Run time: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    out.append(f"Base URL: `{BASE_URL}`")
    out.append(f"Probes: **{len(rest_results)}**, rate ~{RATE_LIMIT_RPM} rpm")
    out.append("")
    out.append("## Sintesi per classificazione")
    out.append("")
    out.append("| Classe | Conteggio |")
    out.append("|---|---:|")
    for cls in ("AVAILABLE", "AVAILABLE_EMPTY", "GATED", "RATE_LIMIT", "ERROR", "NOT_FOUND"):
        out.append(f"| {cls} | {len(by_cls.get(cls, []))} |")
    out.append("")

    out.append("## Dettaglio")
    out.append("")
    out.append("| Endpoint | Path | Class | code | msg | ms | sample keys |")
    out.append("|---|---|---|---|---|---:|---|")
    for r in rest_results:
        msg = (r.body_msg or "").replace("|", "\\|")[:60]
        keys = ", ".join(r.sample_keys[:6]) if r.sample_keys else "—"
        out.append(f"| `{r.name}` | `{r.path}` | **{r.classification}** | {r.body_code or '—'} | {msg} | {r.elapsed_ms} | {keys} |")
    out.append("")

    if "GATED" in by_cls:
        out.append("## Endpoint GATED (richiedono upgrade)")
        out.append("")
        out.append("Su Hobbyist NON disponibili. Per ognuno: vedere INTEGRATION-NOTES.md §5 per il sostituto locale.")
        out.append("")
        for r in by_cls["GATED"]:
            out.append(f"- `{r.name}` → {r.body_msg}")
        out.append("")

    if "ERROR" in by_cls or "NOT_FOUND" in by_cls:
        out.append("## Endpoint ERROR / NOT_FOUND")
        out.append("")
        out.append("Path da rivedere: refuso editoriale o cambio di nome non documentato.")
        out.append("")
        for r in (by_cls.get("ERROR", []) + by_cls.get("NOT_FOUND", [])):
            out.append(f"- `{r.name}` ({r.path}): HTTP {r.http_status} code={r.body_code} msg={r.body_msg}")
        out.append("")

    if ws_summary is not None:
        out.append("## WebSocket")
        out.append("")
        out.append("```json")
        out.append(json.dumps(ws_summary, indent=2, default=str))
        out.append("```")
        out.append("")

    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("smoke_report.md"),
                        help="Path del report markdown")
    parser.add_argument("--ws", action="store_true",
                        help="Esegui anche probe WebSocket (richiede pip install websockets)")
    parser.add_argument("--ws-channel", action="append", default=None,
                        help="Canali WS da provare (default: liquidationOrders)")
    args = parser.parse_args()

    api_key = os.environ.get("COINGLASS_API_KEY")
    if not api_key:
        sys.stderr.write("ERROR: variabile COINGLASS_API_KEY non impostata.\n")
        return 2

    sys.stderr.write(f"Eseguo {len(PROBES)} probe REST (~{len(PROBES) * SLEEP_BETWEEN / 60:.1f} min)\n\n")
    rest_results = run_rest_probes(api_key)

    ws_summary = None
    if args.ws:
        channels = args.ws_channel or ["liquidationOrders", "largeLimitOrders", "tickers", "klines", "marketIndicator"]
        sys.stderr.write(f"\nProbo WebSocket sui canali: {channels}\n")
        ws_summary = asyncio.run(probe_websocket(api_key, channels))

    md = render_markdown(rest_results, ws_summary)
    args.out.write_text(md, encoding="utf-8")
    sys.stderr.write(f"\nReport scritto in: {args.out}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
