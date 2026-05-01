# CoinGlass smoke-test report — Hobbyist plan

Run time: 2026-04-30 20:09:41 UTC
Base URL: `https://open-api-v4.coinglass.com`
Probes: **171**, rate ~24 rpm

## Sintesi per classificazione

| Classe | Conteggio |
|---|---:|
| AVAILABLE | 82 |
| AVAILABLE_EMPTY | 1 |
| GATED | 79 |
| RATE_LIMIT | 0 |
| ERROR | 2 |
| NOT_FOUND | 3 |

## Dettaglio

| Endpoint | Path | Class | code | msg | ms | sample keys |
|---|---|---|---|---|---:|---|
| `supported-coins` | `/api/futures/supported-coins` | **AVAILABLE** | 0 |  | 895 | — |
| `supported-exchange-pairs` | `/api/futures/supported-exchange-pairs` | **AVAILABLE** | 0 |  | 2030 | ApeX Omni, Aster, Binance, BingX, Bitfinex, Bitget |
| `coins-markets` | `/api/futures/coins-markets` | **GATED** | 401 | Upgrade plan | 545 | — |
| `open-interest-history-1h` | `/api/futures/open-interest/history` | **AVAILABLE** | 0 |  | 505 | close, high, low, open, time |
| `funding-rate-history` | `/api/futures/funding-rate/history` | **AVAILABLE** | 0 |  | 632 | close, high, low, open, time |
| `liquidation-aggregated-history` | `/api/futures/liquidation/aggregated-history` | **AVAILABLE** | 0 |  | 593 | aggregated_long_liquidation_usd, aggregated_short_liquidation_usd, time |
| `global-long-short-account-ratio` | `/api/futures/global-long-short-account-ratio/history` | **AVAILABLE** | 0 |  | 665 | global_account_long_percent, global_account_long_short_ratio, global_account_short_percent, time |
| `cgdi-index-history` | `/api/futures/cgdi-index/history` | **AVAILABLE** | 0 |  | 908 | cgdi_index_value, time |
| `etf-bitcoin-list` | `/api/etf/bitcoin/list` | **AVAILABLE** | 0 |  | 633 | asset_details, aum_usd, cik_code, fund_name, fund_type, last_quote_time |
| `etf-bitcoin-flow-history` | `/api/etf/bitcoin/flow-history` | **AVAILABLE** | 0 |  | 1369 | etf_flows, flow_usd, price_usd, timestamp |
| `etf-bitcoin-net-assets-history` | `/api/etf/bitcoin/net-assets/history` | **AVAILABLE** | 0 |  | 890 | change_usd, net_assets_usd, price_usd, timestamp |
| `etf-bitcoin-premium-discount-history` | `/api/etf/bitcoin/premium-discount/history` | **AVAILABLE** | 0 |  | 1676 | list, timestamp |
| `etf-ethereum-list` | `/api/etf/ethereum/list` | **AVAILABLE** | 0 |  | 496 | asset_details, aum_usd, fund_name, fund_type, last_quote_time, last_trade_time |
| `etf-hong-kong-bitcoin-flow-history` | `/api/hk-etf/bitcoin/flow-history` | **AVAILABLE** | 0 |  | 1286 | etf_flows, flow_usd, price_usd, timestamp |
| `futures-rsi-list` | `/api/futures/rsi/list` | **GATED** | 401 | Upgrade plan | 510 | — |
| `orderbook-history` | `/api/futures/orderbook/history` | **GATED** | 401 | Upgrade plan | 522 | — |
| `orderbook-large-limit-order` | `/api/futures/orderbook/large-limit-order` | **GATED** | 401 | Upgrade plan | 456 | — |
| `orderbook-large-limit-order-history` | `/api/futures/orderbook/large-limit-order-history` | **GATED** | 401 | Upgrade plan | 451 | — |
| `footprint` | `/api/futures/volume/footprint-history` | **GATED** | 401 | Upgrade plan | 492 | — |
| `liquidation-heatmap-model1-1y` | `/api/futures/liquidation/heatmap/model1` | **GATED** | 401 | Upgrade plan | 412 | — |
| `liquidation-heatmap-model1-180d` | `/api/futures/liquidation/heatmap/model1` | **GATED** | 401 | Upgrade plan | 600 | — |
| `liquidation-heatmap-model2-180d` | `/api/futures/liquidation/heatmap/model2` | **GATED** | 401 | Upgrade plan | 535 | — |
| `liquidation-heatmap-model3-180d` | `/api/futures/liquidation/heatmap/model3` | **GATED** | 401 | Upgrade plan | 548 | — |
| `liquidation-aggregated-heatmap-model3` | `/api/futures/liquidation/aggregated-heatmap/model3` | **GATED** | 401 | Upgrade plan | 466 | — |
| `hyperliquid-whale-alert` | `/api/hyperliquid/whale-alert` | **GATED** | 401 | Upgrade plan | 500 | — |
| `hyperliquid-whale-position` | `/api/hyperliquid/whale-position` | **GATED** | 401 | Upgrade plan | 494 | — |
| `cvd-history` | `/api/futures/cvd/history` | **GATED** | 401 | Upgrade plan | 418 | — |
| `aggregated-cvd-history` | `/api/futures/aggregated-cvd/history` | **GATED** | 401 | Upgrade plan | 494 | — |
| `taker-buy-sell-volume-history` | `/api/futures/taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 531 | taker_buy_volume_usd, taker_sell_volume_usd, time |
| `taker-buy-sell-volume-history-v2` | `/api/futures/v2/taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 503 | taker_buy_volume_usd, taker_sell_volume_usd, time |
| `aggregated-taker-buy-sell-volume` | `/api/futures/aggregated-taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 490 | aggregated_buy_volume_usd, aggregated_sell_volume_usd, time |
| `option-info` | `/api/option/info` | **AVAILABLE** | 0 |  | 514 | exchange_name, oi_market_share, open_interest, open_interest_change_24h, open_interest_usd, volume_change_percent_24h |
| `option-max-pain` | `/api/option/max-pain` | **AVAILABLE** | 0 |  | 530 | call_open_interest, call_open_interest_market_value, call_open_interest_notional, date, max_pain_price, put_open_interest |
| `option-exchange-oi-history` | `/api/option/exchange-oi-history` | **AVAILABLE** | 0 |  | 521 | data_map, price_list, time_list |
| `coinbase-premium-index` | `/api/coinbase-premium-index` | **AVAILABLE** | 0 | success | 433 | coinbase_price, premium, premium_rate, time |
| `fear-greed-history` | `/api/index/fear-greed-history` | **AVAILABLE** | 0 |  | 1181 | data_list, price_list, time_list |
| `stable-coin-marketcap-history` | `/api/index/stableCoin-marketCap-history` | **AVAILABLE** | 0 |  | 1397 | data_list, price_list, time_list |
| `exchange-balance-list` | `/api/exchange/balance/list` | **AVAILABLE** | 0 |  | 426 | balance_change_1d, balance_change_30d, balance_change_7d, balance_change_percent_1d, balance_change_percent_30d, balance_change_percent_7d |
| `index-ahr999` | `/api/index/ahr999` | **AVAILABLE** | 0 |  | 1830 | ahr999_value, average_price, current_value, date_string |
| `index-puell-multiple` | `/api/index/puell-multiple` | **AVAILABLE** | 0 |  | 1650 | price, puell_multiple, timestamp |
| `index-golden-ratio-multiplier` | `/api/index/golden-ratio-multiplier` | **AVAILABLE** | 0 |  | 2046 | accumulation_high_1_6, low_bull_high_2, ma_350, price, timestamp, x_13 |
| `index-pi-cycle` | `/api/index/pi-cycle-indicator` | **AVAILABLE** | 0 |  | 1650 | ma_110, ma_350_mu_2, price, timestamp |
| `index-stock-flow` | `/api/index/stock-flow` | **AVAILABLE** | 0 |  | 1625 | next_halving, price, timestamp |
| `index-bitcoin-rainbow` | `/api/index/bitcoin/rainbow-chart` | **AVAILABLE** | 0 |  | 1825 | — |
| `index-bitcoin-bubble-index` | `/api/index/bitcoin/bubble-index` | **AVAILABLE** | 0 |  | 1800 | address_send_count, bubble_index, date_string, mining_difficulty, price, transaction_count |
| `user-account-subscription` | `/api/user/account/subscription` | **AVAILABLE** | 0 |  | 402 | expire_time, expired, level |
| `futures-pairs-markets` | `/api/futures/pairs-markets` | **AVAILABLE_EMPTY** | 0 |  | 609 | — |
| `futures-price-ohlc-history` | `/api/futures/price/history` | **AVAILABLE** | 0 |  | 742 | close, high, low, open, time, volume_usd |
| `futures-exchange-rank` | `/api/futures/exchange-rank` | **AVAILABLE** | 0 |  | 541 | exchange, liquidation_usd_24h, open_interest_usd, volume_usd |
| `futures-delisted-pairs` | `/api/futures/delisted-exchange-pairs` | **AVAILABLE** | 0 |  | 947 | ApeX Omni, Aster, Binance, BingX, Bitfinex, Bitget |
| `futures-supported-exchanges` | `/api/futures/supported-exchanges` | **AVAILABLE** | 0 |  | 420 | — |
| `futures-funding-rate-oi-weight` | `/api/futures/funding-rate/oi-weight-history` | **AVAILABLE** | 0 |  | 552 | close, high, low, open, time |
| `futures-funding-rate-vol-weight` | `/api/futures/funding-rate/vol-weight-history` | **AVAILABLE** | 0 |  | 636 | close, high, low, open, time |
| `futures-funding-rate-cumulative` | `/api/futures/funding-rate/accumulated-exchange-list` | **AVAILABLE** | 0 |  | 1851 | stablecoin_margin_list, symbol, token_margin_list |
| `futures-top-long-short-account-ratio` | `/api/futures/top-long-short-account-ratio/history` | **AVAILABLE** | 0 |  | 683 | time, top_account_long_percent, top_account_long_short_ratio, top_account_short_percent |
| `futures-top-long-short-position-ratio` | `/api/futures/top-long-short-position-ratio/history` | **AVAILABLE** | 0 |  | 700 | time, top_position_long_percent, top_position_long_short_ratio, top_position_short_percent |
| `futures-coin-aggregated-orderbook` | `/api/futures/orderbook/aggregated-ask-bids-history` | **AVAILABLE** | 0 |  | 1136 | aggregated_asks_quantity, aggregated_asks_usd, aggregated_bids_quantity, aggregated_bids_usd, time |
| `futures-aggregated-taker-buy-sell-volume-fix` | `/api/futures/aggregated-taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 485 | aggregated_buy_volume_usd, aggregated_sell_volume_usd, time |
| `futures-liquidation-aggregated-history-fix` | `/api/futures/liquidation/aggregated-history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange_list' is not present | 541 | — |
| `spot-supported-coins` | `/api/spot/supported-coins` | **AVAILABLE** | 0 |  | 742 | — |
| `spot-supported-exchange-pairs` | `/api/spot/supported-exchange-pairs` | **AVAILABLE** | 0 |  | 1588 | Binance, Bitfinex, Bitget, Bybit, Coinbase, Crypto.com |
| `spot-pairs-markets` | `/api/spot/pairs-markets` | **ERROR** | 500 | Server Error | 514 | — |
| `spot-price-history` | `/api/spot/price/history` | **AVAILABLE** | 0 |  | 791 | close, high, low, open, time, volume_usd |
| `spot-orderbook-ask-bids` | `/api/spot/orderbook/ask-bids-history` | **AVAILABLE** | 0 |  | 769 | asks_quantity, asks_usd, bids_quantity, bids_usd, time |
| `spot-aggregated-orderbook` | `/api/spot/orderbook/aggregated-ask-bids-history` | **AVAILABLE** | 0 |  | 805 | aggregated_asks_quantity, aggregated_asks_usd, aggregated_bids_quantity, aggregated_bids_usd, time |
| `spot-coin-taker-buy-sell-history` | `/api/spot/aggregated-taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 473 | aggregated_buy_volume_usd, aggregated_sell_volume_usd, time |
| `spot-pair-taker-buy-sell-history` | `/api/spot/taker-buy-sell-volume/history` | **AVAILABLE** | 0 |  | 478 | taker_buy_volume_usd, taker_sell_volume_usd, time |
| `option-info-fix` | `/api/option/info` | **AVAILABLE** | 0 |  | 541 | exchange_name, oi_market_share, open_interest, open_interest_change_24h, open_interest_usd, volume_change_percent_24h |
| `option-exchange-vol-history` | `/api/option/exchange-vol-history` | **AVAILABLE** | 0 | success | 1457 | data_map, price_list, time_list |
| `option-exchange-oi-history-fix` | `/api/option/exchange-oi-history` | **AVAILABLE** | 0 |  | 688 | data_map, price_list, time_list |
| `etf-bitcoin-net-assets-fix` | `/api/etf/bitcoin/net-assets/history` | **AVAILABLE** | 0 |  | 911 | change_usd, net_assets_usd, price_usd, timestamp |
| `etf-bitcoin-premium-discount-fix` | `/api/etf/bitcoin/premium-discount/history` | **AVAILABLE** | 0 |  | 967 | market_price_usd, nav_usd, premium_discount_details, timestamp |
| `etf-bitcoin-history` | `/api/etf/bitcoin/history` | **AVAILABLE** | 0 |  | 1121 | assets_date, btc_holdings, market_date, market_price, name, nav |
| `etf-bitcoin-price-history` | `/api/etf/bitcoin/price/history` | **AVAILABLE** | 0 |  | 1465 | close, high, low, open, time, volume |
| `etf-bitcoin-detail` | `/api/etf/bitcoin/detail` | **AVAILABLE** | 0 |  | 576 | last_quote, last_trade, market_status, name, performance, session |
| `etf-hk-bitcoin-flow-fix` | `/api/hk-etf/bitcoin/flow-history` | **AVAILABLE** | 0 |  | 1265 | etf_flows, flow_usd, price_usd, timestamp |
| `etf-ethereum-flow-history` | `/api/etf/ethereum/flow-history` | **AVAILABLE** | 0 |  | 1145 | etf_flows, flow_usd, price_usd, timestamp |
| `etf-ethereum-net-assets` | `/api/etf/ethereum/net-assets/history` | **AVAILABLE** | 0 |  | 2897 | change_usd, net_assets_usd, price_usd, timestamp |
| `etf-grayscale-holdings` | `/api/grayscale/holdings-list` | **AVAILABLE** | 0 |  | 405 | close_time, holdings_amount, holdings_amount_change1d, holdings_amount_change_30d, holdings_amount_change_7d, holdings_usd |
| `etf-solana-flow-history` | `/api/etf/solana/flow-history` | **AVAILABLE** | 0 |  | 534 | etf_flows, flow_usd, price_usd, timestamp |
| `etf-xrp-flow-history` | `/api/etf/xrp/flow-history` | **AVAILABLE** | 0 |  | 864 | etf_flows, flow_usd, price_usd, timestamp |
| `exchange-assets` | `/api/exchange/assets` | **AVAILABLE** | 0 | success | 510 | assets_name, balance, balance_usd, price, symbol, wallet_address |
| `exchange-balance-chart` | `/api/exchange/balance/chart` | **AVAILABLE** | 0 |  | 1274 | data_map, price_list, time_list |
| `exchange-onchain-transfers-erc20` | `/api/exchange/chain/tx/list` | **AVAILABLE** | 0 |  | 728 | amount_usd, asset_quantity, asset_symbol, exchange_name, from_address, to_address |
| `indic-futures-basis` | `/api/futures/basis/history` | **ERROR** | 500 | Server Error | 435 | — |
| `indic-puell-multiple-fix` | `/api/index/puell-multiple` | **AVAILABLE** | 0 |  | 1686 | price, puell_multiple, timestamp |
| `indic-golden-ratio-fix` | `/api/index/golden-ratio-multiplier` | **AVAILABLE** | 0 |  | 1950 | accumulation_high_1_6, low_bull_high_2, ma_350, price, timestamp, x_13 |
| `indic-pi-cycle-fix` | `/api/index/pi-cycle-indicator` | **AVAILABLE** | 0 |  | 1647 | ma_110, ma_350_mu_2, price, timestamp |
| `indic-stock-flow-fix` | `/api/index/stock-flow` | **AVAILABLE** | 0 |  | 1587 | next_halving, price, timestamp |
| `indic-bitcoin-bubble-fix` | `/api/index/bitcoin/bubble-index` | **AVAILABLE** | 0 |  | 1821 | address_send_count, bubble_index, date_string, mining_difficulty, price, transaction_count |
| `indic-bitcoin-profitable-days` | `/api/index/bitcoin/profitable-days` | **AVAILABLE** | 0 |  | 1444 | price, side, timestamp |
| `indic-bull-market-peak` | `/api/bull-market-peak-indicator` | **AVAILABLE** | 0 | success | 567 | change_value, comparison_type, current_value, hit_status, indicator_name, previous_value |
| `indic-2y-ma-multiplier` | `/api/index/2-year-ma-multiplier` | **AVAILABLE** | 0 |  | 1845 | moving_average_730, moving_average_730_multiplier_5, price, timestamp |
| `indic-200w-ma-heatmap` | `/api/index/200-week-moving-average-heatmap` | **AVAILABLE** | 0 |  | 1578 | moving_average_1440, moving_average_1440_ip, price, timestamp |
| `indic-cdri-index` | `/api/futures/cdri-index/history` | **AVAILABLE** | 0 |  | 989 | cdri_index_value, time |
| `indic-bitfinex-margin-long-short` | `/api/bitfinex-margin-long-short` | **AVAILABLE** | 0 |  | 536 | long_quantity, short_quantity, time |
| `indic-borrow-interest-rate` | `/api/borrow-interest-rate/history` | **AVAILABLE** | 0 |  | 485 | interest_rate, time |
| `other-economic-calendar` | `/api/calendar/economic-data` | **GATED** | 401 | Upgrade plan | 490 | — |
| `other-news-list` | `/api/article/list` | **GATED** | 401 | Upgrade plan | 503 | — |
| `futures-coins-price-change` | `/api/futures/coins-price-change` | **GATED** | 401 | Upgrade plan | 613 | — |
| `oi-aggregated-history` | `/api/futures/open-interest/aggregated-history` | **AVAILABLE** | 0 |  | 490 | close, high, low, open, time |
| `oi-aggregated-stablecoin-history` | `/api/futures/open-interest/aggregated-stablecoin-history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange_list' is not present | 466 | — |
| `oi-aggregated-coin-margin-history` | `/api/futures/open-interest/aggregated-coin-margin-history` | **BAD_PARAMS** | 400 | Required String parameter 'exchange_list' is not present | 602 | — |
| `oi-exchange-history-chart` | `/api/futures/open-interest/exchange-history-chart` | **BAD_PARAMS** | 400 | Required String parameter 'range' is not present | 510 | — |
| `funding-rate-arbitrage` | `/api/futures/funding-rate/arbitrage` | **GATED** | 401 | Upgrade plan | 412 | — |
| `taker-buy-sell-exchange-list` | `/api/futures/taker-buy-sell-volume/exchange-list` | **AVAILABLE** | 0 | success | 865 | buy_ratio, buy_vol_usd, exchange_list, sell_ratio, sell_vol_usd, symbol |
| `net-position-history` | `/api/futures/net-position/history` | **GATED** | 401 | Upgrade plan | 561 | — |
| `net-position-v2-history` | `/api/futures/v2/net-position/history` | **GATED** | 401 | Upgrade plan | 704 | — |
| `liq-aggregated-heatmap-model1` | `/api/futures/liquidation/aggregated-heatmap/model1` | **GATED** | 401 | Upgrade plan | 662 | — |
| `liq-aggregated-heatmap-model2` | `/api/futures/liquidation/aggregated-heatmap/model2` | **GATED** | 401 | Upgrade plan | 538 | — |
| `liq-pair-map` | `/api/futures/liquidation/map` | **GATED** | 401 | Upgrade plan | 471 | — |
| `liq-aggregated-map` | `/api/futures/liquidation/aggregated-map` | **GATED** | 401 | Upgrade plan | 678 | — |
| `liq-max-pain` | `/api/futures/liquidation/max-pain` | **GATED** | 401 | Upgrade plan | 501 | — |
| `hyperliquid-position` | `/api/hyperliquid/position` | **GATED** | 401 | Upgrade plan | 617 | — |
| `hyperliquid-user-position` | `/api/hyperliquid/user-position` | **GATED** | 401 | Upgrade plan | 527 | — |
| `hyperliquid-wallet-pnl-dist` | `/api/hyperliquid/wallet/pnl-distribution` | **GATED** | 401 | Upgrade plan | 549 | — |
| `hyperliquid-global-l-s-account` | `/api/hyperliquid/global-long-short-account-ratio/history` | **GATED** | 401 | Upgrade plan | 480 | — |
| `futures-netflow-list` | `/api/futures/netflow-list` | **GATED** | 401 | Upgrade plan | 491 | — |
| `futures-coin-netflow-typo` | `/api/furures/coin/netflow` | **NOT_FOUND** | — | HTTP 404 | 517 | — |
| `futures-coin-netflow-fix` | `/api/futures/coin/netflow` | **GATED** | 401 | Upgrade plan | 760 | — |
| `spot-coins-markets` | `/api/spot/coins-markets` | **GATED** | 401 | Upgrade plan | 470 | — |
| `spot-orderbook-history` | `/api/spot/orderbook/history` | **GATED** | 401 | Upgrade plan | 449 | — |
| `spot-large-limit-order` | `/api/spot/orderbook/large-limit-order` | **GATED** | 401 | Upgrade plan | 481 | — |
| `spot-large-limit-order-history` | `/api/spot/orderbook/large-limit-order-history` | **GATED** | 401 | Upgrade plan | 539 | — |
| `spot-footprint` | `/api/spot/volume/footprint-history` | **GATED** | 401 | Upgrade plan | 565 | — |
| `spot-cvd-history` | `/api/spot/cvd/history` | **GATED** | 401 | Upgrade plan | 447 | — |
| `spot-aggregated-cvd` | `/api/spot/aggregated-cvd/history` | **GATED** | 401 | Upgrade plan | 492 | — |
| `spot-netflow-list` | `/api/spot/netflow-list` | **GATED** | 401 | Upgrade plan | 536 | — |
| `spot-coin-netflow` | `/api/spot/coin/netflow` | **GATED** | 401 | Upgrade plan | 615 | — |
| `onchain-exchange-assets-transparency` | `/api/exchange_assets_transparency/list` | **GATED** | 401 | Upgrade plan | 520 | — |
| `onchain-token-unlock-list` | `/api/coin/unlock-list` | **GATED** | 401 | Upgrade plan | 426 | — |
| `onchain-token-vesting` | `/api/coin/vesting` | **GATED** | 401 | Upgrade plan | 576 | — |
| `onchain-whale-transfer` | `/api/chain/v2/whale-transfer` | **GATED** | 401 | Upgrade plan | 532 | — |
| `etf-bitcoin-aum` | `/api/etf/bitcoin/aum` | **AVAILABLE** | 0 |  | 1005 | aum_usd, time |
| `etf-grayscale-premium` | `/api/grayscale/premium-history` | **AVAILABLE** | 0 |  | 925 | premium_rate_list, primary_market_price, secondary_market_price_list, time_list |
| `indic-td-sequential` | `/api/futures/indicators/td` | **GATED** | 401 | Upgrade plan | 626 | — |
| `indic-coin-atr-list` | `/api/futures/avg-true-range/list` | **GATED** | 401 | Upgrade plan | 487 | — |
| `indic-pair-atr` | `/api/futures/indicators/avg-true-range` | **GATED** | 401 | Upgrade plan | 555 | — |
| `indic-whale-index` | `/api/futures/whale-index/history` | **GATED** | 401 | Upgrade plan | 539 | — |
| `indic-ma-native` | `/api/futures/indicators/ma` | **GATED** | 401 | Upgrade plan | 464 | — |
| `indic-ema-native` | `/api/futures/indicators/ema` | **GATED** | 401 | Upgrade plan | 534 | — |
| `indic-rsi-native` | `/api/futures/indicators/rsi` | **GATED** | 401 | Upgrade plan | 850 | — |
| `indic-macd-native` | `/api/futures/indicators/macd` | **GATED** | 401 | Upgrade plan | 536 | — |
| `indic-boll-native` | `/api/futures/indicators/boll` | **GATED** | 401 | Upgrade plan | 496 | — |
| `indic-macd-list` | `/api/futures/macd/list` | **GATED** | 401 | Upgrade plan | 787 | — |
| `indic-bitcoin-sth-sopr` | `/api/index/bitcoin-sth-sopr` | **GATED** | 401 | Upgrade plan | 546 | — |
| `indic-bitcoin-lth-sopr` | `/api/index/bitcoin-lth-sopr` | **GATED** | 401 | Upgrade plan | 576 | — |
| `indic-bitcoin-sth-realized-price` | `/api/index/bitcoin-sth-realized-price` | **GATED** | 401 | Upgrade plan | 425 | — |
| `indic-bitcoin-lth-realized-price` | `/api/index/bitcoin-lth-realized-price` | **GATED** | 401 | Upgrade plan | 489 | — |
| `indic-bitcoin-rhodl-ratio` | `/api/index/bitcoin-rhodl-ratio` | **GATED** | 401 | Upgrade plan | 490 | — |
| `indic-bitcoin-sth-supply` | `/api/index/bitcoin-short-term-holder-supply` | **GATED** | 401 | Upgrade plan | 455 | — |
| `indic-bitcoin-lth-supply` | `/api/index/bitcoin-long-term-holder-supply` | **GATED** | 401 | Upgrade plan | 456 | — |
| `indic-bitcoin-new-addresses` | `/api/index/bitcoin-new-addresses` | **GATED** | 401 | Upgrade plan | 508 | — |
| `indic-bitcoin-active-addresses` | `/api/index/bitcoin-active-addresses` | **GATED** | 401 | Upgrade plan | 534 | — |
| `indic-bitcoin-reserve-risk` | `/api/index/bitcoin-reserve-risk` | **GATED** | 401 | Upgrade plan | 672 | — |
| `indic-bitcoin-nupl` | `/api/index/bitcoin-net-unrealized-profit-loss` | **GATED** | 401 | Upgrade plan | 452 | — |
| `indic-bitcoin-correlation` | `/api/index/bitcoin-correlation` | **GATED** | 401 | Upgrade plan | 514 | — |
| `indic-bitcoin-bmo` | `/api/index/bitcoin-macro-oscillator` | **GATED** | 401 | Upgrade plan | 491 | — |
| `indic-options-futures-oi-ratio` | `/api/index/option-vs-futures-oi-ratio` | **GATED** | 401 | Upgrade plan | 555 | — |
| `indic-altcoin-season` | `/api/index/altcoin-season` | **GATED** | 401 | Upgrade plan | 646 | — |
| `indic-btc-vs-global-m2` | `/api/index/bitcoin-vs-global-m2-growth` | **GATED** | 401 | Upgrade plan | 503 | — |
| `indic-btc-vs-us-m2` | `/api/index/bitcoin-vs-us-m2-growth` | **GATED** | 401 | Upgrade plan | 686 | — |
| `indic-bitcoin-dominance` | `/api/index/bitcoin-dominance` | **GATED** | 401 | Upgrade plan | 663 | — |
| `indic-futures-spot-volume-ratio` | `/api/futures_spot_volume_ratio` | **GATED** | 401 | Upgrade plan | 441 | — |
| `btc-correlations-traditional` | `/api/index/bitcoin-correlation` | **GATED** | 401 | Upgrade plan | 824 | — |
| `indic-td-list-multicoin` | `/api/futures/td/list` | **GATED** | 401 | Upgrade plan | 475 | — |
| `indic-ma-list-multicoin` | `/api/futures/ma/list` | **GATED** | 401 | Upgrade plan | 601 | — |
| `indic-ema-list-multicoin` | `/api/futures/ema/list` | **GATED** | 401 | Upgrade plan | 746 | — |
| `indic-rsi-list-pair` | `/api/futures/rsi/list` | **GATED** | 401 | Upgrade plan | 693 | — |
| `spot-coin-market-data-history` | `/api/spot/coin-market-data/history` | **NOT_FOUND** | — | HTTP 404 | 511 | — |
| `instruments-matrix` | `/api/futures/instruments` | **NOT_FOUND** | — | HTTP 404 | 605 | — |

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
- `btc-correlations-traditional` → Upgrade plan
- `indic-td-list-multicoin` → Upgrade plan
- `indic-ma-list-multicoin` → Upgrade plan
- `indic-ema-list-multicoin` → Upgrade plan
- `indic-rsi-list-pair` → Upgrade plan

## Endpoint ERROR / NOT_FOUND

Path da rivedere: refuso editoriale o cambio di nome non documentato.

- `spot-pairs-markets` (/api/spot/pairs-markets): HTTP 200 code=500 msg=Server Error
- `indic-futures-basis` (/api/futures/basis/history): HTTP 200 code=500 msg=Server Error
- `futures-coin-netflow-typo` (/api/furures/coin/netflow): HTTP 404 code=None msg=HTTP 404
- `spot-coin-market-data-history` (/api/spot/coin-market-data/history): HTTP 404 code=None msg=HTTP 404
- `instruments-matrix` (/api/futures/instruments): HTTP 404 code=None msg=HTTP 404
