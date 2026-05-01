# Coinalyze API smoke-test report

Run: 2026-04-30 18:39:49 UTC
Base URL: `https://api.coinalyze.net/v1` — auth via `?api_key=...`
Probes: **21**, rate ~35 rpm (free tier 40 rpm)

## Sintesi

| Classe | Conteggio |
|---|---:|
| AVAILABLE | 19 |
| AVAILABLE_EMPTY | 0 |
| BAD_PARAMS | 0 |
| ERROR | 0 |
| NOT_FOUND | 2 |
| RATE_LIMIT | 0 |

## Dettaglio

| Endpoint | Path | Class | HTTP | ms | Sample |
|---|---|---|---|---:|---|
| `exchanges` | `/exchanges` | **AVAILABLE** | 200 | 562 | list[28] keys=name,code |
| `future-markets` | `/future-markets` | **AVAILABLE** | 200 | 908 | list[4255] keys=symbol,exchange,symbol_on_exchange,base_asset,quote_asset,expire |
| `spot-markets` | `/spot-markets` | **AVAILABLE** | 200 | 758 | list[6491] keys=symbol,exchange,symbol_on_exchange,base_asset,quote_asset,has_bu |
| `open-interest BTC binance` | `/open-interest` | **AVAILABLE** | 200 | 436 | list[1] keys=symbol,value,update |
| `open-interest multi-exchange` | `/open-interest` | **AVAILABLE** | 200 | 340 | list[2] keys=symbol,value,update |
| `funding-rate BTC binance` | `/funding-rate` | **AVAILABLE** | 200 | 319 | list[1] keys=symbol,value,update |
| `predicted-funding-rate (★ unico)` | `/predicted-funding-rate` | **AVAILABLE** | 200 | 327 | list[1] keys=symbol,value,update |
| `ohlcv-history BTC 1h` | `/ohlcv-history` | **AVAILABLE** | 200 | 343 | list[1] keys=symbol,history |
| `ohlcv-history BTC 1d` | `/ohlcv-history` | **AVAILABLE** | 200 | 442 | list[1] keys=symbol,history |
| `ohlcv-history BTC 1m intraday` | `/ohlcv-history` | **AVAILABLE** | 200 | 377 | list[1] keys=symbol,history |
| `open-interest-history BTC 1h` | `/open-interest-history` | **AVAILABLE** | 200 | 347 | list[1] keys=symbol,history |
| `open-interest-history BTC 5m` | `/open-interest-history` | **AVAILABLE** | 200 | 359 | list[1] keys=symbol,history |
| `funding-rate-history BTC 1h` | `/funding-rate-history` | **AVAILABLE** | 200 | 326 | list[1] keys=symbol,history |
| `predicted-funding-rate-history (★)` | `/predicted-funding-rate-history` | **AVAILABLE** | 200 | 316 | list[1] keys=symbol,history |
| `liquidation-history BTC 1h` | `/liquidation-history` | **AVAILABLE** | 200 | 287 | list[1] keys=symbol,history |
| `liquidation-history multi-symbol` | `/liquidation-history` | **AVAILABLE** | 200 | 378 | list[2] keys=symbol,history |
| `long-short-ratio-history` | `/long-short-ratio-history` | **AVAILABLE** | 200 | 381 | list[1] keys=symbol,history |
| `large-orders BTC` | `/large-orders` | **NOT_FOUND** | 404 | 243 | dict keys=message |
| `cvd-history (test)` | `/cvd-history` | **NOT_FOUND** | 404 | 239 | dict keys=message |
| `open-interest ETH binance` | `/open-interest` | **AVAILABLE** | 200 | 329 | list[1] keys=symbol,value,update |
| `funding-rate ETH binance` | `/funding-rate` | **AVAILABLE** | 200 | 329 | list[1] keys=symbol,value,update |
