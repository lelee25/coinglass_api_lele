# CoinGlass smoke-test report — Hobbyist plan

Run time: 2026-04-30 18:15:24 UTC
Base URL: `https://open-api-v4.coinglass.com`
Probes: **46**, rate ~24 rpm

## Sintesi per classificazione

| Classe | Conteggio |
|---|---:|
| AVAILABLE | 20 |
| AVAILABLE_EMPTY | 0 |
| GATED | 13 |
| RATE_LIMIT | 0 |
| ERROR | 0 |
| NOT_FOUND | 10 |

## Dettaglio

| Endpoint | Path | Class | code | msg | ms | sample keys |
|---|---|---|---|---|---:|---|
| `supported-coins` | `/api/futures/supported-coins` | **AVAILABLE** | 0 |  | 929 | — |
| `supported-exchange-pairs` | `/api/futures/supported-exchange-pairs` | **AVAILABLE** | 0 |  | 1916 | ApeX Omni, Aster, Binance, BingX, Bitfinex, Bitget |
| `coins-markets` | `/api/futures/coins-markets` | **GATED** | 401 | Upgrade plan | 468 | — |
| `open-interest-history-1h` | `/api/futures/open-interest/history` | **AVAILABLE** | 0 |  | 658 | close, high, low, open, time |
| `funding-rate-history` | `/api/futures/funding-rate/history` | **AVAILABLE** | 0 |  | 537 | close, high, low, open, time |
| `liquidation-aggregated-history` | `/api/futures/liquidation/aggregated-history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange_list' is not present | 529 | — |
| `global-long-short-account-ratio` | `/api/futures/global-long-short-account-ratio/history` | **AVAILABLE** | 0 |  | 783 | global_account_long_percent, global_account_long_short_ratio, global_account_short_percent, time |
| `cgdi-index-history` | `/api/futures/cgdi-index/history` | **AVAILABLE** | 0 |  | 893 | cgdi_index_value, time |
| `etf-bitcoin-list` | `/api/etf/bitcoin/list` | **AVAILABLE** | 0 |  | 638 | asset_details, aum_usd, cik_code, fund_name, fund_type, last_quote_time |
| `etf-bitcoin-flow-history` | `/api/etf/bitcoin/flow-history` | **AVAILABLE** | 0 |  | 1379 | etf_flows, flow_usd, price_usd, timestamp |
| `etf-bitcoin-net-assets-history` | `/api/etf/bitcoin/net-assets-history` | **NOT_FOUND** | — | HTTP 404 | 634 | — |
| `etf-bitcoin-premium-discount-history` | `/api/etf/bitcoin/premium-discount-history` | **NOT_FOUND** | — | HTTP 404 | 756 | — |
| `etf-ethereum-list` | `/api/etf/ethereum/list` | **AVAILABLE** | 0 |  | 664 | asset_details, aum_usd, fund_name, fund_type, last_quote_time, last_trade_time |
| `etf-hong-kong-bitcoin-flow-history` | `/api/etf/hong-kong-bitcoin/flow-history` | **NOT_FOUND** | — | HTTP 404 | 816 | — |
| `futures-rsi-list` | `/api/futures/rsi/list` | **GATED** | 401 | Upgrade plan | 763 | — |
| `orderbook-heatmap` | `/api/futures/orderbook/heatmap` | **NOT_FOUND** | — | HTTP 404 | 639 | — |
| `orderbook-large-limit-order` | `/api/futures/orderbook/large-limit-order` | **GATED** | 401 | Upgrade plan | 704 | — |
| `orderbook-large-limit-order-history` | `/api/futures/orderbook/large-limit-order-history` | **GATED** | 401 | Upgrade plan | 468 | — |
| `footprint` | `/api/futures/footprint` | **NOT_FOUND** | — | HTTP 404 | 527 | — |
| `liquidation-heatmap-model1-1y` | `/api/futures/liquidation/heatmap/model1` | **GATED** | 401 | Upgrade plan | 628 | — |
| `liquidation-heatmap-model1-180d` | `/api/futures/liquidation/heatmap/model1` | **GATED** | 401 | Upgrade plan | 753 | — |
| `liquidation-heatmap-model2-180d` | `/api/futures/liquidation/heatmap/model2` | **GATED** | 401 | Upgrade plan | 522 | — |
| `liquidation-heatmap-model3-180d` | `/api/futures/liquidation/heatmap/model3` | **GATED** | 401 | Upgrade plan | 454 | — |
| `liquidation-aggregated-heatmap-model3` | `/api/futures/liquidation/aggregated-heatmap/model3` | **GATED** | 401 | Upgrade plan | 550 | — |
| `hyperliquid-whale-alert` | `/api/hyperliquid/whale-alert` | **GATED** | 401 | Upgrade plan | 627 | — |
| `hyperliquid-whale-position` | `/api/hyperliquid/whale-position` | **GATED** | 401 | Upgrade plan | 463 | — |
| `cvd-history` | `/api/futures/cvd/history` | **GATED** | 401 | Upgrade plan | 448 | — |
| `aggregated-cvd-history` | `/api/futures/aggregated-cvd/history` | **GATED** | 401 | Upgrade plan | 492 | — |
| `taker-buy-sell-volume-history` | `/api/futures/taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 642 | taker_buy_volume_usd, taker_sell_volume_usd, time |
| `taker-buy-sell-volume-history-v2` | `/api/futures/v2/taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 512 | taker_buy_volume_usd, taker_sell_volume_usd, time |
| `aggregated-taker-buy-sell-volume` | `/api/futures/aggregated-taker-buy-sell-volume/history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange_list' is not present | 764 | — |
| `option-info` | `/api/option/info` | **AVAILABLE** | 0 |  | 819 | exchange_name, oi_market_share, open_interest, open_interest_change_24h, open_interest_usd, volume_change_percent_24h |
| `option-max-pain` | `/api/option/max-pain` | **AVAILABLE** | 0 |  | 464 | call_open_interest, call_open_interest_market_value, call_open_interest_notional, date, max_pain_price, put_open_interest |
| `option-exchange-oi-history` | `/api/option/exchange-oi-history` | **BAD_PARAMS** | 400 | Required String parameter 'range' is not present | 497 | — |
| `coinbase-premium-index` | `/api/coinbase-premium-index` | **AVAILABLE** | 0 | success | 430 | coinbase_price, premium, premium_rate, time |
| `fear-greed-history` | `/api/index/fear-greed-history` | **AVAILABLE** | 0 |  | 1121 | data_list, price_list, time_list |
| `stable-coin-marketcap-history` | `/api/index/stableCoin-marketCap-history` | **AVAILABLE** | 0 |  | 1356 | data_list, price_list, time_list |
| `exchange-balance-list` | `/api/exchange/balance/list` | **AVAILABLE** | 0 |  | 443 | balance_change_1d, balance_change_30d, balance_change_7d, balance_change_percent_1d, balance_change_percent_30d, balance_change_percent_7d |
| `index-ahr999` | `/api/index/ahr999` | **AVAILABLE** | 0 |  | 1676 | ahr999_value, average_price, current_value, date_string |
| `index-puell-multiple` | `/api/index/puell_multiple` | **NOT_FOUND** | — | HTTP 404 | 522 | — |
| `index-golden-ratio-multiplier` | `/api/index/golden_ratio_multiplier` | **NOT_FOUND** | — | HTTP 404 | 489 | — |
| `index-pi-cycle` | `/api/index/pi` | **NOT_FOUND** | — | HTTP 404 | 481 | — |
| `index-stock-flow` | `/api/index/stock_flow` | **NOT_FOUND** | — | HTTP 404 | 617 | — |
| `index-bitcoin-rainbow` | `/api/index/bitcoin/rainbow-chart` | **AVAILABLE** | 0 |  | 2554 | — |
| `index-bitcoin-bubble-index` | `/api/index/bitcoin_bubble_index` | **NOT_FOUND** | — | HTTP 404 | 895 | — |
| `user-account-subscription` | `/api/user/account/subscription` | **AVAILABLE** | 0 |  | 554 | expire_time, expired, level |

## Endpoint GATED (richiedono upgrade)

Su Hobbyist NON disponibili. Per ognuno: vedere INTEGRATION-NOTES.md §5 per il sostituto locale.

- `coins-markets` → Upgrade plan
- `futures-rsi-list` → Upgrade plan
- `orderbook-large-limit-order` → Upgrade plan
- `orderbook-large-limit-order-history` → Upgrade plan
- `liquidation-heatmap-model1-1y` → Upgrade plan
- `liquidation-heatmap-model1-180d` → Upgrade plan
- `liquidation-heatmap-model2-180d` → Upgrade plan
- `liquidation-heatmap-model3-180d` → Upgrade plan
- `liquidation-aggregated-heatmap-model3` → Upgrade plan
- `hyperliquid-whale-alert` → Upgrade plan
- `hyperliquid-whale-position` → Upgrade plan
- `cvd-history` → Upgrade plan
- `aggregated-cvd-history` → Upgrade plan

## Endpoint ERROR / NOT_FOUND

Path da rivedere: refuso editoriale o cambio di nome non documentato.

- `etf-bitcoin-net-assets-history` (/api/etf/bitcoin/net-assets-history): HTTP 404 code=None msg=HTTP 404
- `etf-bitcoin-premium-discount-history` (/api/etf/bitcoin/premium-discount-history): HTTP 404 code=None msg=HTTP 404
- `etf-hong-kong-bitcoin-flow-history` (/api/etf/hong-kong-bitcoin/flow-history): HTTP 404 code=None msg=HTTP 404
- `orderbook-heatmap` (/api/futures/orderbook/heatmap): HTTP 404 code=None msg=HTTP 404
- `footprint` (/api/futures/footprint): HTTP 404 code=None msg=HTTP 404
- `index-puell-multiple` (/api/index/puell_multiple): HTTP 404 code=None msg=HTTP 404
- `index-golden-ratio-multiplier` (/api/index/golden_ratio_multiplier): HTTP 404 code=None msg=HTTP 404
- `index-pi-cycle` (/api/index/pi): HTTP 404 code=None msg=HTTP 404
- `index-stock-flow` (/api/index/stock_flow): HTTP 404 code=None msg=HTTP 404
- `index-bitcoin-bubble-index` (/api/index/bitcoin_bubble_index): HTTP 404 code=None msg=HTTP 404
