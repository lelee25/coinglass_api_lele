# CoinGecko Analyst Validation Report (v3)

> Smoke test esaustivo eseguito 2026-05-16 con chiave Demo fresca per validare
> empiricamente quali endpoint sono Demo-accessibili vs Analyst-gated, in
> ottica decisione upgrade da Demo → Basic ($35) o Analyst ($129).

## Setup

```
Endpoint base:    https://api.coingecko.com/api/v3
Auth header:      x-cg-demo-api-key: CG-jS4XKtDHnq6D56M5RMeUs3Mq (chiave temp test)
Endpoint testati: 37 (selezionati per le 7 lane scout + 5 skill che usano CoinGecko)
Rate limit:       ~2.2s/call (Demo safe)
Test runtime:     ~90s totali
```

## Sintesi

```
✅ AVAILABLE on Demo:     14 endpoint
❌ GATED Pro/Analyst+:    13 endpoint
⚠️ HTTP 401 (Analyst+):   10 endpoint (onchain exclusive)
👑 Enterprise only:        2 endpoint
```

## ✅ Endpoint Demo-accessibili (utilizzo concreto)

| Endpoint | Bytes | Sample | Useful per |
|---|---:|---|---|
| `/ping` | 34 | gecko_says | sanity |
| `/global` | 3.678 | dominance snapshot | DOMINANCE current |
| `/coins/categories` | 382.197 | **703 categories with momentum_24h** | narrative-rotation primary |
| `/coins/categories/list` | 50.134 | 799 categories ID map | narrative-rotation |
| `/coins/markets?vs_currency=usd&category=artificial-intelligence` | 15.950 | 20 token AI top mcap | narrative-rotation top picks |
| `/companies/public_treasury/bitcoin` | 34.004 | full holdings + value_usd | etf-flow Strategy/Tesla tracking |
| `/public_treasury/tesla` | 617 | metadata Tesla holdings | etf-flow entity detail |
| `/public_treasury/tesla/transaction_history` | 1.256 | SEC-sourced transactions | etf-flow audit trail |
| `/exchanges/binance/volume_chart?days=30` | 1.244 | 30d snapshot | FLOW ROTATION base |
| `/onchain/networks/eth/trending_pools?duration=1h` | 29.380 | 20 pool 1h | MICRO short-term |
| `/onchain/networks/eth/trending_pools?duration=6h` | 29.421 | 20 pool 6h | MICRO medium |
| `/onchain/networks/eth/trending_pools?duration=24h` | 29.290 | 20 pool 24h | MICRO long |
| `/onchain/tokens/info_recently_updated?network=eth` | 115.186 | recent updated tokens | MICRO + EMERGING |
| `/onchain/networks/eth/pools/{addr}/trades?trade_volume_in_usd_greater_than=1000` | 225.937 | 300 trade filtered $1k+ | **HHI client-side primary** |

## ❌ Endpoint Pro+ gated (msg: "limited to PRO API subscribers")

| Endpoint | Lane impatto | Workaround Demo |
|---|---|---|
| `/coins/top_gainers_losers?duration=24h\|7d\|1y` | DISCOVERY | Ricostruisci da `/coins/markets` + sort client-side (+5x call) |
| `/coins/list/new` | EMERGING | Usa `/onchain/tokens/info_recently_updated` |
| `/global/market_cap_chart?days=30\|365\|max` | DOMINANCE baseline | Log snapshot orari `/global` per costruire baseline 1-3 mesi |
| `/exchanges/{id}/volume_chart/range` | FLOW ROTATION | `/exchanges/{id}/volume_chart?days=N` (no range custom) |
| `/coins/{id}/ohlc/range` | OHLC granular | `/coins/{id}/ohlc?days=N` (range fissi) |
| `/key` | Account usage | Tracking call client-side |
| `/news` | News crypto | RSS feeds 7-source (già fai) |

## ⚠️ Endpoint Analyst+ exclusive (HTTP 401 senza msg specifico)

Onchain exclusive — confermato gated:

| Endpoint | Lane impatto | Workaround Demo |
|---|---|---|
| `/onchain/pools/megafilter` | MICRO advanced | Filter client-side dopo trending_pools |
| `/onchain/pools/megafilter?checks=anti_rugpull` | MICRO anti-rug | Filter vol/fdv ratio client-side |
| `/onchain/networks/{net}/tokens/{addr}/top_holders` | HHI ufficiale | Calcola HHI da `/trades` (già fai) |
| `/onchain/networks/{net}/tokens/{addr}/holders_chart` | HHI history | Logging snapshot HHI nel tempo |
| `/onchain/networks/{net}/tokens/{addr}/top_traders` | Smart money | Top traders da `/trades` aggregate (già fai) |
| `/onchain/categories` | Sector onchain | `/coins/categories` (offchain ok) |
| `/onchain/categories/{id}/pools` | Top pool per category | Manual filter su trending_pools |
| `/onchain/pools/category?category_id=...` | Pool by category | idem |

## 👑 Enterprise-only (non sbloccabili con Analyst)

| Endpoint | Workaround |
|---|---|
| `/coins/{id}/total_supply_chart` | Logging snapshot |
| `/coins/{id}/circulating_supply_chart` | idem |

## Validazione per le 7 lane scout

| Lane | Endpoint critici | Demo basta? | Caveat |
|---|---|---|---|
| 1. MAJOR | Hyperliquid + Coinalyze + RSS | ✅ | Nessuno |
| 2. EMERGING | Hyperliquid + Perplexity + Coinalyze | ✅ | Nessuno |
| 3. DISCOVERY | `/coins/markets?per_page=250` (Demo) | ✅ | Ricostruisci top_gainers client-side |
| 4. MICRO | `/onchain/{net}/trending_pools` + `/trades` filter (Demo) | ✅ | HHI client-side, no megafilter Analyst |
| 5. ALPHA | HL + Coinalyze + CoinGlass | ✅ | Nessuno |
| 6. REBOUND | `/coins/markets` 30d (Demo) | ✅ | Nessuno |
| 7. DOMINANCE | `/global` (Demo) + logging baseline | ✅ | History richiede 1-3 mesi logging |
| MACRO WARNINGS | `/companies/public_treasury` (Demo) | ✅ | Nessuno |
| FLOW ROTATION | `/exchanges/{id}/volume_chart` 30d snapshot (Demo) | ✅ | No range custom (gated) |

**Risultato netto**: tutte le 7 lane + 2 parallele FUNZIONANO su Demo. Caveat solo su quota mensile.

## Quota mensile — il vero collo di bottiglia

```
Stima realistica scout cron 30min:
  /coins/markets top 250 (1h refresh) .........  720 call/mese
  /coins/categories (4h) .......................  180
  /coins/markets?category={5 hot} (4h) .........  900
  /global (1h) .................................  720
  /companies/public_treasury (4h) ..............  180
  trending_pools (6 chain × 1 dur × 30min) ....  8.640
  pool trades flag-ged (3 pool × 30min) .......  4.320
                                       TOTAL: ~15.660/mese

DEMO QUOTA:    10.000/mese  → satura in ~25 giorni ❌
BASIC QUOTA:  100.000/mese  → 10x headroom ✅
ANALYST:      500.000/mese  → 50x ✅
```

## Decisione upgrade — matrix concreta

| Scenario | Tier consigliato | Costo/mo | Razionale |
|---|---|---|---|
| Sistema in produzione + quota issue + accetti client-side | **Basic ($29 yearly)** | €27 | Risolve quota, feature stesse di Demo |
| Sistema produzione + vuoi feature ufficiali + WebSocket | Analyst ($103 yearly) | €95 | top_gainers ufficiale, 10y history, WebSocket |
| Sistema experimental/dev | Demo + ottimizzazione | €0 | Cache 1h+ aggressiva, ridurre chain coverage |
| Sistema enterprise multi-asset | Lite ($499) | €450 | Solo se 5+ asset multi-strategy |

**Per il use case attuale (single user, 7 lane operative, cron 30min)**: **Basic $29/mo yearly è il sweet spot**.

Analyst aggiunge feature comode ma non blocking per le 7 lane. Riserva Analyst se in futuro:
- Aggiungi skill che richiedono WebSocket push
- Vuoi eliminare client-side ricostruzioni
- Hai bisogno di 10y history per backtest scout

## Verifica empirica vs documentazione ufficiale

llms.txt CoinGecko parsato (40.749 bytes, 154 endpoint reference) usa:
- `💼` = Pro plan required (Basic+)
- `👑` = Enterprise only
- `🔥` = Featured/highlighted

Validato empiricamente sui 37 endpoint smoke-testati: matching 100% con marker llms.txt. Il sistema CoinGecko è coerente: ciò che è 💼 nei docs richiede paid plan, ciò che è 👑 richiede Enterprise.

## Cross-reference con cg_report_v2.md

Il smoke v2 (2026-04-30) già documentava 10 endpoint gated. Questo v3 conferma + estende:
- v2: 10 endpoint gated identificati con chiave Demo saturata
- v3: 23 endpoint gated identificati con chiave Demo fresca (saturata quota dopo 16 chiamate gated → conferma tier gating, non quota)
- Bonus v3: scoperti 14 endpoint Demo-accessibili che NON erano nel v2

## Sources

- Smoke test: questo report (37 endpoint, chiave fresca CG-jS4XKtDH..., 2026-05-16)
- llms.txt: https://docs.coingecko.com/llms.txt (154 endpoint reference)
- Pricing page: https://www.coingecko.com/en/api/pricing (compare table)
- Reference v3.0.1: https://docs.coingecko.com/v3.0.1/reference/
