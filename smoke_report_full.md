# CoinGlass smoke-test report — Hobbyist plan

Run time: 2026-04-30 18:43:52 UTC
Base URL: `https://open-api-v4.coinglass.com`
Probes: **99**, rate ~24 rpm

## Sintesi per classificazione

| Classe | Conteggio |
|---|---:|
| AVAILABLE | 52 |
| AVAILABLE_EMPTY | 1 |
| GATED | 14 |
| RATE_LIMIT | 0 |
| ERROR | 1 |
| NOT_FOUND | 20 |

## Dettaglio

| Endpoint | Path | Class | code | msg | ms | sample keys |
|---|---|---|---|---|---:|---|
| `supported-coins` | `/api/futures/supported-coins` | **AVAILABLE** | 0 |  | 1104 | — |
| `supported-exchange-pairs` | `/api/futures/supported-exchange-pairs` | **AVAILABLE** | 0 |  | 1958 | ApeX Omni, Aster, Binance, BingX, Bitfinex, Bitget |
| `coins-markets` | `/api/futures/coins-markets` | **GATED** | 401 | Upgrade plan | 416 | — |
| `open-interest-history-1h` | `/api/futures/open-interest/history` | **AVAILABLE** | 0 |  | 573 | close, high, low, open, time |
| `funding-rate-history` | `/api/futures/funding-rate/history` | **AVAILABLE** | 0 |  | 437 | close, high, low, open, time |
| `liquidation-aggregated-history` | `/api/futures/liquidation/aggregated-history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange_list' is not present | 482 | — |
| `global-long-short-account-ratio` | `/api/futures/global-long-short-account-ratio/history` | **AVAILABLE** | 0 |  | 806 | global_account_long_percent, global_account_long_short_ratio, global_account_short_percent, time |
| `cgdi-index-history` | `/api/futures/cgdi-index/history` | **AVAILABLE** | 0 |  | 998 | cgdi_index_value, time |
| `etf-bitcoin-list` | `/api/etf/bitcoin/list` | **AVAILABLE** | 0 |  | 712 | asset_details, aum_usd, cik_code, fund_name, fund_type, last_quote_time |
| `etf-bitcoin-flow-history` | `/api/etf/bitcoin/flow-history` | **AVAILABLE** | 0 |  | 1612 | etf_flows, flow_usd, price_usd, timestamp |
| `etf-bitcoin-net-assets-history` | `/api/etf/bitcoin/net-assets-history` | **NOT_FOUND** | — | HTTP 404 | 730 | — |
| `etf-bitcoin-premium-discount-history` | `/api/etf/bitcoin/premium-discount-history` | **NOT_FOUND** | — | HTTP 404 | 540 | — |
| `etf-ethereum-list` | `/api/etf/ethereum/list` | **AVAILABLE** | 0 |  | 720 | asset_details, aum_usd, fund_name, fund_type, last_quote_time, last_trade_time |
| `etf-hong-kong-bitcoin-flow-history` | `/api/etf/hong-kong-bitcoin/flow-history` | **NOT_FOUND** | — | HTTP 404 | 564 | — |
| `futures-rsi-list` | `/api/futures/rsi/list` | **GATED** | 401 | Upgrade plan | 752 | — |
| `orderbook-heatmap` | `/api/futures/orderbook/heatmap` | **NOT_FOUND** | — | HTTP 404 | 599 | — |
| `orderbook-large-limit-order` | `/api/futures/orderbook/large-limit-order` | **GATED** | 401 | Upgrade plan | 696 | — |
| `orderbook-large-limit-order-history` | `/api/futures/orderbook/large-limit-order-history` | **GATED** | 401 | Upgrade plan | 615 | — |
| `footprint` | `/api/futures/footprint` | **NOT_FOUND** | — | HTTP 404 | 684 | — |
| `liquidation-heatmap-model1-1y` | `/api/futures/liquidation/heatmap/model1` | **GATED** | 401 | Upgrade plan | 665 | — |
| `liquidation-heatmap-model1-180d` | `/api/futures/liquidation/heatmap/model1` | **GATED** | 401 | Upgrade plan | 473 | — |
| `liquidation-heatmap-model2-180d` | `/api/futures/liquidation/heatmap/model2` | **GATED** | 401 | Upgrade plan | 642 | — |
| `liquidation-heatmap-model3-180d` | `/api/futures/liquidation/heatmap/model3` | **GATED** | 401 | Upgrade plan | 461 | — |
| `liquidation-aggregated-heatmap-model3` | `/api/futures/liquidation/aggregated-heatmap/model3` | **GATED** | 401 | Upgrade plan | 422 | — |
| `hyperliquid-whale-alert` | `/api/hyperliquid/whale-alert` | **GATED** | 401 | Upgrade plan | 513 | — |
| `hyperliquid-whale-position` | `/api/hyperliquid/whale-position` | **GATED** | 401 | Upgrade plan | 482 | — |
| `cvd-history` | `/api/futures/cvd/history` | **GATED** | 401 | Upgrade plan | 462 | — |
| `aggregated-cvd-history` | `/api/futures/aggregated-cvd/history` | **GATED** | 401 | Upgrade plan | 471 | — |
| `taker-buy-sell-volume-history` | `/api/futures/taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 617 | taker_buy_volume_usd, taker_sell_volume_usd, time |
| `taker-buy-sell-volume-history-v2` | `/api/futures/v2/taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 787 | taker_buy_volume_usd, taker_sell_volume_usd, time |
| `aggregated-taker-buy-sell-volume` | `/api/futures/aggregated-taker-buy-sell-volume/history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange_list' is not present | 586 | — |
| `option-info` | `/api/option/info` | **AVAILABLE** | 0 |  | 683 | exchange_name, oi_market_share, open_interest, open_interest_change_24h, open_interest_usd, volume_change_percent_24h |
| `option-max-pain` | `/api/option/max-pain` | **AVAILABLE** | 0 |  | 509 | call_open_interest, call_open_interest_market_value, call_open_interest_notional, date, max_pain_price, put_open_interest |
| `option-exchange-oi-history` | `/api/option/exchange-oi-history` | **BAD_PARAMS** | 400 | Required String parameter 'range' is not present | 519 | — |
| `coinbase-premium-index` | `/api/coinbase-premium-index` | **AVAILABLE** | 0 | success | 540 | coinbase_price, premium, premium_rate, time |
| `fear-greed-history` | `/api/index/fear-greed-history` | **AVAILABLE** | 0 |  | 1119 | data_list, price_list, time_list |
| `stable-coin-marketcap-history` | `/api/index/stableCoin-marketCap-history` | **AVAILABLE** | 0 |  | 1692 | data_list, price_list, time_list |
| `exchange-balance-list` | `/api/exchange/balance/list` | **AVAILABLE** | 0 |  | 428 | balance_change_1d, balance_change_30d, balance_change_7d, balance_change_percent_1d, balance_change_percent_30d, balance_change_percent_7d |
| `index-ahr999` | `/api/index/ahr999` | **AVAILABLE** | 0 |  | 2347 | ahr999_value, average_price, current_value, date_string |
| `index-puell-multiple` | `/api/index/puell_multiple` | **NOT_FOUND** | — | HTTP 404 | 849 | — |
| `index-golden-ratio-multiplier` | `/api/index/golden_ratio_multiplier` | **NOT_FOUND** | — | HTTP 404 | 536 | — |
| `index-pi-cycle` | `/api/index/pi` | **NOT_FOUND** | — | HTTP 404 | 470 | — |
| `index-stock-flow` | `/api/index/stock_flow` | **NOT_FOUND** | — | HTTP 404 | 757 | — |
| `index-bitcoin-rainbow` | `/api/index/bitcoin/rainbow-chart` | **AVAILABLE** | 0 |  | 1974 | — |
| `index-bitcoin-bubble-index` | `/api/index/bitcoin_bubble_index` | **NOT_FOUND** | — | HTTP 404 | 840 | — |
| `user-account-subscription` | `/api/user/account/subscription` | **AVAILABLE** | 0 |  | 697 | expire_time, expired, level |
| `futures-pairs-markets` | `/api/futures/pairs-markets` | **AVAILABLE_EMPTY** | 0 |  | 818 | — |
| `futures-price-ohlc-history` | `/api/futures/price/history` | **AVAILABLE** | 0 |  | 438 | close, high, low, open, time, volume_usd |
| `futures-exchange-rank` | `/api/futures/exchange-rank` | **AVAILABLE** | 0 |  | 483 | exchange, liquidation_usd_24h, open_interest_usd, volume_usd |
| `futures-delisted-pairs` | `/api/futures/delisted-pairs` | **NOT_FOUND** | — | HTTP 404 | 449 | — |
| `futures-supported-exchanges` | `/api/futures/supported-exchanges` | **AVAILABLE** | 0 |  | 500 | — |
| `futures-funding-rate-oi-weight` | `/api/futures/funding-rate/oi-weight-ohlc-history` | **NOT_FOUND** | — | HTTP 404 | 526 | — |
| `futures-funding-rate-vol-weight` | `/api/futures/funding-rate/vol-weight-ohlc-history` | **NOT_FOUND** | — | HTTP 404 | 673 | — |
| `futures-funding-rate-cumulative` | `/api/futures/funding-rate/accumulated-exchange-list` | **BAD_PARAMS** | 400 | Required String parameter 'range' is not present | 641 | — |
| `futures-top-long-short-account-ratio` | `/api/futures/top-long-short-account-ratio/history` | **AVAILABLE** | 0 |  | 1063 | time, top_account_long_percent, top_account_long_short_ratio, top_account_short_percent |
| `futures-top-long-short-position-ratio` | `/api/futures/top-long-short-position-ratio/history` | **AVAILABLE** | 0 |  | 700 | time, top_position_long_percent, top_position_long_short_ratio, top_position_short_percent |
| `futures-coin-aggregated-orderbook` | `/api/futures/orderbook/aggregated-ask-bids-history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange_list' is not present | 864 | — |
| `futures-aggregated-taker-buy-sell-volume-fix` | `/api/futures/aggregated-taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 903 | aggregated_buy_volume_usd, aggregated_sell_volume_usd, time |
| `futures-liquidation-aggregated-history-fix` | `/api/futures/liquidation/aggregated-history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange_list' is not present | 620 | — |
| `spot-supported-coins` | `/api/spot/supported-coins` | **AVAILABLE** | 0 |  | 661 | — |
| `spot-supported-exchange-pairs` | `/api/spot/supported-exchange-pairs` | **AVAILABLE** | 0 |  | 1825 | Binance, Bitfinex, Bitget, Bybit, Coinbase, Crypto.com |
| `spot-pairs-markets` | `/api/spot/pairs-markets` | **ERROR** | 500 | Server Error | 826 | — |
| `spot-price-history` | `/api/spot/price/history` | **AVAILABLE** | 0 |  | 718 | close, high, low, open, time, volume_usd |
| `spot-orderbook-ask-bids` | `/api/spot/orderbook/ask-bids-history` | **AVAILABLE** | 0 |  | 695 | asks_quantity, asks_usd, bids_quantity, bids_usd, time |
| `spot-aggregated-orderbook` | `/api/spot/orderbook/aggregated-ask-bids-history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange_list' is not present | 519 | — |
| `spot-coin-taker-buy-sell-history` | `/api/spot/aggregated-taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 1363 | aggregated_buy_volume_usd, aggregated_sell_volume_usd, time |
| `spot-pair-taker-buy-sell-history` | `/api/spot/taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 445 | taker_buy_volume_usd, taker_sell_volume_usd, time |
| `option-info-fix` | `/api/option/info` | **AVAILABLE** | 0 |  | 712 | exchange_name, oi_market_share, open_interest, open_interest_change_24h, open_interest_usd, volume_change_percent_24h |
| `option-exchange-vol-history` | `/api/option/exchange-vol-history` | **AVAILABLE** | 0 | success | 1665 | data_map, price_list, time_list |
| `option-exchange-oi-history-fix` | `/api/option/exchange-oi-history` | **BAD_PARAMS** | 400 | Required String parameter 'range' is not present | 679 | — |
| `etf-bitcoin-net-assets-fix` | `/api/etf/bitcoin/net-assets/history` | **AVAILABLE** | 0 |  | 918 | change_usd, net_assets_usd, price_usd, timestamp |
| `etf-bitcoin-premium-discount-fix` | `/api/etf/bitcoin/premium-discount-history` | **NOT_FOUND** | — | HTTP 404 | 748 | — |
| `etf-bitcoin-history` | `/api/etf/bitcoin/history` | **AVAILABLE** | 0 |  | 1131 | assets_date, btc_holdings, market_date, market_price, name, nav |
| `etf-bitcoin-price-history` | `/api/etf/bitcoin/price/history` | **BAD_PARAMS** | 400 | Required String parameter 'range' is not present | 474 | — |
| `etf-bitcoin-detail` | `/api/etf/bitcoin/detail` | **AVAILABLE** | 0 |  | 476 | last_quote, last_trade, market_status, name, performance, session |
| `etf-hk-bitcoin-flow-fix` | `/api/hk-etf/bitcoin/flow-history` | **AVAILABLE** | 0 |  | 1133 | etf_flows, flow_usd, price_usd, timestamp |
| `etf-ethereum-flow-history` | `/api/etf/ethereum/flow-history` | **AVAILABLE** | 0 |  | 1564 | etf_flows, flow_usd, price_usd, timestamp |
| `etf-ethereum-net-assets` | `/api/etf/ethereum/net-assets/history` | **AVAILABLE** | 0 |  | 1733 | change_usd, net_assets_usd, price_usd, timestamp |
| `etf-grayscale-holdings` | `/api/grayscale/holdings-list` | **AVAILABLE** | 0 |  | 755 | close_time, holdings_amount, holdings_amount_change1d, holdings_amount_change_30d, holdings_amount_change_7d, holdings_usd |
| `etf-solana-flow-history` | `/api/sol-etf/flow-history` | **NOT_FOUND** | — | HTTP 404 | 742 | — |
| `etf-xrp-flow-history` | `/api/xrp-etf/flow-history` | **NOT_FOUND** | — | HTTP 404 | 728 | — |
| `exchange-assets` | `/api/exchange/assets` | **AVAILABLE** | 0 | success | 851 | assets_name, balance, balance_usd, price, symbol, wallet_address |
| `exchange-balance-chart` | `/api/exchange/balance/chart` | **AVAILABLE** | 0 |  | 1310 | data_map, price_list, time_list |
| `exchange-onchain-transfers-erc20` | `/api/exchange/chain/tx/list` | **AVAILABLE** | 0 |  | 1136 | amount_usd, asset_quantity, asset_symbol, exchange_name, from_address, to_address |
| `indic-futures-basis` | `/api/futures/basis/history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange' is not present | 450 | — |
| `indic-puell-multiple-fix` | `/api/index/puell-multiple` | **AVAILABLE** | 0 |  | 1884 | price, puell_multiple, timestamp |
| `indic-golden-ratio-fix` | `/api/index/golden-ratio-multiplier` | **AVAILABLE** | 0 |  | 3010 | accumulation_high_1_6, low_bull_high_2, ma_350, price, timestamp, x_13 |
| `indic-pi-cycle-fix` | `/api/index/pi-cycle-indicator` | **AVAILABLE** | 0 |  | 2493 | ma_110, ma_350_mu_2, price, timestamp |
| `indic-stock-flow-fix` | `/api/index/stock-flow` | **AVAILABLE** | 0 |  | 1744 | next_halving, price, timestamp |
| `indic-bitcoin-bubble-fix` | `/api/index/bitcoin/bubble-index` | **AVAILABLE** | 0 |  | 2541 | address_send_count, bubble_index, date_string, mining_difficulty, price, transaction_count |
| `indic-bitcoin-profitable-days` | `/api/index/bitcoin/profitable-days` | **AVAILABLE** | 0 |  | 1683 | price, side, timestamp |
| `indic-bull-market-peak` | `/api/index/bull-market-peak-indicators` | **NOT_FOUND** | — | HTTP 404 | 535 | — |
| `indic-2y-ma-multiplier` | `/api/index/two-year-ma-multiplier` | **NOT_FOUND** | — | HTTP 404 | 716 | — |
| `indic-200w-ma-heatmap` | `/api/index/200-week-moving-avg-heatmap` | **NOT_FOUND** | — | HTTP 404 | 739 | — |
| `indic-cdri-index` | `/api/futures/cdri-index/history` | **AVAILABLE** | 0 |  | 974 | cdri_index_value, time |
| `indic-bitfinex-margin-long-short` | `/api/bitfinex-margin-long-short` | **AVAILABLE** | 0 |  | 528 | long_quantity, short_quantity, time |
| `indic-borrow-interest-rate` | `/api/borrow-interest-rate/history` | **BAD_PARAMS** | 400 | Required String parameter 'interval' is not present | 710 | — |
| `other-economic-calendar` | `/api/calendar/economic-data` | **GATED** | 401 | Upgrade plan | 570 | — |
| `other-news-list` | `/api/news` | **NOT_FOUND** | — | HTTP 404 | 633 | — |

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
- `other-economic-calendar` → Upgrade plan

## Endpoint ERROR / NOT_FOUND

Path da rivedere: refuso editoriale o cambio di nome non documentato.

- `spot-pairs-markets` (/api/spot/pairs-markets): HTTP 200 code=500 msg=Server Error
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
- `futures-delisted-pairs` (/api/futures/delisted-pairs): HTTP 404 code=None msg=HTTP 404
- `futures-funding-rate-oi-weight` (/api/futures/funding-rate/oi-weight-ohlc-history): HTTP 404 code=None msg=HTTP 404
- `futures-funding-rate-vol-weight` (/api/futures/funding-rate/vol-weight-ohlc-history): HTTP 404 code=None msg=HTTP 404
- `etf-bitcoin-premium-discount-fix` (/api/etf/bitcoin/premium-discount-history): HTTP 404 code=None msg=HTTP 404
- `etf-solana-flow-history` (/api/sol-etf/flow-history): HTTP 404 code=None msg=HTTP 404
- `etf-xrp-flow-history` (/api/xrp-etf/flow-history): HTTP 404 code=None msg=HTTP 404
- `indic-bull-market-peak` (/api/index/bull-market-peak-indicators): HTTP 404 code=None msg=HTTP 404
- `indic-2y-ma-multiplier` (/api/index/two-year-ma-multiplier): HTTP 404 code=None msg=HTTP 404
- `indic-200w-ma-heatmap` (/api/index/200-week-moving-avg-heatmap): HTTP 404 code=None msg=HTTP 404
- `other-news-list` (/api/news): HTTP 404 code=None msg=HTTP 404
