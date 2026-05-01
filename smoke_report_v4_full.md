# CoinGlass smoke-test report — Hobbyist plan

Run time: 2026-04-30 19:52:51 UTC
Base URL: `https://open-api-v4.coinglass.com`
Probes: **164**, rate ~24 rpm

## Sintesi per classificazione

| Classe | Conteggio |
|---|---:|
| AVAILABLE | 81 |
| AVAILABLE_EMPTY | 1 |
| GATED | 74 |
| RATE_LIMIT | 0 |
| ERROR | 2 |
| NOT_FOUND | 1 |

## Dettaglio

| Endpoint | Path | Class | code | msg | ms | sample keys |
|---|---|---|---|---|---:|---|
| `supported-coins` | `/api/futures/supported-coins` | **AVAILABLE** | 0 |  | 1078 | — |
| `supported-exchange-pairs` | `/api/futures/supported-exchange-pairs` | **AVAILABLE** | 0 |  | 1813 | ApeX Omni, Aster, Binance, BingX, Bitfinex, Bitget |
| `coins-markets` | `/api/futures/coins-markets` | **GATED** | 401 | Upgrade plan | 681 | — |
| `open-interest-history-1h` | `/api/futures/open-interest/history` | **AVAILABLE** | 0 |  | 557 | close, high, low, open, time |
| `funding-rate-history` | `/api/futures/funding-rate/history` | **AVAILABLE** | 0 |  | 447 | close, high, low, open, time |
| `liquidation-aggregated-history` | `/api/futures/liquidation/aggregated-history` | **AVAILABLE** | 0 |  | 540 | aggregated_long_liquidation_usd, aggregated_short_liquidation_usd, time |
| `global-long-short-account-ratio` | `/api/futures/global-long-short-account-ratio/history` | **AVAILABLE** | 0 |  | 770 | global_account_long_percent, global_account_long_short_ratio, global_account_short_percent, time |
| `cgdi-index-history` | `/api/futures/cgdi-index/history` | **AVAILABLE** | 0 |  | 897 | cgdi_index_value, time |
| `etf-bitcoin-list` | `/api/etf/bitcoin/list` | **AVAILABLE** | 0 |  | 780 | asset_details, aum_usd, cik_code, fund_name, fund_type, last_quote_time |
| `etf-bitcoin-flow-history` | `/api/etf/bitcoin/flow-history` | **AVAILABLE** | 0 |  | 1475 | etf_flows, flow_usd, price_usd, timestamp |
| `etf-bitcoin-net-assets-history` | `/api/etf/bitcoin/net-assets/history` | **AVAILABLE** | 0 |  | 889 | change_usd, net_assets_usd, price_usd, timestamp |
| `etf-bitcoin-premium-discount-history` | `/api/etf/bitcoin/premium-discount/history` | **AVAILABLE** | 0 |  | 1744 | list, timestamp |
| `etf-ethereum-list` | `/api/etf/ethereum/list` | **AVAILABLE** | 0 |  | 546 | asset_details, aum_usd, fund_name, fund_type, last_quote_time, last_trade_time |
| `etf-hong-kong-bitcoin-flow-history` | `/api/hk-etf/bitcoin/flow-history` | **AVAILABLE** | 0 |  | 1175 | etf_flows, flow_usd, price_usd, timestamp |
| `futures-rsi-list` | `/api/futures/rsi/list` | **GATED** | 401 | Upgrade plan | 622 | — |
| `orderbook-history` | `/api/futures/orderbook/history` | **GATED** | 401 | Upgrade plan | 514 | — |
| `orderbook-large-limit-order` | `/api/futures/orderbook/large-limit-order` | **GATED** | 401 | Upgrade plan | 538 | — |
| `orderbook-large-limit-order-history` | `/api/futures/orderbook/large-limit-order-history` | **GATED** | 401 | Upgrade plan | 486 | — |
| `footprint` | `/api/futures/volume/footprint-history` | **GATED** | 401 | Upgrade plan | 504 | — |
| `liquidation-heatmap-model1-1y` | `/api/futures/liquidation/heatmap/model1` | **GATED** | 401 | Upgrade plan | 540 | — |
| `liquidation-heatmap-model1-180d` | `/api/futures/liquidation/heatmap/model1` | **GATED** | 401 | Upgrade plan | 552 | — |
| `liquidation-heatmap-model2-180d` | `/api/futures/liquidation/heatmap/model2` | **GATED** | 401 | Upgrade plan | 587 | — |
| `liquidation-heatmap-model3-180d` | `/api/futures/liquidation/heatmap/model3` | **GATED** | 401 | Upgrade plan | 416 | — |
| `liquidation-aggregated-heatmap-model3` | `/api/futures/liquidation/aggregated-heatmap/model3` | **GATED** | 401 | Upgrade plan | 660 | — |
| `hyperliquid-whale-alert` | `/api/hyperliquid/whale-alert` | **GATED** | 401 | Upgrade plan | 560 | — |
| `hyperliquid-whale-position` | `/api/hyperliquid/whale-position` | **GATED** | 401 | Upgrade plan | 516 | — |
| `cvd-history` | `/api/futures/cvd/history` | **GATED** | 401 | Upgrade plan | 511 | — |
| `aggregated-cvd-history` | `/api/futures/aggregated-cvd/history` | **GATED** | 401 | Upgrade plan | 470 | — |
| `taker-buy-sell-volume-history` | `/api/futures/taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 462 | taker_buy_volume_usd, taker_sell_volume_usd, time |
| `taker-buy-sell-volume-history-v2` | `/api/futures/v2/taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 536 | taker_buy_volume_usd, taker_sell_volume_usd, time |
| `aggregated-taker-buy-sell-volume` | `/api/futures/aggregated-taker-buy-sell-volume/history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange_list' is not present | 462 | — |
| `option-info` | `/api/option/info` | **AVAILABLE** | 0 |  | 547 | exchange_name, oi_market_share, open_interest, open_interest_change_24h, open_interest_usd, volume_change_percent_24h |
| `option-max-pain` | `/api/option/max-pain` | **AVAILABLE** | 0 |  | 583 | call_open_interest, call_open_interest_market_value, call_open_interest_notional, date, max_pain_price, put_open_interest |
| `option-exchange-oi-history` | `/api/option/exchange-oi-history` | **AVAILABLE** | 0 |  | 643 | data_map, price_list, time_list |
| `coinbase-premium-index` | `/api/coinbase-premium-index` | **AVAILABLE** | 0 | success | 547 | coinbase_price, premium, premium_rate, time |
| `fear-greed-history` | `/api/index/fear-greed-history` | **AVAILABLE** | 0 |  | 1258 | data_list, price_list, time_list |
| `stable-coin-marketcap-history` | `/api/index/stableCoin-marketCap-history` | **AVAILABLE** | 0 |  | 1409 | data_list, price_list, time_list |
| `exchange-balance-list` | `/api/exchange/balance/list` | **AVAILABLE** | 0 |  | 445 | balance_change_1d, balance_change_30d, balance_change_7d, balance_change_percent_1d, balance_change_percent_30d, balance_change_percent_7d |
| `index-ahr999` | `/api/index/ahr999` | **AVAILABLE** | 0 |  | 1680 | ahr999_value, average_price, current_value, date_string |
| `index-puell-multiple` | `/api/index/puell-multiple` | **AVAILABLE** | 0 |  | 1709 | price, puell_multiple, timestamp |
| `index-golden-ratio-multiplier` | `/api/index/golden-ratio-multiplier` | **AVAILABLE** | 0 |  | 1841 | accumulation_high_1_6, low_bull_high_2, ma_350, price, timestamp, x_13 |
| `index-pi-cycle` | `/api/index/pi-cycle-indicator` | **AVAILABLE** | 0 |  | 1564 | ma_110, ma_350_mu_2, price, timestamp |
| `index-stock-flow` | `/api/index/stock-flow` | **AVAILABLE** | 0 |  | 1603 | next_halving, price, timestamp |
| `index-bitcoin-rainbow` | `/api/index/bitcoin/rainbow-chart` | **AVAILABLE** | 0 |  | 1827 | — |
| `index-bitcoin-bubble-index` | `/api/index/bitcoin/bubble-index` | **AVAILABLE** | 0 |  | 1804 | address_send_count, bubble_index, date_string, mining_difficulty, price, transaction_count |
| `user-account-subscription` | `/api/user/account/subscription` | **AVAILABLE** | 0 |  | 449 | expire_time, expired, level |
| `futures-pairs-markets` | `/api/futures/pairs-markets` | **AVAILABLE_EMPTY** | 0 |  | 734 | — |
| `futures-price-ohlc-history` | `/api/futures/price/history` | **AVAILABLE** | 0 |  | 451 | close, high, low, open, time, volume_usd |
| `futures-exchange-rank` | `/api/futures/exchange-rank` | **AVAILABLE** | 0 |  | 481 | exchange, liquidation_usd_24h, open_interest_usd, volume_usd |
| `futures-delisted-pairs` | `/api/futures/delisted-exchange-pairs` | **AVAILABLE** | 0 |  | 1015 | ApeX Omni, Aster, Binance, BingX, Bitfinex, Bitget |
| `futures-supported-exchanges` | `/api/futures/supported-exchanges` | **AVAILABLE** | 0 |  | 406 | — |
| `futures-funding-rate-oi-weight` | `/api/futures/funding-rate/oi-weight-history` | **AVAILABLE** | 0 |  | 617 | close, high, low, open, time |
| `futures-funding-rate-vol-weight` | `/api/futures/funding-rate/vol-weight-history` | **AVAILABLE** | 0 |  | 465 | close, high, low, open, time |
| `futures-funding-rate-cumulative` | `/api/futures/funding-rate/accumulated-exchange-list` | **AVAILABLE** | 0 |  | 1927 | stablecoin_margin_list, symbol, token_margin_list |
| `futures-top-long-short-account-ratio` | `/api/futures/top-long-short-account-ratio/history` | **AVAILABLE** | 0 |  | 802 | time, top_account_long_percent, top_account_long_short_ratio, top_account_short_percent |
| `futures-top-long-short-position-ratio` | `/api/futures/top-long-short-position-ratio/history` | **AVAILABLE** | 0 |  | 661 | time, top_position_long_percent, top_position_long_short_ratio, top_position_short_percent |
| `futures-coin-aggregated-orderbook` | `/api/futures/orderbook/aggregated-ask-bids-history` | **AVAILABLE** | 0 |  | 980 | aggregated_asks_quantity, aggregated_asks_usd, aggregated_bids_quantity, aggregated_bids_usd, time |
| `futures-aggregated-taker-buy-sell-volume-fix` | `/api/futures/aggregated-taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 572 | aggregated_buy_volume_usd, aggregated_sell_volume_usd, time |
| `futures-liquidation-aggregated-history-fix` | `/api/futures/liquidation/aggregated-history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange_list' is not present | 466 | — |
| `spot-supported-coins` | `/api/spot/supported-coins` | **AVAILABLE** | 0 |  | 666 | — |
| `spot-supported-exchange-pairs` | `/api/spot/supported-exchange-pairs` | **AVAILABLE** | 0 |  | 1533 | Binance, Bitfinex, Bitget, Bybit, Coinbase, Crypto.com |
| `spot-pairs-markets` | `/api/spot/pairs-markets` | **ERROR** | 500 | Server Error | 658 | — |
| `spot-price-history` | `/api/spot/price/history` | **AVAILABLE** | 0 |  | 643 | close, high, low, open, time, volume_usd |
| `spot-orderbook-ask-bids` | `/api/spot/orderbook/ask-bids-history` | **AVAILABLE** | 0 |  | 731 | asks_quantity, asks_usd, bids_quantity, bids_usd, time |
| `spot-aggregated-orderbook` | `/api/spot/orderbook/aggregated-ask-bids-history` | **AVAILABLE** | 0 |  | 825 | aggregated_asks_quantity, aggregated_asks_usd, aggregated_bids_quantity, aggregated_bids_usd, time |
| `spot-coin-taker-buy-sell-history` | `/api/spot/aggregated-taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 519 | aggregated_buy_volume_usd, aggregated_sell_volume_usd, time |
| `spot-pair-taker-buy-sell-history` | `/api/spot/taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 526 | taker_buy_volume_usd, taker_sell_volume_usd, time |
| `option-info-fix` | `/api/option/info` | **AVAILABLE** | 0 |  | 445 | exchange_name, oi_market_share, open_interest, open_interest_change_24h, open_interest_usd, volume_change_percent_24h |
| `option-exchange-vol-history` | `/api/option/exchange-vol-history` | **AVAILABLE** | 0 | success | 1368 | data_map, price_list, time_list |
| `option-exchange-oi-history-fix` | `/api/option/exchange-oi-history` | **AVAILABLE** | 0 |  | 437 | data_map, price_list, time_list |
| `etf-bitcoin-net-assets-fix` | `/api/etf/bitcoin/net-assets/history` | **AVAILABLE** | 0 |  | 894 | change_usd, net_assets_usd, price_usd, timestamp |
| `etf-bitcoin-premium-discount-fix` | `/api/etf/bitcoin/premium-discount/history` | **AVAILABLE** | 0 |  | 873 | market_price_usd, nav_usd, premium_discount_details, timestamp |
| `etf-bitcoin-history` | `/api/etf/bitcoin/history` | **AVAILABLE** | 0 |  | 1104 | assets_date, btc_holdings, market_date, market_price, name, nav |
| `etf-bitcoin-price-history` | `/api/etf/bitcoin/price/history` | **AVAILABLE** | 0 |  | 1462 | close, high, low, open, time, volume |
| `etf-bitcoin-detail` | `/api/etf/bitcoin/detail` | **AVAILABLE** | 0 |  | 687 | last_quote, last_trade, market_status, name, performance, session |
| `etf-hk-bitcoin-flow-fix` | `/api/hk-etf/bitcoin/flow-history` | **AVAILABLE** | 0 |  | 1208 | etf_flows, flow_usd, price_usd, timestamp |
| `etf-ethereum-flow-history` | `/api/etf/ethereum/flow-history` | **AVAILABLE** | 0 |  | 1333 | etf_flows, flow_usd, price_usd, timestamp |
| `etf-ethereum-net-assets` | `/api/etf/ethereum/net-assets/history` | **AVAILABLE** | 0 |  | 1869 | change_usd, net_assets_usd, price_usd, timestamp |
| `etf-grayscale-holdings` | `/api/grayscale/holdings-list` | **AVAILABLE** | 0 |  | 454 | close_time, holdings_amount, holdings_amount_change1d, holdings_amount_change_30d, holdings_amount_change_7d, holdings_usd |
| `etf-solana-flow-history` | `/api/etf/solana/flow-history` | **AVAILABLE** | 0 |  | 745 | etf_flows, flow_usd, price_usd, timestamp |
| `etf-xrp-flow-history` | `/api/etf/xrp/flow-history` | **AVAILABLE** | 0 |  | 747 | etf_flows, flow_usd, price_usd, timestamp |
| `exchange-assets` | `/api/exchange/assets` | **AVAILABLE** | 0 | success | 1015 | assets_name, balance, balance_usd, price, symbol, wallet_address |
| `exchange-balance-chart` | `/api/exchange/balance/chart` | **AVAILABLE** | 0 |  | 1176 | data_map, price_list, time_list |
| `exchange-onchain-transfers-erc20` | `/api/exchange/chain/tx/list` | **AVAILABLE** | 0 |  | 741 | amount_usd, asset_quantity, asset_symbol, exchange_name, from_address, to_address |
| `indic-futures-basis` | `/api/futures/basis/history` | **ERROR** | 500 | Server Error | 473 | — |
| `indic-puell-multiple-fix` | `/api/index/puell-multiple` | **AVAILABLE** | 0 |  | 1777 | price, puell_multiple, timestamp |
| `indic-golden-ratio-fix` | `/api/index/golden-ratio-multiplier` | **AVAILABLE** | 0 |  | 1877 | accumulation_high_1_6, low_bull_high_2, ma_350, price, timestamp, x_13 |
| `indic-pi-cycle-fix` | `/api/index/pi-cycle-indicator` | **AVAILABLE** | 0 |  | 1595 | ma_110, ma_350_mu_2, price, timestamp |
| `indic-stock-flow-fix` | `/api/index/stock-flow` | **AVAILABLE** | 0 |  | 1564 | next_halving, price, timestamp |
| `indic-bitcoin-bubble-fix` | `/api/index/bitcoin/bubble-index` | **AVAILABLE** | 0 |  | 2116 | address_send_count, bubble_index, date_string, mining_difficulty, price, transaction_count |
| `indic-bitcoin-profitable-days` | `/api/index/bitcoin/profitable-days` | **AVAILABLE** | 0 |  | 1427 | price, side, timestamp |
| `indic-bull-market-peak` | `/api/bull-market-peak-indicator` | **AVAILABLE** | 0 | success | 453 | change_value, comparison_type, current_value, hit_status, indicator_name, previous_value |
| `indic-2y-ma-multiplier` | `/api/index/2-year-ma-multiplier` | **AVAILABLE** | 0 |  | 1696 | moving_average_730, moving_average_730_multiplier_5, price, timestamp |
| `indic-200w-ma-heatmap` | `/api/index/200-week-moving-average-heatmap` | **AVAILABLE** | 0 |  | 1603 | moving_average_1440, moving_average_1440_ip, price, timestamp |
| `indic-cdri-index` | `/api/futures/cdri-index/history` | **AVAILABLE** | 0 |  | 1146 | cdri_index_value, time |
| `indic-bitfinex-margin-long-short` | `/api/bitfinex-margin-long-short` | **AVAILABLE** | 0 |  | 595 | long_quantity, short_quantity, time |
| `indic-borrow-interest-rate` | `/api/borrow-interest-rate/history` | **AVAILABLE** | 0 |  | 529 | interest_rate, time |
| `other-economic-calendar` | `/api/calendar/economic-data` | **GATED** | 401 | Upgrade plan | 549 | — |
| `other-news-list` | `/api/article/list` | **GATED** | 401 | Upgrade plan | 441 | — |
| `futures-coins-price-change` | `/api/futures/coins-price-change` | **GATED** | 401 | Upgrade plan | 523 | — |
| `oi-aggregated-history` | `/api/futures/open-interest/aggregated-history` | **AVAILABLE** | 0 |  | 1553 | close, high, low, open, time |
| `oi-aggregated-stablecoin-history` | `/api/futures/open-interest/aggregated-stablecoin-history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange_list' is not present | 674 | — |
| `oi-aggregated-coin-margin-history` | `/api/futures/open-interest/aggregated-coin-margin-history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange_list' is not present | 740 | — |
| `oi-exchange-history-chart` | `/api/futures/open-interest/exchange-history-chart` | **BAD_PARAMS** | 400 | Required String parameter 'range' is not present | 663 | — |
| `funding-rate-arbitrage` | `/api/futures/funding-rate/arbitrage` | **GATED** | 401 | Upgrade plan | 621 | — |
| `taker-buy-sell-exchange-list` | `/api/futures/taker-buy-sell-volume/exchange-list` | **AVAILABLE** | 0 | success | 835 | buy_ratio, buy_vol_usd, exchange_list, sell_ratio, sell_vol_usd, symbol |
| `net-position-history` | `/api/futures/net-position/history` | **GATED** | 401 | Upgrade plan | 507 | — |
| `net-position-v2-history` | `/api/futures/v2/net-position/history` | **GATED** | 401 | Upgrade plan | 772 | — |
| `liq-aggregated-heatmap-model1` | `/api/futures/liquidation/aggregated-heatmap/model1` | **GATED** | 401 | Upgrade plan | 551 | — |
| `liq-aggregated-heatmap-model2` | `/api/futures/liquidation/aggregated-heatmap/model2` | **GATED** | 401 | Upgrade plan | 742 | — |
| `liq-pair-map` | `/api/futures/liquidation/map` | **GATED** | 401 | Upgrade plan | 683 | — |
| `liq-aggregated-map` | `/api/futures/liquidation/aggregated-map` | **GATED** | 401 | Upgrade plan | 525 | — |
| `liq-max-pain` | `/api/futures/liquidation/max-pain` | **GATED** | 401 | Upgrade plan | 518 | — |
| `hyperliquid-position` | `/api/hyperliquid/position` | **GATED** | 401 | Upgrade plan | 530 | — |
| `hyperliquid-user-position` | `/api/hyperliquid/user-position` | **GATED** | 401 | Upgrade plan | 575 | — |
| `hyperliquid-wallet-pnl-dist` | `/api/hyperliquid/wallet/pnl-distribution` | **GATED** | 401 | Upgrade plan | 682 | — |
| `hyperliquid-global-l-s-account` | `/api/hyperliquid/global-long-short-account-ratio/history` | **GATED** | 401 | Upgrade plan | 556 | — |
| `futures-netflow-list` | `/api/futures/netflow-list` | **GATED** | 401 | Upgrade plan | 705 | — |
| `futures-coin-netflow-typo` | `/api/furures/coin/netflow` | **NOT_FOUND** | — | HTTP 404 | 665 | — |
| `futures-coin-netflow-fix` | `/api/futures/coin/netflow` | **GATED** | 401 | Upgrade plan | 529 | — |
| `spot-coins-markets` | `/api/spot/coins-markets` | **GATED** | 401 | Upgrade plan | 459 | — |
| `spot-orderbook-history` | `/api/spot/orderbook/history` | **GATED** | 401 | Upgrade plan | 711 | — |
| `spot-large-limit-order` | `/api/spot/orderbook/large-limit-order` | **GATED** | 401 | Upgrade plan | 468 | — |
| `spot-large-limit-order-history` | `/api/spot/orderbook/large-limit-order-history` | **GATED** | 401 | Upgrade plan | 758 | — |
| `spot-footprint` | `/api/spot/volume/footprint-history` | **GATED** | 401 | Upgrade plan | 744 | — |
| `spot-cvd-history` | `/api/spot/cvd/history` | **GATED** | 401 | Upgrade plan | 497 | — |
| `spot-aggregated-cvd` | `/api/spot/aggregated-cvd/history` | **GATED** | 401 | Upgrade plan | 544 | — |
| `spot-netflow-list` | `/api/spot/netflow-list` | **GATED** | 401 | Upgrade plan | 516 | — |
| `spot-coin-netflow` | `/api/spot/coin/netflow` | **GATED** | 401 | Upgrade plan | 772 | — |
| `onchain-exchange-assets-transparency` | `/api/exchange_assets_transparency/list` | **GATED** | 401 | Upgrade plan | 892 | — |
| `onchain-token-unlock-list` | `/api/coin/unlock-list` | **GATED** | 401 | Upgrade plan | 480 | — |
| `onchain-token-vesting` | `/api/coin/vesting` | **GATED** | 401 | Upgrade plan | 544 | — |
| `onchain-whale-transfer` | `/api/chain/v2/whale-transfer` | **GATED** | 401 | Upgrade plan | 514 | — |
| `etf-bitcoin-aum` | `/api/etf/bitcoin/aum` | **AVAILABLE** | 0 |  | 997 | aum_usd, time |
| `etf-grayscale-premium` | `/api/grayscale/premium-history` | **AVAILABLE** | 0 |  | 981 | premium_rate_list, primary_market_price, secondary_market_price_list, time_list |
| `indic-td-sequential` | `/api/futures/indicators/td` | **GATED** | 401 | Upgrade plan | 601 | — |
| `indic-coin-atr-list` | `/api/futures/avg-true-range/list` | **GATED** | 401 | Upgrade plan | 1672 | — |
| `indic-pair-atr` | `/api/futures/indicators/avg-true-range` | **GATED** | 401 | Upgrade plan | 512 | — |
| `indic-whale-index` | `/api/futures/whale-index/history` | **GATED** | 401 | Upgrade plan | 547 | — |
| `indic-ma-native` | `/api/futures/indicators/ma` | **GATED** | 401 | Upgrade plan | 635 | — |
| `indic-ema-native` | `/api/futures/indicators/ema` | **GATED** | 401 | Upgrade plan | 485 | — |
| `indic-rsi-native` | `/api/futures/indicators/rsi` | **GATED** | 401 | Upgrade plan | 681 | — |
| `indic-macd-native` | `/api/futures/indicators/macd` | **GATED** | 401 | Upgrade plan | 689 | — |
| `indic-boll-native` | `/api/futures/indicators/boll` | **GATED** | 401 | Upgrade plan | 484 | — |
| `indic-macd-list` | `/api/futures/macd/list` | **GATED** | 401 | Upgrade plan | 567 | — |
| `indic-bitcoin-sth-sopr` | `/api/index/bitcoin-sth-sopr` | **GATED** | 401 | Upgrade plan | 523 | — |
| `indic-bitcoin-lth-sopr` | `/api/index/bitcoin-lth-sopr` | **GATED** | 401 | Upgrade plan | 594 | — |
| `indic-bitcoin-sth-realized-price` | `/api/index/bitcoin-sth-realized-price` | **GATED** | 401 | Upgrade plan | 702 | — |
| `indic-bitcoin-lth-realized-price` | `/api/index/bitcoin-lth-realized-price` | **GATED** | 401 | Upgrade plan | 556 | — |
| `indic-bitcoin-rhodl-ratio` | `/api/index/bitcoin-rhodl-ratio` | **GATED** | 401 | Upgrade plan | 467 | — |
| `indic-bitcoin-sth-supply` | `/api/index/bitcoin-short-term-holder-supply` | **GATED** | 401 | Upgrade plan | 481 | — |
| `indic-bitcoin-lth-supply` | `/api/index/bitcoin-long-term-holder-supply` | **GATED** | 401 | Upgrade plan | 512 | — |
| `indic-bitcoin-new-addresses` | `/api/index/bitcoin-new-addresses` | **GATED** | 401 | Upgrade plan | 810 | — |
| `indic-bitcoin-active-addresses` | `/api/index/bitcoin-active-addresses` | **GATED** | 401 | Upgrade plan | 600 | — |
| `indic-bitcoin-reserve-risk` | `/api/index/bitcoin-reserve-risk` | **GATED** | 401 | Upgrade plan | 645 | — |
| `indic-bitcoin-nupl` | `/api/index/bitcoin-net-unrealized-profit-loss` | **GATED** | 401 | Upgrade plan | 658 | — |
| `indic-bitcoin-correlation` | `/api/index/bitcoin-correlation` | **GATED** | 401 | Upgrade plan | 621 | — |
| `indic-bitcoin-bmo` | `/api/index/bitcoin-macro-oscillator` | **GATED** | 401 | Upgrade plan | 510 | — |
| `indic-options-futures-oi-ratio` | `/api/index/option-vs-futures-oi-ratio` | **GATED** | 401 | Upgrade plan | 554 | — |
| `indic-altcoin-season` | `/api/index/altcoin-season` | **GATED** | 401 | Upgrade plan | 658 | — |
| `indic-btc-vs-global-m2` | `/api/index/bitcoin-vs-global-m2-growth` | **GATED** | 401 | Upgrade plan | 809 | — |
| `indic-btc-vs-us-m2` | `/api/index/bitcoin-vs-us-m2-growth` | **GATED** | 401 | Upgrade plan | 639 | — |
| `indic-bitcoin-dominance` | `/api/index/bitcoin-dominance` | **GATED** | 401 | Upgrade plan | 535 | — |
| `indic-futures-spot-volume-ratio` | `/api/futures_spot_volume_ratio` | **GATED** | 401 | Upgrade plan | 540 | — |

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
- `futures-coins-price-change` → Upgrade plan
- `funding-rate-arbitrage` → Upgrade plan
- `net-position-history` → Upgrade plan
- `net-position-v2-history` → Upgrade plan
- `liq-aggregated-heatmap-model1` → Upgrade plan
- `liq-aggregated-heatmap-model2` → Upgrade plan
- `liq-pair-map` → Upgrade plan
- `liq-aggregated-map` → Upgrade plan
- `liq-max-pain` → Upgrade plan
- `hyperliquid-position` → Upgrade plan
- `hyperliquid-user-position` → Upgrade plan
- `hyperliquid-wallet-pnl-dist` → Upgrade plan
- `hyperliquid-global-l-s-account` → Upgrade plan
- `futures-netflow-list` → Upgrade plan
- `futures-coin-netflow-fix` → Upgrade plan
- `spot-coins-markets` → Upgrade plan
- `spot-orderbook-history` → Upgrade plan
- `spot-large-limit-order` → Upgrade plan
- `spot-large-limit-order-history` → Upgrade plan
- `spot-footprint` → Upgrade plan
- `spot-cvd-history` → Upgrade plan
- `spot-aggregated-cvd` → Upgrade plan
- `spot-netflow-list` → Upgrade plan
- `spot-coin-netflow` → Upgrade plan
- `onchain-exchange-assets-transparency` → Upgrade plan
- `onchain-token-unlock-list` → Upgrade plan
- `onchain-token-vesting` → Upgrade plan
- `onchain-whale-transfer` → Upgrade plan
- `indic-td-sequential` → Upgrade plan
- `indic-coin-atr-list` → Upgrade plan
- `indic-pair-atr` → Upgrade plan
- `indic-whale-index` → Upgrade plan
- `indic-ma-native` → Upgrade plan
- `indic-ema-native` → Upgrade plan
- `indic-rsi-native` → Upgrade plan
- `indic-macd-native` → Upgrade plan
- `indic-boll-native` → Upgrade plan
- `indic-macd-list` → Upgrade plan
- `indic-bitcoin-sth-sopr` → Upgrade plan
- `indic-bitcoin-lth-sopr` → Upgrade plan
- `indic-bitcoin-sth-realized-price` → Upgrade plan
- `indic-bitcoin-lth-realized-price` → Upgrade plan
- `indic-bitcoin-rhodl-ratio` → Upgrade plan
- `indic-bitcoin-sth-supply` → Upgrade plan
- `indic-bitcoin-lth-supply` → Upgrade plan
- `indic-bitcoin-new-addresses` → Upgrade plan
- `indic-bitcoin-active-addresses` → Upgrade plan
- `indic-bitcoin-reserve-risk` → Upgrade plan
- `indic-bitcoin-nupl` → Upgrade plan
- `indic-bitcoin-correlation` → Upgrade plan
- `indic-bitcoin-bmo` → Upgrade plan
- `indic-options-futures-oi-ratio` → Upgrade plan
- `indic-altcoin-season` → Upgrade plan
- `indic-btc-vs-global-m2` → Upgrade plan
- `indic-btc-vs-us-m2` → Upgrade plan
- `indic-bitcoin-dominance` → Upgrade plan
- `indic-futures-spot-volume-ratio` → Upgrade plan

## Endpoint ERROR / NOT_FOUND

Path da rivedere: refuso editoriale o cambio di nome non documentato.

- `spot-pairs-markets` (/api/spot/pairs-markets): HTTP 200 code=500 msg=Server Error
- `indic-futures-basis` (/api/futures/basis/history): HTTP 200 code=500 msg=Server Error
- `futures-coin-netflow-typo` (/api/furures/coin/netflow): HTTP 404 code=None msg=HTTP 404
