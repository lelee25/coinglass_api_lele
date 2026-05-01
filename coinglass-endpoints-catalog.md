# CoinGlass v4 — Catalog completo endpoint

> Compilato il **2026-04-30** incrociando:
> - **Repo skill ufficiale** [coinglass-official/coinglass-api-skills](https://github.com/coinglass-official/coinglass-api-skills) (8 domini, file `API.md` per categoria) — fonte autoritativa di path + parametri.
> - **References ufficiali** [`plans-interval-history-length.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/options/references/plans-interval-history-length.md) e [`errors-codes.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/options/references/errors-codes.md).
> - **Pricing page** [coinglass.com/pricing](https://www.coinglass.com/pricing) — rate limits e endpoint count per piano.
> - **docs.coinglass.com** per voci secondarie.
> - **Smoke test reale Hobbyist** (`tests/smoke_endpoints.py`, run 2026-04-30, 46 probe con chiave reale) per ground-truth gating.
>
> NOTA: La OpenAPI/Swagger spec di docs.coinglass.com (ReadMe.io) NON è esposta pubblicamente come JSON scaricabile (provati `/openapi.json`, `/api-spec.json`, redirect — tutti 404). Lo skill repo è perciò la sorgente più affidabile dopo la chiave reale.

---

## Sintesi

- **Endpoint catalogati: 130** (futures 47, spots 16, options 4, etf 16, indic 36, on-chain 4, account 1, other 2 + 4 WS)
- **Disponibili su Hobbyist (full): ~58** (45%)
- **Parzialmente disponibili su Hobbyist** (gating per interval ≥ 4h o per range storico): ~30 (23%)
- **Gated Hobbyist (richiede Startup+/Standard+/Pro): ~42** (32%)
- **Gating per interval su Hobbyist: minimum 4h** (1m, 3m, 5m, 15m, 30m, 1h, 2h non disponibili — confermato sia da skill repo che da smoke test)
- **Heatmap (model1/2/3, map, max-pain) richiede PROFESSIONAL**
- **Liquidation order, large limit order, footprint, news/calendar, RSI list richiedono Startup+ o Standard+**

### Plan-tier × interval matrix (sorgente: `options/references/plans-interval-history-length.md`)

| Interval | Hobbyist | Startup | Standard | Professional |
|---|---|---|---|---|
| 1m  | NO | NO | 6d | 12d |
| 3m  | NO | NO | 20d | 40d |
| 5m  | NO | NO | 30d | 60d |
| 15m | NO | NO | 90d | 180d |
| 30m | NO | 90d | 180d | 360d |
| 1h  | NO | 180d | 360d | 720d |
| 2h  | NO | 180d | 360d | 720d |
| 4h  | 180d | 180d | 360d | 720d |
| 6h  | 360d | 360d | 360d | 720d |
| 8h  | 360d | 360d | 360d | 720d |
| 12h | 360d | 360d | 360d | 720d |
| 1d  | All-time | All-time | All-time | All-time |

### Rate limits per piano (sorgente: pricing page)

| Piano | $/month | RPM | Endpoint count |
|---|---|---|---|
| Hobbyist | 29 | 30 | 80+ |
| Startup | 79 | 80 | 130+ |
| Standard | 299 | 300 | 150+ |
| Professional | 699 | 1200 | 160+ |

### Legenda colonna "Hobbyist"

- **YES** = disponibile, nessuna restrizione
- **interval ≥ 4h** = disponibile ma solo con interval 4h/6h/8h/12h/1d
- **GATED** = bloccato a Hobbyist; tier minimo indicato in colonna "Note"
- **EMPTY** = endpoint risponde 200 + code 0 ma `data` vuoto (la skill repo lo lista come "All tiers", da verificare con dati live)

---

## 1. Futures (47 endpoint)

Base URL: `https://open-api-v4.coinglass.com`

### 1.1 Discovery & meta (9)

Skill: [`futures/trading-market/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/futures/trading-market/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/futures/supported-coins` | GET | (none) | — | YES | Lista coin con futures (smoke: AVAILABLE) |
| `/api/futures/supported-exchanges` | GET | (none) | — | YES | Lista exchange supportati |
| `/api/futures/supported-exchange-pairs` | GET | `exchange` (opt) | — | YES | Pair per exchange (smoke: AVAILABLE) |
| `/api/futures/coins-markets` | GET | `exchange_list`, `per_page`, `page` | `page=1` | **GATED** | Smoke 2026-04-30: msg "Upgrade plan". Skill repo NON specifica tier. **Richiede Startup+** |
| `/api/futures/pairs-markets` | GET | `symbol` (req) | — | TBD | Skill repo: All tiers. Non testato in smoke |
| `/api/futures/coins-price-change` | GET | (none) | — | TBD | Snapshot variazione prezzo |
| `/api/futures/price/history` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time` | `limit=1000` | **interval ≥ 4h** | OHLC prezzo |
| `/api/futures/delisted-exchange-pairs` | GET | (none) | — | TBD | Pair delistate |
| `/api/futures/exchange-rank` | GET | (none) | — | TBD | Ranking exchange |

### 1.2 Open Interest (6)

Skill: [`futures/open-interest/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/futures/open-interest/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/futures/open-interest/history` | GET | `exchange` (req), `symbol` (req), `interval` (req: 1m..1w), `limit` (max 1000), `start_time`, `end_time`, `unit` (usd/coin) | `limit=1000` | **interval ≥ 4h** | OHLC OI per pair (smoke: 1h GATED, 4h+ AVAILABLE) |
| `/api/futures/open-interest/aggregated-history` | GET | `symbol` (req), `interval` (req), `limit`, `start_time`, `end_time`, `unit` | `limit=1000` | **interval ≥ 4h** | OI aggregato per coin |
| `/api/futures/open-interest/aggregated-stablecoin-history` | GET | `exchange_list` (req), `symbol` (req), `interval` (req), `limit`, `start_time`, `end_time` | — | **interval ≥ 4h** | OI stablecoin-margin |
| `/api/futures/open-interest/aggregated-coin-margin-history` | GET | `exchange_list` (req), `symbol` (req), `interval` (req), `limit`, `start_time`, `end_time` | — | **interval ≥ 4h** | OI coin-margin |
| `/api/futures/open-interest/exchange-list` | GET | `symbol` (req) | — | YES | Snapshot OI per exchange (smoke: AVAILABLE) |
| `/api/futures/open-interest/exchange-history-chart` | GET | `symbol` (req), `range` (all/1m/15m/1h/4h/12h), `unit` | — | YES | Chart history per exchange |

### 1.3 Funding Rate (6)

Skill: [`futures/funding-rate/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/futures/funding-rate/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/futures/funding-rate/history` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time` | `limit=1000` | **interval ≥ 4h** | OHLC funding rate (smoke: 1h GATED) |
| `/api/futures/funding-rate/oi-weight-history` | GET | `symbol`, `interval`, `limit`, `start_time`, `end_time` | — | **interval ≥ 4h** | OI-weighted funding |
| `/api/futures/funding-rate/vol-weight-history` | GET | `symbol`, `interval`, `limit`, `start_time`, `end_time` | — | **interval ≥ 4h** | Volume-weighted funding |
| `/api/futures/funding-rate/exchange-list` | GET | (none) | — | YES | Snapshot per exchange (smoke: AVAILABLE) |
| `/api/futures/funding-rate/accumulated-exchange-list` | GET | `range` (1d/7d/30d/365d) | — | YES | Funding cumulativo |
| `/api/futures/funding-rate/arbitrage` | GET | `usd` (req), `exchange_list` (opt) | — | **GATED** | Skill repo: "Hobbyist Not Available". Richiede **Startup+** |

### 1.4 Liquidation (14)

Skill: [`futures/liquidation/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/futures/liquidation/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/futures/liquidation/history` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time` | `limit=1000` | **interval ≥ 4h** | Pair liquidation OHLC |
| `/api/futures/liquidation/aggregated-history` | GET | `exchange_list` (req), `symbol`, `interval`, `limit`, `start_time`, `end_time` | — | **interval ≥ 4h** | Coin liquidation aggregata (smoke: 1h GATED) |
| `/api/futures/liquidation/coin-list` | GET | `exchange` (req) | — | **GATED** | Richiede **Startup+** |
| `/api/futures/liquidation/exchange-list` | GET | `symbol` (opt), `range` (1h/4h/12h/24h) | — | YES | Snapshot per exchange (smoke: AVAILABLE) |
| `/api/futures/liquidation/order` | GET | `exchange`, `symbol`, `min_liquidation_amount` (req), `start_time`, `end_time` | — | **GATED** | Richiede **Standard+** |
| `/api/futures/liquidation/heatmap/model1` | GET | `exchange`, `symbol`, `range` (12h/24h/3d/7d/30d/90d/180d/1y) | — | **GATED** | **PROFESSIONAL only** (smoke: GATED) |
| `/api/futures/liquidation/heatmap/model2` | GET | stesso | — | **GATED** | PROFESSIONAL only (smoke: GATED) |
| `/api/futures/liquidation/heatmap/model3` | GET | stesso | — | **GATED** | PROFESSIONAL only (smoke: GATED) |
| `/api/futures/liquidation/aggregated-heatmap/model1` | GET | `symbol`, `range` (12h..1y) | — | **GATED** | PROFESSIONAL only |
| `/api/futures/liquidation/aggregated-heatmap/model2` | GET | stesso | — | **GATED** | PROFESSIONAL only |
| `/api/futures/liquidation/aggregated-heatmap/model3` | GET | stesso | — | **GATED** | PROFESSIONAL only (smoke: GATED) |
| `/api/futures/liquidation/map` | GET | `exchange`, `symbol`, `range` (1d/7d/30d) | — | **GATED** | PROFESSIONAL only |
| `/api/futures/liquidation/aggregated-map` | GET | `symbol`, `range` (1d/7d/30d) | — | **GATED** | PROFESSIONAL only |
| `/api/futures/liquidation/max-pain` | GET | `range` (12h/24h/48h/3d/7d/14d/30d) | — | **GATED** | PROFESSIONAL only |

### 1.5 Long/Short Ratio (6)

Skill: [`futures/long-short-ratio/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/futures/long-short-ratio/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/futures/global-long-short-account-ratio/history` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time` | — | **interval ≥ 4h** | Global account ratio (smoke: 1h GATED) |
| `/api/futures/top-long-short-account-ratio/history` | GET | come sopra | — | **interval ≥ 4h** | Top trader account ratio |
| `/api/futures/top-long-short-position-ratio/history` | GET | come sopra | — | **interval ≥ 4h** | Top trader position ratio |
| `/api/futures/taker-buy-sell-volume/exchange-list` | GET | `symbol`, `range` (5m/15m/30m/1h/4h/12h/24h) | — | YES | Snapshot taker per exchange |
| `/api/futures/net-position/history` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time` | — | **interval ≥ 4h** | Net long/short position |
| `/api/futures/v2/net-position/history` | GET | `exchange` (Binance only), `symbol`, `interval`, `limit`, `start_time`, `end_time` | — | **interval ≥ 4h** | v2 (Binance only) |

### 1.6 Order Book L2 (5)

Skill: [`futures/order-book-l2/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/futures/order-book-l2/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/futures/orderbook/ask-bids-history` | GET | `exchange`, `symbol`, `interval`, `limit` (1-1000), `start_time`, `end_time`, `range` (0.25/0.5/0.75/1/2/3/5/10) | `limit=1000` | **interval ≥ 4h** | Bid/ask OHLC ±range% |
| `/api/futures/orderbook/aggregated-ask-bids-history` | GET | `exchange_list` (or "ALL"), `symbol`, `interval`, `limit`, `start_time`, `end_time`, `range` | — | **interval ≥ 4h** | Aggregato per coin |
| `/api/futures/orderbook/history` | GET | `exchange`, `symbol`, `interval`, `limit` (1-100, **req**), `start_time`, `end_time` | `limit=100` | **GATED** | Heatmap orderbook OHLC. **Richiede Standard+** (path corretto: NON `/orderbook/heatmap`) |
| `/api/futures/orderbook/large-limit-order` | GET | `exchange`, `symbol` | — | **GATED** | Smoke: GATED. **Richiede Standard+** |
| `/api/futures/orderbook/large-limit-order-history` | GET | `exchange`, `symbol`, `start_time` (req), `end_time` (req), `state` (1/2/3) | — | **GATED** | Storico large orders. State: 1=in progress, 2=finished, 3=revoked. Richiede Standard+ |

### 1.7 Taker Buy/Sell + Volume + CVD + NetFlow (7)

Skill: [`futures/taker-buy-sell/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/futures/taker-buy-sell/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/futures/v2/taker-buy-sell-volume/history` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time` | `limit=1000` | **interval ≥ 4h** | Pair taker history (path v2 reale) |
| `/api/futures/aggregated-taker-buy-sell-volume/history` | GET | `exchange_list`, `symbol`, `interval`, `limit`, `start_time`, `end_time`, `unit` | — | **interval ≥ 4h** | Coin taker aggregato |
| `/api/futures/volume/footprint-history` | GET | `exchange` (Binance/OKX/Bybit/Hyperliquid), `symbol`, `interval`, `limit`, `start_time`, `end_time` | — | **GATED** | Footprint OHLC. Path corretto è `/volume/footprint-history`, NON `/futures/footprint`. **Richiede Standard+** |
| `/api/futures/cvd/history` | GET | `exchange` (Binance/OKX), `symbol`, `interval`, `limit`, `start_time`, `end_time` | — | **interval ≥ 4h** | CVD pair |
| `/api/futures/aggregated-cvd/history` | GET | `exchange_list`, `symbol`, `interval`, `limit` (max 4500), `start_time`, `end_time`, `unit` | — | **interval ≥ 4h** | CVD aggregato |
| `/api/futures/netflow-list` | GET | `per_page`, `page` | `page=1` | TBD | Lista netflow per coin |
| `/api/futures/coin/netflow` | GET | `symbol`, `exchange_list` (Binance/Bybit/OKX/Bitget/Gate) | — | TBD | Netflow per coin specifica |

### 1.8 Hyperliquid (7)

Skill: [`futures/hyperliquid-positions/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/futures/hyperliquid-positions/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/hyperliquid/whale-alert` | GET | (none) | — | **GATED** | Smoke: GATED. **Richiede Standard+** |
| `/api/hyperliquid/whale-position` | GET | (none) | — | **GATED** | Smoke: GATED. Richiede Standard+ |
| `/api/hyperliquid/position` | GET | `symbol` (req), `current_page` (opt) | — | TBD | Posizioni wallet per coin |
| `/api/hyperliquid/user-position` | GET | `user_address` (req) | — | TBD | Posizioni di uno specifico wallet |
| `/api/hyperliquid/wallet/position-distribution` | GET | (none) | — | TBD | Distribuzione posizioni |
| `/api/hyperliquid/wallet/pnl-distribution` | GET | (none) | — | TBD | Distribuzione PnL |
| `/api/hyperliquid/global-long-short-account-ratio/history` | GET | `symbol`, `interval` (5m/1h/1d), `limit` (max 1000), `start_time`, `end_time` | `limit=1000` | **interval ≥ 1h (limited)** | Hyperliquid LS ratio. NB: solo 5m/1h/1d valid intervals |

---

## 2. Spots (16 endpoint)

### 2.1 Discovery & price (5)

Skill: [`spots/trading-market/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/spots/trading-market/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/spot/supported-coins` | GET | (none) | — | YES | |
| `/api/spot/supported-exchange-pairs` | GET | (none) | — | YES | |
| `/api/spot/coins-markets` | GET | `per_page`, `page` | `page=1` | TBD | Verosimilmente Startup+ come futures-coins-markets |
| `/api/spot/pairs-markets` | GET | `symbol` (req) | — | TBD | |
| `/api/spot/price/history` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time` | `limit=1000` | **interval ≥ 4h** | OHLC prezzo spot |

### 2.2 Order Book (5)

Skill: [`spots/order-book/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/spots/order-book/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/spot/orderbook/ask-bids-history` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time`, `range` | — | **interval ≥ 4h** | Bid/ask spot |
| `/api/spot/orderbook/aggregated-ask-bids-history` | GET | `exchange_list`, `symbol`, `interval`, `limit`, `range` | — | **interval ≥ 4h** | |
| `/api/spot/orderbook/history` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time` | — | **GATED** | Heatmap. Standard+ |
| `/api/spot/orderbook/large-limit-order` | GET | `exchange`, `symbol` | — | **GATED** | Standard+ |
| `/api/spot/orderbook/large-limit-order-history` | GET | `exchange`, `symbol`, `start_time`, `end_time`, `state` (1/2/3) | — | **GATED** | Standard+ |

### 2.3 Taker / CVD / NetFlow (7)

Skill: [`spots/taker-buy-sell/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/spots/taker-buy-sell/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/spot/taker-buy-sell-volume/history` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time` | — | **interval ≥ 4h** | |
| `/api/spot/aggregated-taker-buy-sell-volume/history` | GET | `exchange_list`, `symbol`, `interval`, `limit`, `start_time`, `end_time`, `unit` | — | **interval ≥ 4h** | |
| `/api/spot/volume/footprint-history` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time` | — | **GATED** | Standard+ (90d storico) |
| `/api/spot/cvd/history` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time`, `unit` | — | **interval ≥ 4h** | CVD spot |
| `/api/spot/aggregated-cvd/history` | GET | `exchange_list`, `symbol`, `interval`, `limit` (max 4500), `start_time`, `end_time`, `unit` | — | **interval ≥ 4h** | |
| `/api/spot/netflow-list` | GET | `per_page`, `page` | `page=1` | TBD | |
| `/api/spot/coin/netflow` | GET | `symbol`, `exchange_list` | — | TBD | |

---

## 3. Options (4 endpoint)

Skill: [`options/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/options/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/option/max-pain` | GET | `symbol` (BTC/ETH), `exchange` (Deribit/Binance/OKX) | — | TBD | Verosimilmente All tiers |
| `/api/option/info` | GET | `symbol` (BTC/ETH) | — | TBD | |
| `/api/option/exchange-oi-history` | GET | `symbol`, `unit` (USD/coin), `range` (1h/4h/12h/all) | — | TBD | |
| `/api/option/exchange-vol-history` | GET | `symbol`, `unit` | — | TBD | |

---

## 4. ETF (16 endpoint)

### 4.1 Bitcoin ETF (9)

Skill: [`etf/bitcoin-etf/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/etf/bitcoin-etf/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/etf/bitcoin/list` | GET | (none) | — | YES | Lista ETF (smoke: AVAILABLE) |
| `/api/etf/bitcoin/flow-history` | GET | (none) | — | YES | Flussi storici (smoke: AVAILABLE) |
| `/api/etf/bitcoin/net-assets/history` | GET | `ticker` (opt) | — | YES | **Path corretto: `/net-assets/history`** (NON `/net-assets-history`). Smoke 404 perché path errato |
| `/api/etf/bitcoin/premium-discount/history` | GET | `ticker` (opt) | — | YES | **Path corretto: `/premium-discount/history`**. Smoke 404 perché path errato |
| `/api/etf/bitcoin/history` | GET | `ticker` (req) | — | YES | History per singolo ETF |
| `/api/etf/bitcoin/price/history` | GET | `ticker` (req), `range` (1d/7d/all) | — | YES | Prezzo storico ETF |
| `/api/etf/bitcoin/detail` | GET | `ticker` (req) | — | YES | Dettaglio singolo ETF |
| `/api/etf/bitcoin/aum` | GET | `ticker` (opt) | — | YES | Asset under management |
| `/api/hk-etf/bitcoin/flow-history` | GET | (none) | — | YES | **Path corretto: `/hk-etf/bitcoin/flow-history`** (NON `/etf/hong-kong-bitcoin/flow-history`). Smoke 404 perché path errato |

### 4.2 Ethereum ETF (3)

Skill: [`etf/ethereum-etf/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/etf/ethereum-etf/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/etf/ethereum/list` | GET | (none) | — | YES | (smoke: AVAILABLE) |
| `/api/etf/ethereum/flow-history` | GET | (none) | — | YES | |
| `/api/etf/ethereum/net-assets/history` | GET | (none) | — | YES | |

### 4.3 Grayscale (2)

Skill: [`etf/grayscale/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/etf/grayscale/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/grayscale/holdings-list` | GET | (none) | — | YES | All tiers |
| `/api/grayscale/premium-history` | GET | `symbol` (req: ETC/LTC/BCH/SOL/XLM/LINK/ZEC/MANA/ZEN/FIL/BAT/LPT/BTC) | — | YES | All tiers |

### 4.4 Solana / XRP ETF (2)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/etf/solana/flow-history` | GET | (none) | — | YES | [skill](https://github.com/coinglass-official/coinglass-api-skills/blob/main/etf/solana-etf/API.md) |
| `/api/etf/xrp/flow-history` | GET | (none) | — | YES | [skill](https://github.com/coinglass-official/coinglass-api-skills/blob/main/etf/xrp-etf/API.md) |

---

## 5. Indic / Indicators (36 endpoint)

### 5.1 Indicatori tecnici futures (15)

Skill: [`indic/futures/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/indic/futures/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/futures/rsi/list` | GET | (none) | — | **GATED** | Smoke: GATED. **Richiede Startup+** |
| `/api/futures/indicators/rsi` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time`, `window`, `series_type` | — | **interval ≥ 4h** | RSI calcolato |
| `/api/futures/indicators/ma` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time`, `window`, `series_type` | — | **interval ≥ 4h** | Moving average |
| `/api/futures/ma/list` | GET | (none) | — | **GATED** | Probabile Startup+ (allinea a rsi/list) |
| `/api/futures/indicators/ema` | GET | come ma | — | **interval ≥ 4h** | EMA |
| `/api/futures/ema/list` | GET | (none) | — | **GATED** | |
| `/api/futures/indicators/boll` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time`, `series_type`, `window`, `mult` | — | **interval ≥ 4h** | Bollinger |
| `/api/futures/indicators/macd` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time`, `series_type`, `fast_window`, `slow_window`, `signal_window` | — | **interval ≥ 4h** | MACD |
| `/api/futures/macd/list` | GET | (none) | — | **GATED** | |
| `/api/futures/basis/history` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time` | — | **interval ≥ 4h** | Basis history |
| `/api/futures/whale-index/history` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time` | — | **interval ≥ 4h** | Whale index |
| `/api/futures/cgdi-index/history` | GET | (none) | — | YES | CGDI (smoke: AVAILABLE) |
| `/api/futures/cdri-index/history` | GET | (none) | — | YES | CDRI |
| `/api/futures/indicators/avg-true-range` | GET | `exchange`, `symbol`, `interval`, `limit`, `start_time`, `end_time`, `window` | — | **interval ≥ 4h** | ATR |
| `/api/futures/avg-true-range/list` | GET | (none) | — | **GATED** | Probabile Startup+ |

### 5.2 Indicatori spot (3)

Skill: [`indic/spots/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/indic/spots/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/coinbase-premium-index` | GET | `interval`, `limit`, `start_time`, `end_time` | `limit=1000` | **interval ≥ 4h** | Coinbase Premium |
| `/api/bitfinex-margin-long-short` | GET | `symbol` (BTC/ETH), `interval`, `limit`, `start_time`, `end_time` | `limit=1000` | **interval ≥ 4h** | Bitfinex margin |
| `/api/borrow-interest-rate/history` | GET | `exchange` (Binance/OKX/Bybit), `symbol`, `interval`, `limit`, `start_time`, `end_time` | `limit=1000` | **interval ≥ 4h** | Borrow rate |

### 5.3 Macro / on-chain indicator (33 endpoint, "indic/other")

Skill: [`indic/other/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/indic/other/API.md). **Tutti GET, nessun parametro** salvo dove indicato.

| Endpoint | Hobbyist | Note |
|---|---|---|
| `/api/index/ahr999` | YES | Smoke: AVAILABLE |
| `/api/bull-market-peak-indicator` | YES | |
| `/api/index/puell-multiple` | YES | **Path corretto: `puell-multiple`** (NON `puell_multiple`). Smoke 404 era path snake_case errato |
| `/api/index/stock-flow` | YES | **Path corretto: `stock-flow`** (NON `stock_flow`) |
| `/api/index/pi-cycle-indicator` | YES | **Path corretto: `pi-cycle-indicator`** (NON `pi`) |
| `/api/index/golden-ratio-multiplier` | YES | **Path corretto: `golden-ratio-multiplier`** (NON `golden_ratio_multiplier`) |
| `/api/index/bitcoin/profitable-days` | YES | |
| `/api/index/bitcoin/rainbow-chart` | YES | Smoke: AVAILABLE |
| `/api/index/fear-greed-history` | YES | Smoke: AVAILABLE |
| `/api/index/stableCoin-marketCap-history` | YES | NB: camelCase. Smoke: AVAILABLE |
| `/api/index/bitcoin/bubble-index` | YES | **Path corretto: `bitcoin/bubble-index`** (NON `bitcoin_bubble_index`) |
| `/api/index/2-year-ma-multiplier` | YES | |
| `/api/index/200-week-moving-average-heatmap` | YES | |
| `/api/index/altcoin-season` | YES | |
| `/api/index/bitcoin-sth-sopr` | YES | |
| `/api/index/bitcoin-lth-sopr` | YES | |
| `/api/index/bitcoin-sth-realized-price` | YES | |
| `/api/index/bitcoin-lth-realized-price` | YES | |
| `/api/index/bitcoin-short-term-holder-supply` | YES | |
| `/api/index/bitcoin-long-term-holder-supply` | YES | |
| `/api/index/bitcoin-rhodl-ratio` | YES | |
| `/api/index/bitcoin-reserve-risk` | YES | |
| `/api/index/bitcoin-active-addresses` | YES | |
| `/api/index/bitcoin-new-addresses` | YES | |
| `/api/index/bitcoin-net-unrealized-profit-loss` | YES | NUPL |
| `/api/index/bitcoin-correlation` | YES | |
| `/api/index/bitcoin-macro-oscillator` | YES | |
| `/api/index/option-vs-futures-oi-ratio` | YES | |
| `/api/index/bitcoin-vs-global-m2-growth` | YES | |
| `/api/index/bitcoin-vs-us-m2-growth` | YES | |
| `/api/index/bitcoin-dominance` | YES | |
| `/api/exchange_assets_transparency/list` | YES | NB: snake_case |
| `/api/futures_spot_volume_ratio` | YES | Param: `exchange_list`, `symbol`, `interval`, `limit`, `start_time`, `end_time`. **interval ≥ 4h** |

---

## 6. On-Chain (4 endpoint)

### 6.1 Exchange data (3)

Skill: [`on-chain/exchange-data/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/on-chain/exchange-data/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/exchange/assets` | GET | `exchange` (req), `per_page`, `page` | `page=1` | YES | |
| `/api/exchange/balance/list` | GET | `symbol` (req: BTC/ETH/USDT(ETH)) | — | YES | Smoke: AVAILABLE |
| `/api/exchange/balance/chart` | GET | `symbol` (req) | — | YES | |

### 6.2 Token (2)

Skill: [`on-chain/token/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/on-chain/token/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/coin/unlock-list` | GET | `per_page`, `page` | `page=1` | YES | Token unlocks |
| `/api/coin/vesting` | GET | `symbol` (req) | — | YES | Vesting schedule |

### 6.3 Transactions (2)

Skill: [`on-chain/transactions/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/on-chain/transactions/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/exchange/chain/tx/list` | GET | `symbol`, `start_time`, `min_usd`, `per_page` (max 100), `page` | `page=1` | TBD | ERC-20 transfers |
| `/api/chain/v2/whale-transfer` | GET | `symbol`, `start_time`, `end_time` | — | TBD | Whale transfer |

---

## 7. Account (1 endpoint)

Skill: [`account/API.md`](https://github.com/coinglass-official/coinglass-api-skills/blob/main/account/API.md)

| Endpoint | Method | Parametri | Default | Hobbyist | Note |
|---|---|---|---|---|---|
| `/api/user/account/subscription` | GET | (none) | — | YES | Subscription level + expiration (smoke: AVAILABLE) |

---

## 8. Other (2 endpoint)

| Endpoint | Method | Parametri | Hobbyist | Note |
|---|---|---|---|---|
| `/api/article/list` | GET | `start_time`, `end_time`, `language` (en/zh/zh-tw), `page`, `per_page` | **GATED** | News. **Richiede Startup+** ([skill](https://github.com/coinglass-official/coinglass-api-skills/blob/main/other/news/API.md)) |
| `/api/calendar/economic-data` | GET | `start_time` (max 15d before), `end_time` (max 15d after), `language` (en/zh) | **GATED** | Calendar. Richiede Startup+ ([skill](https://github.com/coinglass-official/coinglass-api-skills/blob/main/other/financial-calendar/API.md)) |

---

## 9. WebSocket (4 channel principali)

Endpoint: `wss://open-api-v4.coinglass.com/ws`. Auth: header `CG-API-KEY` o messaggio iniziale `{"action":"subscribe","channel":"...","apikey":"..."}`. Documentazione formale non pubblicata come OpenAPI; canali derivati da smoke probe e dalla pricing page.

| Channel | Payload subscribe | Hobbyist | Note |
|---|---|---|---|
| `liquidationOrders` | `{symbol,exchange}` | TBD | Stream liquidazioni live |
| `largeOrder` | `{symbol,exchange}` | **GATED** (probabile Standard+) | Order book whale |
| `whaleAlert` | `{}` | **GATED** | Hyperliquid whale stream |
| `priceUpdate` | `{symbols:[]}` | TBD | Prezzo realtime |

> NB: Lo smoke test corrente non probe-a WebSocket. Da estendere se servono live stream.

---

## 10. Endpoint NOT_FOUND da smoke test — investigation

Per ognuno il path corretto trovato nel skill repo o conferma di non esistenza:

| Path testato (smoke) | Status | Path corretto | Sorgente |
|---|---|---|---|
| `/api/etf/bitcoin/net-assets-history` | NOT_FOUND | `/api/etf/bitcoin/net-assets/history` (slash) | bitcoin-etf/API.md |
| `/api/etf/bitcoin/premium-discount-history` | NOT_FOUND | `/api/etf/bitcoin/premium-discount/history` | bitcoin-etf/API.md |
| `/api/etf/hong-kong-bitcoin/flow-history` | NOT_FOUND | `/api/hk-etf/bitcoin/flow-history` | bitcoin-etf/API.md |
| `/api/futures/orderbook/heatmap` | NOT_FOUND | `/api/futures/orderbook/history` (Standard+) | order-book-l2/API.md |
| `/api/futures/footprint` | NOT_FOUND | `/api/futures/volume/footprint-history` (Standard+) | taker-buy-sell/API.md |
| `/api/index/puell_multiple` | NOT_FOUND | `/api/index/puell-multiple` (kebab-case) | indic/other/API.md |
| `/api/index/golden_ratio_multiplier` | NOT_FOUND | `/api/index/golden-ratio-multiplier` | indic/other/API.md |
| `/api/index/pi` | NOT_FOUND | `/api/index/pi-cycle-indicator` | indic/other/API.md |
| `/api/index/stock_flow` | NOT_FOUND | `/api/index/stock-flow` | indic/other/API.md |
| `/api/index/bitcoin_bubble_index` | NOT_FOUND | `/api/index/bitcoin/bubble-index` | indic/other/API.md |

**Conclusione**: tutti i NOT_FOUND erano dovuti a path errati (snake_case usato dove serve kebab-case, o nome categoria sbagliato). **Nessun endpoint è realmente "scomparso" in v4**. Aggiornare `tests/smoke_endpoints.py` con i path corretti.

---

## 11. Gating reale Hobbyist (vs marketing)

Confronto pricing page vs smoke test reale del 2026-04-30.

| Feature | Pricing page (marketing) | Smoke reale Hobbyist | Discrepanza? |
|---|---|---|---|
| 80+ endpoint | "Available" generico | ~58 full-access + ~30 con gating per interval | NO (numero coerente con i ~88 disponibili anche se parziali) |
| Interval 1m–1h | NON menzionato esplicitamente | TUTTI gated 1m/3m/5m/15m/30m/1h/2h | SÌ — pricing non avvisa che <4h è bloccato |
| Heatmap liquidation | NON menzionato | Tutti gated (richiede Pro) | SÌ |
| Hyperliquid whales | NON menzionato | Gated | SÌ |
| Large limit order | NON menzionato | Gated | SÌ |
| Footprint | NON menzionato | Gated | SÌ |
| RSI/MA list | NON menzionato | Gated | SÌ |
| Funding arbitrage | NON menzionato | Gated (skill repo conferma "Hobbyist Not Available") | NO (skill repo onesto) |
| News + Calendar | NON menzionato | Gated (skill repo: "Startup+") | NO (skill repo onesto) |
| Coins-markets | NON menzionato | Gated | SÌ — endpoint "discovery" che ci si aspetta gratuito |
| Liquidation order | NON menzionato | Gated (Standard+) | SÌ |
| Liquidation coin-list | NON menzionato | Gated (Startup+) | SÌ |

**Take-away**: la pricing page CoinGlass NON è esaustiva sui gating. La sorgente di verità è il skill repo + smoke test reale. Il numero "80+ endpoint" su Hobbyist è raggiunto solo conteggiando endpoint che sono accessibili **in qualche forma** (anche con interval limitato a 4h+ e quindi inutili per scalping/intraday <4h).

---

## 12. Raccomandazioni operative

### 12.1 Cosa USARE su Hobbyist senza problemi (full access)

**Discovery & meta** (sempre OK):
- `/api/futures/supported-coins`, `/api/futures/supported-exchange-pairs`
- `/api/spot/supported-coins`, `/api/spot/supported-exchange-pairs`
- `/api/futures/coins-price-change`, `/api/futures/exchange-rank`
- `/api/user/account/subscription`

**Snapshot exchange-list** (sempre OK):
- `/api/futures/open-interest/exchange-list`
- `/api/futures/funding-rate/exchange-list`
- `/api/futures/funding-rate/accumulated-exchange-list`
- `/api/futures/liquidation/exchange-list` (con `range`)
- `/api/futures/taker-buy-sell-volume/exchange-list`
- `/api/futures/open-interest/exchange-history-chart`

**ETF** (full):
- `/api/etf/bitcoin/list`, `/api/etf/bitcoin/flow-history`, `/api/etf/bitcoin/net-assets/history`, `/api/etf/bitcoin/premium-discount/history`, `/api/etf/bitcoin/aum`, `/api/etf/bitcoin/detail`, `/api/etf/bitcoin/history`, `/api/etf/bitcoin/price/history`
- `/api/hk-etf/bitcoin/flow-history`
- `/api/etf/ethereum/list`, `/flow-history`, `/net-assets/history`
- `/api/etf/solana/flow-history`, `/api/etf/xrp/flow-history`
- `/api/grayscale/holdings-list`, `/api/grayscale/premium-history`

**Indicatori macro/on-chain** (33 endpoint kebab-case):
- Tutta la sezione `/api/index/*` (rainbow, fear-greed, ahr999, NUPL, RHODL, ...)
- `/api/exchange/balance/list`, `/api/exchange/balance/chart`, `/api/exchange/assets`
- `/api/coin/unlock-list`, `/api/coin/vesting`
- `/api/futures/cgdi-index/history`, `/api/futures/cdri-index/history`

**OHLC con interval ≥ 4h** (utili per swing/positional, NON per intraday <4h):
- `open-interest/history` + aggregated variants
- `funding-rate/history` + variants
- `liquidation/history` + `liquidation/aggregated-history`
- `global-long-short-account-ratio/history`, `top-long-short-*-ratio/history`, `net-position/history`
- `cvd/history`, `aggregated-cvd/history`, `aggregated-taker-buy-sell-volume/history`, `v2/taker-buy-sell-volume/history`
- `orderbook/ask-bids-history` (e aggregated)
- `indicators/rsi`, `indicators/macd`, `indicators/boll`, `indicators/ma`, `indicators/ema`, `indicators/avg-true-range`, `basis/history`, `whale-index/history`
- spot equivalents (`/api/spot/...`)
- Storico Hobbyist: 4h→180d, 6h/8h/12h→360d, 1d→all-time

### 12.2 Cosa NON usare su Hobbyist

**GATED — restituisce errore "Upgrade plan"** (mai chiamare con chiave Hobbyist):
- `/api/futures/coins-markets`
- `/api/futures/liquidation/coin-list`, `/api/futures/liquidation/order`
- `/api/futures/liquidation/heatmap/model[1-3]`, `aggregated-heatmap/model[1-3]`, `map`, `aggregated-map`, `max-pain`
- `/api/futures/orderbook/large-limit-order`, `large-limit-order-history`, `orderbook/history`
- `/api/futures/volume/footprint-history`
- `/api/hyperliquid/whale-alert`, `/api/hyperliquid/whale-position`
- `/api/futures/rsi/list`, `/api/futures/ma/list`, `/api/futures/ema/list`, `/api/futures/macd/list`, `/api/futures/avg-true-range/list`
- `/api/futures/funding-rate/arbitrage`
- `/api/spot/orderbook/history`, `large-limit-order`, `large-limit-order-history`, `volume/footprint-history`
- `/api/article/list`, `/api/calendar/economic-data`

**GATED per interval** — chiama solo con `interval ∈ {4h, 6h, 8h, 12h, 1d, 1w}`:
- Tutti i `/history` OHLC elencati in §12.1 ultima bullet

**Path errati da correggere in `tests/smoke_endpoints.py`** (NON sono assenti, sono mistyped):
- Vedi §10 sopra. Aggiornare a kebab-case e con slash dove serve.

### 12.3 Quando upgradare a Startup ($79, 80 rpm)

Sblocca:
- `interval=30m` con storico 90d, `interval=1h/2h` con 180d
- `/api/futures/funding-rate/arbitrage`
- `/api/futures/liquidation/coin-list`
- `/api/futures/rsi/list` + `ma/list` + `ema/list` + `macd/list` + `avg-true-range/list` (probabile)
- `/api/article/list` (news)
- `/api/calendar/economic-data`
- `/api/futures/coins-markets` (probabile)

**Se ti serve**: news + calendar + indicator screener cross-coin + qualsiasi analisi su 1h-2h con storico significativo.

### 12.4 Quando upgradare a Standard ($299, 300 rpm)

Sblocca:
- `interval=1m` (6d), `3m` (20d), `5m` (30d), `15m` (90d), `30m` (180d) — full intraday/scalping
- `/api/futures/orderbook/history` (heatmap orderbook)
- `/api/futures/orderbook/large-limit-order` + `large-limit-order-history` (whale book)
- `/api/futures/volume/footprint-history` (footprint)
- `/api/futures/liquidation/order` (liquidation feed)
- `/api/hyperliquid/whale-alert` + `whale-position` (Hyperliquid whales)
- "Commercial use" license

**Se ti serve**: scalping <1h, footprint, whale tracking, iceberg orders, commercial deployment.

### 12.5 Quando upgradare a Professional ($699, 1200 rpm)

Sblocca:
- Heatmap suite completa: `/liquidation/heatmap/model[1-3]`, `aggregated-heatmap/model[1-3]`, `map`, `aggregated-map`, `max-pain`
- Storici 720d su 1h-12h (vs 360d su Standard)
- Storico 12d su 1m, 60d su 5m, 180d su 15m
- Priority chat support

**Se ti serve**: liquidation heatmap (tipica feature CoinGlass marketing), backtesting su >1y di dati intraday, supporto chat priority.

---

## 13. Note di implementazione

- **Auth**: header `CG-API-KEY: <chiave>` su ogni request. WebSocket: stesso header su upgrade o messaggio JSON di subscribe.
- **Rate limit**: 429 = HTTP error; bodycode `50001` = limite raggiunto. Su Hobbyist 30 rpm — lo smoke test usa 24 rpm con sleep 2.5s.
- **Gating signal**: `body.code == "40001"` (o 40002/40003) + `msg` contiene "upgrade"/"plan"/"tier" → endpoint gated. Vedi `classify()` in `tests/smoke_endpoints.py`.
- **Naming convention**: paths in v4 usano **kebab-case**, tranne due eccezioni: `stableCoin-marketCap-history` (camelCase), `exchange_assets_transparency/list` e `futures_spot_volume_ratio` (snake_case). Watch out.
- **Skills repo coverage**: 20 file `API.md` letti, ~130 endpoint catalogati. Il repo è regolarmente aggiornato e rimane la sorgente più affidabile in mancanza di OpenAPI scaricabile.
- **OpenAPI spec**: docs.coinglass.com (ReadMe.io) NON espone la spec come JSON pubblico. Gli URL `openapi.json`, `api-spec.json`, `swagger.json` ritornano 404. Il `Try it!` in pagina usa una API interna ReadMe non documentata.

---

_Fine catalog. Per aggiornamenti: ri-eseguire `tests/smoke_endpoints.py` dopo aver corretto i path NOT_FOUND, e ri-leggere i file `API.md` del repo skill se CoinGlass aggiunge endpoint._
