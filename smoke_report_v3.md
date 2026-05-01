# CoinGlass smoke-test report — Hobbyist plan

Run time: 2026-04-30 19:08:19 UTC
Base URL: `https://open-api-v4.coinglass.com`
Probes: **99**, rate ~24 rpm

## Sintesi per classificazione

| Classe | Conteggio |
|---|---:|
| AVAILABLE | 77 |
| AVAILABLE_EMPTY | 1 |
| GATED | 17 |
| RATE_LIMIT | 0 |
| ERROR | 2 |
| NOT_FOUND | 0 |

## Dettaglio

| Endpoint | Path | Class | code | msg | ms | sample keys |
|---|---|---|---|---|---:|---|
| `supported-coins` | `/api/futures/supported-coins` | **AVAILABLE** | 0 |  | 617 | — |
| `supported-exchange-pairs` | `/api/futures/supported-exchange-pairs` | **AVAILABLE** | 0 |  | 3482 | ApeX Omni, Aster, Binance, BingX, Bitfinex, Bitget |
| `coins-markets` | `/api/futures/coins-markets` | **GATED** | 401 | Upgrade plan | 741 | — |
| `open-interest-history-1h` | `/api/futures/open-interest/history` | **AVAILABLE** | 0 |  | 703 | close, high, low, open, time |
| `funding-rate-history` | `/api/futures/funding-rate/history` | **AVAILABLE** | 0 |  | 552 | close, high, low, open, time |
| `liquidation-aggregated-history` | `/api/futures/liquidation/aggregated-history` | **AVAILABLE** | 0 |  | 779 | aggregated_long_liquidation_usd, aggregated_short_liquidation_usd, time |
| `global-long-short-account-ratio` | `/api/futures/global-long-short-account-ratio/history` | **AVAILABLE** | 0 |  | 896 | global_account_long_percent, global_account_long_short_ratio, global_account_short_percent, time |
| `cgdi-index-history` | `/api/futures/cgdi-index/history` | **AVAILABLE** | 0 |  | 1299 | cgdi_index_value, time |
| `etf-bitcoin-list` | `/api/etf/bitcoin/list` | **AVAILABLE** | 0 |  | 922 | asset_details, aum_usd, cik_code, fund_name, fund_type, last_quote_time |
| `etf-bitcoin-flow-history` | `/api/etf/bitcoin/flow-history` | **AVAILABLE** | 0 |  | 1581 | etf_flows, flow_usd, price_usd, timestamp |
| `etf-bitcoin-net-assets-history` | `/api/etf/bitcoin/net-assets/history` | **AVAILABLE** | 0 |  | 990 | change_usd, net_assets_usd, price_usd, timestamp |
| `etf-bitcoin-premium-discount-history` | `/api/etf/bitcoin/premium-discount/history` | **AVAILABLE** | 0 |  | 1918 | list, timestamp |
| `etf-ethereum-list` | `/api/etf/ethereum/list` | **AVAILABLE** | 0 |  | 577 | asset_details, aum_usd, fund_name, fund_type, last_quote_time, last_trade_time |
| `etf-hong-kong-bitcoin-flow-history` | `/api/hk-etf/bitcoin/flow-history` | **AVAILABLE** | 0 |  | 1630 | etf_flows, flow_usd, price_usd, timestamp |
| `futures-rsi-list` | `/api/futures/rsi/list` | **GATED** | 401 | Upgrade plan | 1048 | — |
| `orderbook-history` | `/api/futures/orderbook/history` | **GATED** | 401 | Upgrade plan | 498 | — |
| `orderbook-large-limit-order` | `/api/futures/orderbook/large-limit-order` | **GATED** | 401 | Upgrade plan | 529 | — |
| `orderbook-large-limit-order-history` | `/api/futures/orderbook/large-limit-order-history` | **GATED** | 401 | Upgrade plan | 729 | — |
| `footprint` | `/api/futures/volume/footprint-history` | **GATED** | 401 | Upgrade plan | 549 | — |
| `liquidation-heatmap-model1-1y` | `/api/futures/liquidation/heatmap/model1` | **GATED** | 401 | Upgrade plan | 772 | — |
| `liquidation-heatmap-model1-180d` | `/api/futures/liquidation/heatmap/model1` | **GATED** | 401 | Upgrade plan | 853 | — |
| `liquidation-heatmap-model2-180d` | `/api/futures/liquidation/heatmap/model2` | **GATED** | 401 | Upgrade plan | 723 | — |
| `liquidation-heatmap-model3-180d` | `/api/futures/liquidation/heatmap/model3` | **GATED** | 401 | Upgrade plan | 1009 | — |
| `liquidation-aggregated-heatmap-model3` | `/api/futures/liquidation/aggregated-heatmap/model3` | **GATED** | 401 | Upgrade plan | 610 | — |
| `hyperliquid-whale-alert` | `/api/hyperliquid/whale-alert` | **GATED** | 401 | Upgrade plan | 1771 | — |
| `hyperliquid-whale-position` | `/api/hyperliquid/whale-position` | **GATED** | 401 | Upgrade plan | 510 | — |
| `cvd-history` | `/api/futures/cvd/history` | **GATED** | 401 | Upgrade plan | 573 | — |
| `aggregated-cvd-history` | `/api/futures/aggregated-cvd/history` | **GATED** | 401 | Upgrade plan | 775 | — |
| `taker-buy-sell-volume-history` | `/api/futures/taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 545 | taker_buy_volume_usd, taker_sell_volume_usd, time |
| `taker-buy-sell-volume-history-v2` | `/api/futures/v2/taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 980 | taker_buy_volume_usd, taker_sell_volume_usd, time |
| `aggregated-taker-buy-sell-volume` | `/api/futures/aggregated-taker-buy-sell-volume/history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange_list' is not present | 482 | — |
| `option-info` | `/api/option/info` | **AVAILABLE** | 0 |  | 522 | exchange_name, oi_market_share, open_interest, open_interest_change_24h, open_interest_usd, volume_change_percent_24h |
| `option-max-pain` | `/api/option/max-pain` | **AVAILABLE** | 0 |  | 532 | call_open_interest, call_open_interest_market_value, call_open_interest_notional, date, max_pain_price, put_open_interest |
| `option-exchange-oi-history` | `/api/option/exchange-oi-history` | **AVAILABLE** | 0 |  | 1672 | data_map, price_list, time_list |
| `coinbase-premium-index` | `/api/coinbase-premium-index` | **AVAILABLE** | 0 | success | 623 | coinbase_price, premium, premium_rate, time |
| `fear-greed-history` | `/api/index/fear-greed-history` | **AVAILABLE** | 0 |  | 1227 | data_list, price_list, time_list |
| `stable-coin-marketcap-history` | `/api/index/stableCoin-marketCap-history` | **AVAILABLE** | 0 |  | 1454 | data_list, price_list, time_list |
| `exchange-balance-list` | `/api/exchange/balance/list` | **AVAILABLE** | 0 |  | 496 | balance_change_1d, balance_change_30d, balance_change_7d, balance_change_percent_1d, balance_change_percent_30d, balance_change_percent_7d |
| `index-ahr999` | `/api/index/ahr999` | **AVAILABLE** | 0 |  | 1837 | ahr999_value, average_price, current_value, date_string |
| `index-puell-multiple` | `/api/index/puell-multiple` | **AVAILABLE** | 0 |  | 1851 | price, puell_multiple, timestamp |
| `index-golden-ratio-multiplier` | `/api/index/golden-ratio-multiplier` | **AVAILABLE** | 0 |  | 3035 | accumulation_high_1_6, low_bull_high_2, ma_350, price, timestamp, x_13 |
| `index-pi-cycle` | `/api/index/pi-cycle-indicator` | **AVAILABLE** | 0 |  | 2294 | ma_110, ma_350_mu_2, price, timestamp |
| `index-stock-flow` | `/api/index/stock-flow` | **AVAILABLE** | 0 |  | 1786 | next_halving, price, timestamp |
| `index-bitcoin-rainbow` | `/api/index/bitcoin/rainbow-chart` | **AVAILABLE** | 0 |  | 2499 | — |
| `index-bitcoin-bubble-index` | `/api/index/bitcoin/bubble-index` | **AVAILABLE** | 0 |  | 1827 | address_send_count, bubble_index, date_string, mining_difficulty, price, transaction_count |
| `user-account-subscription` | `/api/user/account/subscription` | **AVAILABLE** | 0 |  | 461 | expire_time, expired, level |
| `futures-pairs-markets` | `/api/futures/pairs-markets` | **AVAILABLE_EMPTY** | 0 |  | 528 | — |
| `futures-price-ohlc-history` | `/api/futures/price/history` | **AVAILABLE** | 0 |  | 501 | close, high, low, open, time, volume_usd |
| `futures-exchange-rank` | `/api/futures/exchange-rank` | **AVAILABLE** | 0 |  | 864 | exchange, liquidation_usd_24h, open_interest_usd, volume_usd |
| `futures-delisted-pairs` | `/api/futures/delisted-exchange-pairs` | **AVAILABLE** | 0 |  | 1181 | ApeX Omni, Aster, Binance, BingX, Bitfinex, Bitget |
| `futures-supported-exchanges` | `/api/futures/supported-exchanges` | **AVAILABLE** | 0 |  | 763 | — |
| `futures-funding-rate-oi-weight` | `/api/futures/funding-rate/oi-weight-history` | **AVAILABLE** | 0 |  | 513 | close, high, low, open, time |
| `futures-funding-rate-vol-weight` | `/api/futures/funding-rate/vol-weight-history` | **AVAILABLE** | 0 |  | 538 | close, high, low, open, time |
| `futures-funding-rate-cumulative` | `/api/futures/funding-rate/accumulated-exchange-list` | **AVAILABLE** | 0 |  | 2199 | stablecoin_margin_list, symbol, token_margin_list |
| `futures-top-long-short-account-ratio` | `/api/futures/top-long-short-account-ratio/history` | **AVAILABLE** | 0 |  | 494 | time, top_account_long_percent, top_account_long_short_ratio, top_account_short_percent |
| `futures-top-long-short-position-ratio` | `/api/futures/top-long-short-position-ratio/history` | **AVAILABLE** | 0 |  | 790 | time, top_position_long_percent, top_position_long_short_ratio, top_position_short_percent |
| `futures-coin-aggregated-orderbook` | `/api/futures/orderbook/aggregated-ask-bids-history` | **AVAILABLE** | 0 |  | 1464 | aggregated_asks_quantity, aggregated_asks_usd, aggregated_bids_quantity, aggregated_bids_usd, time |
| `futures-aggregated-taker-buy-sell-volume-fix` | `/api/futures/aggregated-taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 979 | aggregated_buy_volume_usd, aggregated_sell_volume_usd, time |
| `futures-liquidation-aggregated-history-fix` | `/api/futures/liquidation/aggregated-history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange_list' is not present | 541 | — |
| `spot-supported-coins` | `/api/spot/supported-coins` | **AVAILABLE** | 0 |  | 954 | — |
| `spot-supported-exchange-pairs` | `/api/spot/supported-exchange-pairs` | **AVAILABLE** | 0 |  | 1806 | Binance, Bitfinex, Bitget, Bybit, Coinbase, Crypto.com |
| `spot-pairs-markets` | `/api/spot/pairs-markets` | **ERROR** | 500 | Server Error | 486 | — |
| `spot-price-history` | `/api/spot/price/history` | **AVAILABLE** | 0 |  | 778 | close, high, low, open, time, volume_usd |
| `spot-orderbook-ask-bids` | `/api/spot/orderbook/ask-bids-history` | **AVAILABLE** | 0 |  | 737 | asks_quantity, asks_usd, bids_quantity, bids_usd, time |
| `spot-aggregated-orderbook` | `/api/spot/orderbook/aggregated-ask-bids-history` | **AVAILABLE** | 0 |  | 1036 | aggregated_asks_quantity, aggregated_asks_usd, aggregated_bids_quantity, aggregated_bids_usd, time |
| `spot-coin-taker-buy-sell-history` | `/api/spot/aggregated-taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 706 | aggregated_buy_volume_usd, aggregated_sell_volume_usd, time |
| `spot-pair-taker-buy-sell-history` | `/api/spot/taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 610 | taker_buy_volume_usd, taker_sell_volume_usd, time |
| `option-info-fix` | `/api/option/info` | **AVAILABLE** | 0 |  | 803 | exchange_name, oi_market_share, open_interest, open_interest_change_24h, open_interest_usd, volume_change_percent_24h |
| `option-exchange-vol-history` | `/api/option/exchange-vol-history` | **AVAILABLE** | 0 | success | 1536 | data_map, price_list, time_list |
| `option-exchange-oi-history-fix` | `/api/option/exchange-oi-history` | **AVAILABLE** | 0 |  | 964 | data_map, price_list, time_list |
| `etf-bitcoin-net-assets-fix` | `/api/etf/bitcoin/net-assets/history` | **AVAILABLE** | 0 |  | 892 | change_usd, net_assets_usd, price_usd, timestamp |
| `etf-bitcoin-premium-discount-fix` | `/api/etf/bitcoin/premium-discount/history` | **AVAILABLE** | 0 |  | 974 | market_price_usd, nav_usd, premium_discount_details, timestamp |
| `etf-bitcoin-history` | `/api/etf/bitcoin/history` | **AVAILABLE** | 0 |  | 1515 | assets_date, btc_holdings, market_date, market_price, name, nav |
| `etf-bitcoin-price-history` | `/api/etf/bitcoin/price/history` | **AVAILABLE** | 0 |  | 1673 | close, high, low, open, time, volume |
| `etf-bitcoin-detail` | `/api/etf/bitcoin/detail` | **AVAILABLE** | 0 |  | 707 | last_quote, last_trade, market_status, name, performance, session |
| `etf-hk-bitcoin-flow-fix` | `/api/hk-etf/bitcoin/flow-history` | **AVAILABLE** | 0 |  | 1147 | etf_flows, flow_usd, price_usd, timestamp |
| `etf-ethereum-flow-history` | `/api/etf/ethereum/flow-history` | **AVAILABLE** | 0 |  | 1493 | etf_flows, flow_usd, price_usd, timestamp |
| `etf-ethereum-net-assets` | `/api/etf/ethereum/net-assets/history` | **AVAILABLE** | 0 |  | 1763 | change_usd, net_assets_usd, price_usd, timestamp |
| `etf-grayscale-holdings` | `/api/grayscale/holdings-list` | **AVAILABLE** | 0 |  | 720 | close_time, holdings_amount, holdings_amount_change1d, holdings_amount_change_30d, holdings_amount_change_7d, holdings_usd |
| `etf-solana-flow-history` | `/api/etf/solana/flow-history` | **AVAILABLE** | 0 |  | 498 | etf_flows, flow_usd, price_usd, timestamp |
| `etf-xrp-flow-history` | `/api/etf/xrp/flow-history` | **AVAILABLE** | 0 |  | 719 | etf_flows, flow_usd, price_usd, timestamp |
| `exchange-assets` | `/api/exchange/assets` | **AVAILABLE** | 0 | success | 700 | assets_name, balance, balance_usd, price, symbol, wallet_address |
| `exchange-balance-chart` | `/api/exchange/balance/chart` | **AVAILABLE** | 0 |  | 1306 | data_map, price_list, time_list |
| `exchange-onchain-transfers-erc20` | `/api/exchange/chain/tx/list` | **AVAILABLE** | 0 |  | 798 | amount_usd, asset_quantity, asset_symbol, exchange_name, from_address, to_address |
| `indic-futures-basis` | `/api/futures/basis/history` | **ERROR** | 500 | Server Error | 566 | — |
| `indic-puell-multiple-fix` | `/api/index/puell-multiple` | **AVAILABLE** | 0 |  | 1648 | price, puell_multiple, timestamp |
| `indic-golden-ratio-fix` | `/api/index/golden-ratio-multiplier` | **AVAILABLE** | 0 |  | 2092 | accumulation_high_1_6, low_bull_high_2, ma_350, price, timestamp, x_13 |
| `indic-pi-cycle-fix` | `/api/index/pi-cycle-indicator` | **AVAILABLE** | 0 |  | 2006 | ma_110, ma_350_mu_2, price, timestamp |
| `indic-stock-flow-fix` | `/api/index/stock-flow` | **AVAILABLE** | 0 |  | 1649 | next_halving, price, timestamp |
| `indic-bitcoin-bubble-fix` | `/api/index/bitcoin/bubble-index` | **AVAILABLE** | 0 |  | 1855 | address_send_count, bubble_index, date_string, mining_difficulty, price, transaction_count |
| `indic-bitcoin-profitable-days` | `/api/index/bitcoin/profitable-days` | **AVAILABLE** | 0 |  | 1609 | price, side, timestamp |
| `indic-bull-market-peak` | `/api/bull-market-peak-indicator` | **AVAILABLE** | 0 | success | 522 | change_value, comparison_type, current_value, hit_status, indicator_name, previous_value |
| `indic-2y-ma-multiplier` | `/api/index/2-year-ma-multiplier` | **AVAILABLE** | 0 |  | 2345 | moving_average_730, moving_average_730_multiplier_5, price, timestamp |
| `indic-200w-ma-heatmap` | `/api/index/200-week-moving-average-heatmap` | **AVAILABLE** | 0 |  | 2127 | moving_average_1440, moving_average_1440_ip, price, timestamp |
| `indic-cdri-index` | `/api/futures/cdri-index/history` | **AVAILABLE** | 0 |  | 1035 | cdri_index_value, time |
| `indic-bitfinex-margin-long-short` | `/api/bitfinex-margin-long-short` | **AVAILABLE** | 0 |  | 532 | long_quantity, short_quantity, time |
| `indic-borrow-interest-rate` | `/api/borrow-interest-rate/history` | **AVAILABLE** | 0 |  | 631 | interest_rate, time |
| `other-economic-calendar` | `/api/calendar/economic-data` | **GATED** | 401 | Upgrade plan | 1388 | — |
| `other-news-list` | `/api/article/list` | **GATED** | 401 | Upgrade plan | 844 | — |

## Endpoint GATED (richiedono upgrade)

Su Hobbyist NON disponibili. Per ognuno: vedere INTEGRATION-NOTES.md §5 per il sostituto locale.

- `coins-markets` → Upgrade plan
- `futures-rsi-list` → Upgrade plan
- `orderbook-history` → Upgrade plan
- `orderbook-large-limit-order` → Upgrade plan
- `orderbook-large-limit-order-history` → Upgrade plan
- `footprint` → Upgrade plan
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
- `other-news-list` → Upgrade plan

## Endpoint ERROR / NOT_FOUND

Path da rivedere: refuso editoriale o cambio di nome non documentato.

- `spot-pairs-markets` (/api/spot/pairs-markets): HTTP 200 code=500 msg=Server Error
- `indic-futures-basis` (/api/futures/basis/history): HTTP 200 code=500 msg=Server Error
