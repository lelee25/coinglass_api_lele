# CoinGecko Demo API smoke-test report

Run: 2026-04-30 20:45:22 UTC
Base URL: `https://api.coingecko.com/api/v3` — header `x-cg-demo-api-key`
Probes: **61**, rate ~27 rpm

## Sintesi per classificazione

| Classe | Conteggio |
|---|---:|
| AVAILABLE | 51 |
| AVAILABLE_EMPTY | 0 |
| GATED | 0 |
| RATE_LIMIT | 0 |
| BAD_PARAMS | 0 |
| ERROR | 10 |
| NOT_FOUND | 0 |

## Dettaglio

| Endpoint | Path | Class | code | msg | ms | sample keys |
|---|---|---|---|---|---:|---|
| `ping` | `/ping` | **AVAILABLE** | — |  | 495 | gecko_says |
| `key (account info & usage)` | `/key` | **ERROR** | 10005 | This request is limited to PRO API subscribers. Please visit | 506 | status |
| `simple/price BTC,ETH` | `/simple/price` | **AVAILABLE** | — |  | 408 | bitcoin, ethereum |
| `simple/supported_vs_currencies` | `/simple/supported_vs_currencies` | **AVAILABLE** | — |  | 362 | — |
| `simple/token_price (USDT eth)` | `/simple/token_price/ethereum` | **AVAILABLE** | — |  | 671 | 0xdac17f958d2ee523a2206206994597c13d831ec7 |
| `coins/list (universe)` | `/coins/list` | **AVAILABLE** | — |  | 713 | id, name, symbol |
| `coins/list/new (latest 200)` | `/coins/list/new` | **ERROR** | 10005 | This request is limited to PRO API subscribers. Please visit | 390 | status |
| `coins/markets Top 250` | `/coins/markets` | **AVAILABLE** | — |  | 526 | ath, ath_change_percentage, ath_date, atl, atl_change_percentage, atl_date |
| `coins/top_gainers_losers (PAID?)` | `/coins/top_gainers_losers` | **ERROR** | 10005 | This request is limited to PRO API subscribers. Please visit | 432 | status |
| `coins/{id} bitcoin` | `/coins/bitcoin` | **AVAILABLE** | — |  | 448 | additional_notices, asset_platform_id, block_time_in_minutes, categories, country_origin, description |
| `coins/{id}/tickers BTC` | `/coins/bitcoin/tickers` | **AVAILABLE** | — |  | 735 | name, tickers |
| `coins/{id}/market_chart 30d` | `/coins/bitcoin/market_chart` | **AVAILABLE** | — |  | 791 | market_caps, prices, total_volumes |
| `coins/{id}/market_chart/range` | `/coins/bitcoin/market_chart/range` | **AVAILABLE** | — |  | 512 | market_caps, prices, total_volumes |
| `coins/{id}/ohlc 30d` | `/coins/bitcoin/ohlc` | **AVAILABLE** | — |  | 361 | — |
| `coins/{id}/ohlc/range (PAID?)` | `/coins/bitcoin/ohlc/range` | **ERROR** | 10005 | This request is limited to PRO API subscribers. Please visit | 400 | status |
| `coins/{id}/circulating_supply_chart (PAID?)` | `/coins/bitcoin/circulating_supply_chart` | **ERROR** | 10005 | This endpoint is exclusive to Enterprise plan customers only | 389 | status |
| `coins/{id}/history (DD-MM-YYYY)` | `/coins/bitcoin/history` | **AVAILABLE** | — |  | 403 | community_data, developer_data, id, image, localization, market_data |
| `search/trending` | `/search/trending` | **AVAILABLE** | — |  | 303 | categories, coins, nfts |
| `search?query=solana` | `/search` | **AVAILABLE** | — |  | 387 | categories, coins, exchanges, icos, nfts |
| `coins/categories/list` | `/coins/categories/list` | **AVAILABLE** | — |  | 488 | category_id, name |
| `coins/categories` | `/coins/categories` | **AVAILABLE** | — |  | 826 | content, id, market_cap, market_cap_change_24h, name, top_3_coins |
| `global` | `/global` | **AVAILABLE** | — |  | 589 | data |
| `global/decentralized_finance_defi` | `/global/decentralized_finance_defi` | **AVAILABLE** | — |  | 696 | data |
| `global/market_cap_chart (PAID?)` | `/global/market_cap_chart` | **ERROR** | 10005 | This request is limited to PRO API subscribers. Please visit | 420 | status |
| `exchanges (page1)` | `/exchanges` | **AVAILABLE** | — |  | 423 | country, description, has_trading_incentive, id, image, name |
| `exchanges/list` | `/exchanges/list` | **AVAILABLE** | — |  | 442 | id, name |
| `exchanges/{id}/tickers Binance` | `/exchanges/binance/tickers` | **AVAILABLE** | — |  | 958 | name, tickers |
| `derivatives` | `/derivatives` | **AVAILABLE** | — |  | 1613 | basis, contract_type, expired_at, funding_rate, index, index_id |
| `derivatives/exchanges` | `/derivatives/exchanges` | **AVAILABLE** | — |  | 608 | country, description, id, image, name, number_of_futures_pairs |
| `companies/public_treasury bitcoin` | `/companies/public_treasury/bitcoin` | **AVAILABLE** | — |  | 398 | companies, market_cap_dominance, total_holdings, total_value_usd |
| `nfts/list` | `/nfts/list` | **AVAILABLE** | — |  | 539 | asset_platform_id, contract_address, id, name, symbol |
| `asset_platforms` | `/asset_platforms` | **AVAILABLE** | — |  | 483 | chain_identifier, id, image, name, native_coin_id, shortname |
| `onchain/networks` | `/onchain/networks` | **AVAILABLE** | — |  | 601 | data, links |
| `onchain/networks/eth/dexes` | `/onchain/networks/eth/dexes` | **AVAILABLE** | — |  | 532 | data, links |
| `onchain/networks/trending_pools` | `/onchain/networks/trending_pools` | **AVAILABLE** | — |  | 890 | data |
| `onchain/networks/eth/new_pools` | `/onchain/networks/eth/new_pools` | **AVAILABLE** | — |  | 823 | data |
| `onchain/networks/eth/trending_pools` | `/onchain/networks/eth/trending_pools` | **AVAILABLE** | — |  | 670 | data |
| `onchain/pools/megafilter` | `/onchain/pools/megafilter` | **ERROR** | 401 | This request is exclusive to Analyst plan or above subscribe | 418 | status |
| `onchain/simple/networks/eth/token_price USDT` | `/onchain/simple/networks/eth/token_price/0xdac17f958d2ee523a2206206994597c13d831ec7` | **AVAILABLE** | — |  | 541 | data |
| `onchain/networks/eth/tokens/{addr} USDT` | `/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7` | **AVAILABLE** | — |  | 476 | data |
| `onchain/networks/eth/tokens/{addr}/info` | `/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/info` | **AVAILABLE** | — |  | 651 | data |
| `onchain/networks/eth/tokens/{addr}/top_holders (PAID?)` | `/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/top_holders` | **ERROR** | 401 | This request is exclusive to Analyst plan or above subscribe | 452 | status |
| `onchain/networks/eth/tokens/{addr}/holders_chart` | `/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/holders_chart` | **ERROR** | 401 | This request is exclusive to Analyst plan or above subscribe | 522 | status |
| `onchain/networks/eth/tokens/{addr}/top_traders` | `/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/top_traders` | **ERROR** | 401 | This request is exclusive to Analyst plan or above subscribe | 389 | status |
| `onchain/networks/eth/pools/{addr}/trades` | `/onchain/networks/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/trades` | **AVAILABLE** | — |  | 1539 | data |
| `onchain/networks/eth/pools/{addr}/ohlcv/hour` | `/onchain/networks/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/ohlcv/hour` | **AVAILABLE** | — |  | 4731 | data, meta |
| `coins/{id}/contract/{addr} WBTC` | `/coins/ethereum/contract/0x2260fac5e5542a773aa44fbcfedf7c193bc2c599` | **AVAILABLE** | — |  | 784 | additional_notices, asset_platform_id, block_time_in_minutes, categories, community_data, contract_address |
| `coins/{id}/contract/{addr}/market_chart 30d` | `/coins/ethereum/contract/0x2260fac5e5542a773aa44fbcfedf7c193bc2c599/market_chart` | **AVAILABLE** | — |  | 813 | market_caps, prices, total_volumes |
| `coins/{id}/contract/{addr}/market_chart/range` | `/coins/ethereum/contract/0x2260fac5e5542a773aa44fbcfedf7c193bc2c599/market_chart/range` | **AVAILABLE** | — |  | 421 | market_caps, prices, total_volumes |
| `entities/list` | `/entities/list` | **AVAILABLE** | — |  | 460 | country, id, name, symbol |
| `public_treasury/{entity_id} tesla` | `/public_treasury/tesla` | **AVAILABLE** | — |  | 390 | country, holdings, id, m_nav, name, symbol |
| `public_treasury/{entity_id}/transaction_history` | `/public_treasury/tesla/transaction_history` | **AVAILABLE** | — |  | 308 | transactions |
| `onchain/networks/eth/pools/multi/{addrs}` | `/onchain/networks/eth/pools/multi/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640,0xcbcdf9626bc03e24f779434178a73a0b4bad62ed` | **AVAILABLE** | — |  | 1565 | data |
| `onchain/networks/eth/tokens/multi/{addrs}` | `/onchain/networks/eth/tokens/multi/0xdac17f958d2ee523a2206206994597c13d831ec7,0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48` | **AVAILABLE** | — |  | 606 | data |
| `onchain/tokens/info_recently_updated` | `/onchain/tokens/info_recently_updated` | **AVAILABLE** | — |  | 984 | data |
| `onchain/networks/eth/pools/{addr}/info` | `/onchain/networks/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/info` | **AVAILABLE** | — |  | 541 | data |
| `onchain/search/pools?query=ETH` | `/onchain/search/pools` | **AVAILABLE** | — |  | 3366 | data |
| `onchain/networks/eth/dexes/{dex}/pools` | `/onchain/networks/eth/dexes/uniswap_v3/pools` | **AVAILABLE** | — |  | 614 | data |
| `onchain/networks/eth/tokens/{addr}/pools` | `/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/pools` | **AVAILABLE** | — |  | 665 | data |
| `exchange_rates` | `/exchange_rates` | **AVAILABLE** | — |  | 229 | rates |
| `token_lists/ethereum/all.json` | `/token_lists/ethereum/all.json` | **AVAILABLE** | — |  | 856 | keywords, logoURI, name, timestamp, tokens, version |

## ERROR / NOT_FOUND

- `key (account info & usage)` (/key): HTTP 401 code=10005 msg=This request is limited to PRO API subscribers. Please visit https://www.coingecko.com/en/api/pricing to subscribe to our API plan to access exclusive endpoints.
- `coins/list/new (latest 200)` (/coins/list/new): HTTP 401 code=10005 msg=This request is limited to PRO API subscribers. Please visit https://www.coingecko.com/en/api/pricing to subscribe to our API plan to access exclusive endpoints.
- `coins/top_gainers_losers (PAID?)` (/coins/top_gainers_losers): HTTP 401 code=10005 msg=This request is limited to PRO API subscribers. Please visit https://www.coingecko.com/en/api/pricing to subscribe to our API plan to access exclusive endpoints.
- `coins/{id}/ohlc/range (PAID?)` (/coins/bitcoin/ohlc/range): HTTP 401 code=10005 msg=This request is limited to PRO API subscribers. Please visit https://www.coingecko.com/en/api/pricing to subscribe to our API plan to access exclusive endpoints.
- `coins/{id}/circulating_supply_chart (PAID?)` (/coins/bitcoin/circulating_supply_chart): HTTP 401 code=10005 msg=This endpoint is exclusive to Enterprise plan customers only. Contact for Enterprise plan enquiry: https://www.coingecko.com/en/api/pricing 
- `global/market_cap_chart (PAID?)` (/global/market_cap_chart): HTTP 401 code=10005 msg=This request is limited to PRO API subscribers. Please visit https://www.coingecko.com/en/api/pricing to subscribe to our API plan to access exclusive endpoints.
- `onchain/pools/megafilter` (/onchain/pools/megafilter): HTTP 401 code=401 msg=This request is exclusive to Analyst plan or above subscribers only. Upgrade to Analyst plan or above to access: https://www.coingecko.com/en/api/pricing.
- `onchain/networks/eth/tokens/{addr}/top_holders (PAID?)` (/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/top_holders): HTTP 401 code=401 msg=This request is exclusive to Analyst plan or above subscribers only. Upgrade to Analyst plan or above to access: https://www.coingecko.com/en/api/pricing.
- `onchain/networks/eth/tokens/{addr}/holders_chart` (/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/holders_chart): HTTP 401 code=401 msg=This request is exclusive to Analyst plan or above subscribers only. Upgrade to Analyst plan or above to access: https://www.coingecko.com/en/api/pricing.
- `onchain/networks/eth/tokens/{addr}/top_traders` (/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/top_traders): HTTP 401 code=401 msg=This request is exclusive to Analyst plan or above subscribers only. Upgrade to Analyst plan or above to access: https://www.coingecko.com/en/api/pricing.
