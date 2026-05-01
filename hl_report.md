# Hyperliquid Native API smoke-test report

Run: 2026-05-01 02:50:34 UTC
Endpoint: `https://api.hyperliquid.xyz/info` (POST, no auth)
Probes: **10**

## Sintesi

| Classe | Conteggio |
|---|---:|
| AVAILABLE | 7 |
| AVAILABLE_EMPTY | 3 |
| NOT_FOUND | 0 |
| ERROR | 0 |

## Dettaglio

| Endpoint | Class | HTTP | ms | Size | Sample |
|---|---|---|---:|---:|---|
| `meta (universe 230 asset)` | **AVAILABLE** | 200 | 559 | 17056 | dict keys=universe,marginTables,collateralToken |
| `allMids (current prices)` | **AVAILABLE** | 200 | 449 | 9246 | dict keys=0G,2Z,@1,@10,@100,@101 |
| `metaAndAssetCtxs (OI/funding/premium per asset)` | **AVAILABLE** | 200 | 582 | 71509 | list[2] keys=universe,marginTables,collateralToken |
| `fundingHistory BTC 24h` | **AVAILABLE** | 200 | 460 | 2199 | list[24] keys=coin,fundingRate,premium,time |
| `clearinghouseState wallet test` | **AVAILABLE** | 200 | 835 | 309 | dict keys=marginSummary,crossMarginSummary,crossMaintenanceMarginUsed,withdrawab |
| `openOrders wallet test` | **AVAILABLE_EMPTY** | 200 | 473 | 2 | list[0] |
| `userFills wallet test (limit 100)` | **AVAILABLE_EMPTY** | 200 | 569 | 2 | list[0] |
| `candleSnapshot BTC 1h` | **AVAILABLE** | 200 | 482 | 3478 | list[25] keys=t,T,s,i,o,c |
| `l2Book BTC (orderbook)` | **AVAILABLE** | 200 | 556 | 1576 | dict keys=coin,time,levels |
| `userVaultEquities wallet` | **AVAILABLE_EMPTY** | 200 | 488 | 2 | list[0] |

## Note operative

- Hyperliquid `/info` POST è **gratis e non richiede auth**
- 230 asset disponibili nel universe (BTC, ETH, ATOM, MATIC, DYDX, e altri)
- `metaAndAssetCtxs` espone in singola call: OI, funding, premium, oracle, mark, mid price per ogni asset
- `fundingHistory` ritorna ~24 sample per 24h (granularità oraria)
- Per-wallet state richiede address pubblico (Hyperliquid è onchain perp, gli address sono pubblici per design)
- **NON disponibile come API public**: leaderboard top traders. Va via scraping dashboard https://app.hyperliquid.xyz/leaderboard

## Uso nel sistema gex-agentkit

- `whale-onchain-monitor`: usa `clearinghouseState` per top 20 wallet whitelisted + `metaAndAssetCtxs` per OI delta cross-asset
- `gex-liquidation-forecast`: usa `metaAndAssetCtxs.openInterest` per cross-validation con CoinGlass exchange-list
- `funding-arb-detector`: aggiunge Hyperliquid come 4° venue ai 3 esistenti (Binance, Bybit, OKX) — basis comparison cross-DEX/CEX