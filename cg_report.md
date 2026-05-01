# CoinGecko Demo API smoke-test report

Run: 2026-04-30 18:20:53 UTC
Base URL: `https://api.coingecko.com/api/v3` — header `x-cg-demo-api-key`
Probes: **46**, rate ~27 rpm

## Sintesi per classificazione

| Classe | Conteggio |
|---|---:|
| AVAILABLE | 36 |
| AVAILABLE_EMPTY | 0 |
| GATED | 0 |
| RATE_LIMIT | 0 |
| BAD_PARAMS | 0 |
| ERROR | 10 |
| NOT_FOUND | 0 |

## Dettaglio

| Endpoint | Path | Class | code | msg | ms | sample keys |
|---|---|---|---|---|---:|---|
| `ping` | `/ping` | **AVAILABLE** | — |  | 526 | gecko_says |
| `key (account info & usage)` | `/key` | **ERROR** | 10005 | This request is limited to PRO API subscribers. Please visit | 372 | status |
| `simple/price BTC,ETH` | `/simple/price` | **AVAILABLE** | — |  | 418 | bitcoin, ethereum |
| `simple/supported_vs_currencies` | `/simple/supported_vs_currencies` | **AVAILABLE** | — |  | 281 | — |
| `simple/token_price (USDT eth)` | `/simple/token_price/ethereum` | **AVAILABLE** | — |  | 402 | 0xdac17f958d2ee523a2206206994597c13d831ec7 |
| `coins/list (universe)` | `/coins/list` | **AVAILABLE** | — |  | 732 | id, name, symbol |
| `coins/list/new (latest 200)` | `/coins/list/new` | **ERROR** | 10005 | This request is limited to PRO API subscribers. Please visit | 463 | status |
| `coins/markets Top 250` | `/coins/markets` | **AVAILABLE** | — |  | 548 | ath, ath_change_percentage, ath_date, atl, atl_change_percentage, atl_date |
| `coins/top_gainers_losers (PAID?)` | `/coins/top_gainers_losers` | **ERROR** | 10005 | This request is limited to PRO API subscribers. Please visit | 386 | status |
| `coins/{id} bitcoin` | `/coins/bitcoin` | **AVAILABLE** | — |  | 392 | additional_notices, asset_platform_id, block_time_in_minutes, categories, country_origin, description |
| `coins/{id}/tickers BTC` | `/coins/bitcoin/tickers` | **AVAILABLE** | — |  | 423 | name, tickers |
| `coins/{id}/market_chart 30d` | `/coins/bitcoin/market_chart` | **AVAILABLE** | — |  | 427 | market_caps, prices, total_volumes |
| `coins/{id}/market_chart/range` | `/coins/bitcoin/market_chart/range` | **AVAILABLE** | — |  | 551 | market_caps, prices, total_volumes |
| `coins/{id}/ohlc 30d` | `/coins/bitcoin/ohlc` | **AVAILABLE** | — |  | 354 | — |
| `coins/{id}/ohlc/range (PAID?)` | `/coins/bitcoin/ohlc/range` | **ERROR** | 10005 | This request is limited to PRO API subscribers. Please visit | 378 | status |
| `coins/{id}/circulating_supply_chart (PAID?)` | `/coins/bitcoin/circulating_supply_chart` | **ERROR** | 10005 | This endpoint is exclusive to Enterprise plan customers only | 395 | status |
| `coins/{id}/history (DD-MM-YYYY)` | `/coins/bitcoin/history` | **AVAILABLE** | — |  | 395 | community_data, developer_data, id, image, localization, market_data |
| `search/trending` | `/search/trending` | **AVAILABLE** | — |  | 263 | categories, coins, nfts |
| `search?query=solana` | `/search` | **AVAILABLE** | — |  | 346 | categories, coins, exchanges, icos, nfts |
| `coins/categories/list` | `/coins/categories/list` | **AVAILABLE** | — |  | 940 | category_id, name |
| `coins/categories` | `/coins/categories` | **AVAILABLE** | — |  | 636 | content, id, market_cap, market_cap_change_24h, name, top_3_coins |
| `global` | `/global` | **AVAILABLE** | — |  | 368 | data |
| `global/decentralized_finance_defi` | `/global/decentralized_finance_defi` | **AVAILABLE** | — |  | 465 | data |
| `global/market_cap_chart (PAID?)` | `/global/market_cap_chart` | **ERROR** | 10005 | This request is limited to PRO API subscribers. Please visit | 460 | status |
| `exchanges (page1)` | `/exchanges` | **AVAILABLE** | — |  | 487 | country, description, has_trading_incentive, id, image, name |
| `exchanges/list` | `/exchanges/list` | **AVAILABLE** | — |  | 618 | id, name |
| `exchanges/{id}/tickers Binance` | `/exchanges/binance/tickers` | **AVAILABLE** | — |  | 657 | name, tickers |
| `derivatives` | `/derivatives` | **AVAILABLE** | — |  | 1547 | basis, contract_type, expired_at, funding_rate, index, index_id |
| `derivatives/exchanges` | `/derivatives/exchanges` | **AVAILABLE** | — |  | 445 | country, description, id, image, name, number_of_futures_pairs |
| `companies/public_treasury bitcoin` | `/companies/public_treasury/bitcoin` | **AVAILABLE** | — |  | 392 | companies, market_cap_dominance, total_holdings, total_value_usd |
| `nfts/list` | `/nfts/list` | **AVAILABLE** | — |  | 390 | asset_platform_id, contract_address, id, name, symbol |
| `asset_platforms` | `/asset_platforms` | **AVAILABLE** | — |  | 514 | chain_identifier, id, image, name, native_coin_id, shortname |
| `onchain/networks` | `/onchain/networks` | **AVAILABLE** | — |  | 662 | data, links |
| `onchain/networks/eth/dexes` | `/onchain/networks/eth/dexes` | **AVAILABLE** | — |  | 425 | data, links |
| `onchain/networks/trending_pools` | `/onchain/networks/trending_pools` | **AVAILABLE** | — |  | 921 | data |
| `onchain/networks/eth/new_pools` | `/onchain/networks/eth/new_pools` | **AVAILABLE** | — |  | 704 | data |
| `onchain/networks/eth/trending_pools` | `/onchain/networks/eth/trending_pools` | **AVAILABLE** | — |  | 723 | data |
| `onchain/pools/megafilter` | `/onchain/pools/megafilter` | **ERROR** | 401 | This request is exclusive to Analyst plan or above subscribe | 370 | status |
| `onchain/simple/networks/eth/token_price USDT` | `/onchain/simple/networks/eth/token_price/0xdac17f958d2ee523a2206206994597c13d831ec7` | **AVAILABLE** | — |  | 564 | data |
| `onchain/networks/eth/tokens/{addr} USDT` | `/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7` | **AVAILABLE** | — |  | 548 | data |
| `onchain/networks/eth/tokens/{addr}/info` | `/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/info` | **AVAILABLE** | — |  | 742 | data |
| `onchain/networks/eth/tokens/{addr}/top_holders (PAID?)` | `/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/top_holders` | **ERROR** | 401 | This request is exclusive to Analyst plan or above subscribe | 467 | status |
| `onchain/networks/eth/tokens/{addr}/holders_chart` | `/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/holders_chart` | **ERROR** | 401 | This request is exclusive to Analyst plan or above subscribe | 472 | status |
| `onchain/networks/eth/tokens/{addr}/top_traders` | `/onchain/networks/eth/tokens/0xdac17f958d2ee523a2206206994597c13d831ec7/top_traders` | **ERROR** | 401 | This request is exclusive to Analyst plan or above subscribe | 448 | status |
| `onchain/networks/eth/pools/{addr}/trades` | `/onchain/networks/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/trades` | **AVAILABLE** | — |  | 1087 | data |
| `onchain/networks/eth/pools/{addr}/ohlcv/hour` | `/onchain/networks/eth/pools/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640/ohlcv/hour` | **AVAILABLE** | — |  | 613 | data, meta |

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
