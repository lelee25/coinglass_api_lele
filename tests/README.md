# tests/ — smoke-test CoinGlass Hobbyist

## `smoke_endpoints.py`

Probe automatico di **46 endpoint** CoinGlass per validare cosa è disponibile
sul piano Hobbyist dell'utente. Classifica ogni endpoint come:

- `AVAILABLE` — risponde 200 OK con `code: 0` e `data` non vuoto
- `AVAILABLE_EMPTY` — risponde 200 OK con `code: 0` ma `data` vuoto (endpoint OK, simbolo/parametro fuori range)
- `GATED` — risponde con `code` di errore + msg che contiene `upgrade`/`plan`/`tier`/`subscribe`
- `RATE_LIMIT` — `code: 50001` (lo script attende 5s e ritenta una volta)
- `ERROR` — altri errori (HTTP 4xx/5xx, codici diversi)
- `NOT_FOUND` — HTTP 404 (path probabilmente cambiato di nome)

### Uso

```bash
# Su mac o sul mini-PC server
export COINGLASS_API_KEY="<la tua chiave Hobbyist>"

# REST only (durata stimata ~1.5 min)
python3 tests/smoke_endpoints.py --out smoke_report.md

# REST + WebSocket probe (richiede `pip install websockets`)
python3 tests/smoke_endpoints.py --out smoke_report.md --ws

# Probare canali WS specifici
python3 tests/smoke_endpoints.py --ws \
  --ws-channel liquidationOrders \
  --ws-channel largeLimitOrder \
  --ws-channel whaleAlert
```

Il report `smoke_report.md` include:
- Sintesi conteggi per classificazione
- Tabella dettaglio per ogni probe (path, classe, code, msg, latenza, sample keys del payload)
- Sezione GATED con sostituti locali (rimanda a `INTEGRATION-NOTES.md` §5)
- Sezione ERROR/NOT_FOUND con path da rivedere
- Sezione WebSocket con primi messaggi raccolti (se `--ws`)

### Cosa probiamo

**Control set** (dovrebbe funzionare su Hobbyist):
- `supported-coins`, `supported-exchange-pairs`, `coins-markets`
- OHLC OI, funding-rate, liquidation-aggregated-history
- long-short ratio, CGDI index
- ETF Bitcoin/Ethereum/HK (list, flow-history, net-assets-history, premium-discount-history)
- Options (info, max-pain, exchange-oi-history)
- Macro (coinbase-premium-index, fear-greed-history, exchange-balance)
- Account subscription

**Da verificare** (probabile gating Standard+):
- `futures/rsi/list`
- `orderbook/heatmap`, `orderbook/large-limit-order`, `orderbook/large-limit-order-history`
- `futures/footprint`
- `liquidation/heatmap/model1?range=1y` (vs `range=180d` per confronto gating-by-param)
- `liquidation/heatmap/model2`, `model3` (community-discovered, vedi INTEGRATION-NOTES §14.1)
- `liquidation/aggregated-heatmap/model3`
- `hyperliquid/whale-alert`, `hyperliquid/whale-position`

**Indici V3 legacy** (potrebbero essere stati rimossi silenziosamente):
- `index/ahr999`, `index/puell_multiple`, `index/golden_ratio_multiplier`
- `index/pi` (Pi Cycle Top), `index/stock_flow` (S2F)
- `index/bitcoin/rainbow-chart`, `index/bitcoin_bubble_index`

**CVD** (mancanti dal `coinglass.md` originale):
- `cvd/history`, `aggregated-cvd/history`

**Taker** (verifica path con/senza prefisso `/v2/`):
- `taker-buy-sell-volume/history` ufficiale
- `v2/taker-buy-sell-volume/history` (probabile refuso del documento)

### Rate limit

Lo script chiama 1 endpoint ogni 2.5s = **24 rpm effettivi** (80% del limite Hobbyist). Esecuzione serializzata, no thread/async sui probe REST.

Se gli altri 3 agenti stanno già consumando il budget mentre giri lo smoke, **fermali prima** o avrai falsi `RATE_LIMIT`.

### Output esempio

```markdown
# CoinGlass smoke-test report — Hobbyist plan

Run time: 2026-04-30 18:55:12 UTC
Probes: 34, rate ~24 rpm

## Sintesi per classificazione
| Classe | Conteggio |
| AVAILABLE | 22 |
| AVAILABLE_EMPTY | 3 |
| GATED | 6 |
| ERROR | 2 |
| NOT_FOUND | 1 |
```

### Cosa NON fa

- Non scrive nulla nel sistema, è read-only
- Non esegue trading, non tocca exchange
- Non parsa risposte oltre la struttura di envelope (`code`, `msg`, `data` keys)
- Non dipende da pacchetti pip oltre la stdlib (eccetto `websockets` se usi `--ws`)

### Quando ri-runnarlo

- Dopo cambio piano (es. upgrade a Startup)
- Ogni 30 giorni per intercettare deprecation o gating change
- Prima di basare un nuovo agente su un endpoint che non hai mai testato
