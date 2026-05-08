# gex-agentkit / tradevalue — base informativa multi-agent trading crypto

> **Per il Claude Code sul server (mini-PC Ubuntu via SSH)**
>
> ## ⚠️ COSA È E COSA NON È QUESTO REPO
>
> **QUESTO REPO È**: documentazione + smoke test + skill markdown.
> Una **base informativa** che precede l'implementazione.
>
> **QUESTO REPO NON È**: il sistema vivo. Non contiene il codice operativo
> dell'agent automatico (gex-analyst esegue trade automatici sul server, è
> codice tuo, NON in questo repo).
>
> ## REGOLA D'ORO PER IL CLAUDE SERVER
>
> 1. **PRIMA** leggi cosa già esiste e funziona sul server (gex-analyst attuale,
>    file di stato, logica già validata, fonti dati già usate)
> 2. **POI** leggi questo repo come riferimento di sostanza
> 3. **CONFRONTA** le 16 skill markdown con la logica già operativa
> 4. **MIGLIORA o INTEGRA** dove ha senso, **NON DUPLICARE** quello che già
>    funziona (es. se il sistema attuale produce già GEX/LW da una fonte
>    sua, non rifarlo da zero "perché la skill suggerisce X")
> 5. **VERIFICA EMPIRICAMENTE** prima di assumere — i smoke test sono
>    riproducibili in `tests/`
>
> ## Le skill sono SOSTANZA, non IMPLEMENTAZIONE
>
> Le 16 skill markdown distillano logica di trading professionale + esperienza
> retrospettiva. **Sono il "come ragionare", non il "come eseguire".** Il
> Claude server le legge come framework di ragionamento e le adatta al sistema
> reale (codice, persistenza, fonti dati, vincoli operativi) che conosce
> meglio di chi le ha scritte.
>
> Non implementare meccanicamente — usa giudizio. Se una skill suggerisce
> dato X da fonte Y ma il sistema reale ha già X da fonte Z funzionante,
> mantieni Z e adatta la skill.
>
> Tutti i dati, le skill, le architetture qui contenute sono **verificate
> empiricamente**: ogni endpoint API è smoke-testato, ogni dipendenza esterna
> validata. Non implementare senza prima leggere — c'è 1+ mese di research
> condensato qui. Lo scopo è risparmiarti i buchi a sorpresa, non dettare
> il codice.

---

## TL;DR — Stato del repo

```
✅ TESTATO EMPIRICAMENTE:
   170+ endpoint API (CoinGlass + CoinGecko + Coinalyze + Hyperliquid)
   2 fonti calendar economico (investpy + Forex Factory)
   7 RSS feeds crypto news
   2 WebSocket pubblici (Bitget + Binance)
   Bypass anti-bot Cloudflare 1010 documentato

✅ SPECIFICATO COMPLETAMENTE:
   16 skill markdown (sostanza ragionamento agent)
   9 reference (logica supporto + 2 spec moduli Python)
   4 agent dimensionati (jarvis-main, gex-analyst, macro-master, sentinel-agent)
   Pipeline cron + tool precostruiti + file system convention

⏳ DA FARE (tuo lavoro, Claude server):
   Pipeline tool calls API → context.json/scratchpad.json
   Orchestratore cron multi-agent
   Tool precostruiti esposti agli agent
   Implementazione 4 processi agent
   Integration testing con paper trading
```

---

## Reading order per iniziare

**Leggi in QUESTO ordine** prima di scrivere una riga di codice:

```
1. README.md                       (questo file — orientation)
   ↓
2. AGENT-ARCHITECTURE-GUIDE.md     (mappa architetturale, 12 sezioni)
   → 4 agent ruoli, file convention, cron pipeline, tool precostruiti
   ↓
3. INTEGRATION-NOTES.md            (verità tecnica, 24 sezioni)
   → vincoli reali, auth, smoke results, calibration, bypass patterns
   ↓
4. skills/*.md                     (16 skill — sostanza agent)
   → leggi quelle owned dal primo agent che implementi
   ↓
5. skills/references/*.md          (9 reference — caricati dalle skill)
   → solo quando una skill principale ne carica uno
```

Tempo stimato lettura: **2-3 ore** per orientarsi completamente.
Vale la pena: evita di reinventare logica già distillata.

---

## Mappa file — cosa troverai e perché

### Documenti architetturali (root)

| File | Cosa contiene | Quando leggerlo |
|---|---|---|
| [AGENT-ARCHITECTURE-GUIDE.md](AGENT-ARCHITECTURE-GUIDE.md) | Mappa 4 agent, file system, tool precostruiti, pipeline cron, failure modes, pattern bypass anti-bot, priority implementazione 6 fasi | **PRIMO** — leggilo per orientarti |
| [INTEGRATION-NOTES.md](INTEGRATION-NOTES.md) | Verità tecnica completa: auth, rate limiter, cache TTL, smoke results, calibration framework, audit dipendenze (~2400 righe, 24 sezioni) | Riferimento approfondimento — consulta sezione specifica all'occorrenza |

### Skill markdown (cervello dell'agent)

```
skills/                                    16 skill principali
├── gex-analysis.md                       Analisi struttura GEX×LW×derivati×macro
├── derivatives-dashboard.md              4 pannelli (OI/L/S/Liq/Delta) → bias
├── chart-pattern-recognition.md          30+ pattern visivi + harmonic + Fibonacci
├── price-alert-trigger.md                Risposta < 60s a alert prezzo
├── scalp-execution.md                    6 setup scalp tipizzati
├── macro-regime-monitor.md               5 regime macro + modifier table
├── etf-flow-interpreter.md               Capitale istituzionale leading 6-24h
├── funding-arb-detector.md               Cross-exchange + predicted funding
├── narrative-rotation-monitor.md         Sector rotation EMERGING/FADING
├── whale-onchain-monitor.md              Hyperliquid + DEX + HHI velocity
├── proactive-scout.md                    Scan universe top 50 ogni 30min
├── risk-forward.md                       Pre-emptive event-driven (T-24h/6h/2h)
├── news-sentiment-monitor.md             7 RSS feeds + CRITICAL detection
├── composite-risk-gate.md                Kill switch system-wide (7 trigger)
├── gex-liquidation-forecast.md           ★ STOP_RUN/CASCADE/PIN_RISK forecast
└── basis-arb-monitor.md                  Perp vs spot extreme contrarian
```

```
skills/references/                         9 reference (loaded esplicitamente)
├── candlestick-patterns.md               1-3 candele pattern catalog
├── chart-patterns.md                     Geometria multi-candela
├── harmonic-patterns.md                  Gartley/Bat/Butterfly XABCD Fibonacci
├── fibonacci-analysis.md                 Retracement/extension/cluster
├── stochrsi-volume-integration.md        Filtro qualità SEMPRE applicato
├── chart-reading.md                      VP, GEX Profile, Analysis Chart visual
├── calibration-thresholds.md             Framework percentile P5/P85/P95/P99
├── spec-adaptive-weights.md              SPEC modulo Python weekly
└── spec-calibration-monitor.md           SPEC modulo Python monthly
```

### Smoke tests (riproducibilità totale)

```
tests/                                     7 smoke scripts riproducibili
├── smoke_endpoints.py                    CoinGlass Hobbyist (171 probe → 82 AVAIL)
├── smoke_coingecko.py                    CoinGecko Demo (61 probe → 51 AVAIL)
├── smoke_coinalyze.py                    Coinalyze Free (21 probe → 19 AVAIL)
├── test_hyperliquid.py                   Hyperliquid native (10 probe → 10 AVAIL)
├── test_calendar_news.py                 investpy + Forex Factory + 7 RSS feeds
├── test_bitget_ws.py                     WS Bitget pubblico verificato
├── cross_validation.py                   CoinGecko ↔ Coinalyze cross-validation
└── README.md                             How to run
```

### Smoke reports (audit empirici)

| Report | Contenuto |
|---|---|
| [smoke_report_v5_official.md](smoke_report_v5_official.md) | CoinGlass Hobbyist FINALE — 171 probe, 82 AVAILABLE |
| [cg_report_v2.md](cg_report_v2.md) | CoinGecko Demo FINALE — 61 probe, 51 AVAILABLE |
| [cz_report.md](cz_report.md) | Coinalyze Free — 21 probe, 19 AVAILABLE |
| [hl_report.md](hl_report.md) | Hyperliquid native — 10/10 AVAILABLE |
| [cal_news_report.md](cal_news_report.md) | investpy + Forex Factory + 7 RSS feeds |
| [cross_report.md](cross_report.md) | CG ↔ CZ cross-validation OI/funding |

I report più vecchi (`smoke_report.md`, `_full.md`, `_v3.md`, `_v4_full.md`) sono **storici**, conservati per audit trail. Ignorali per implementazione.

### Catalog endpoint

| File | Contenuto |
|---|---|
| [coinglass-endpoints-catalog.md](coinglass-endpoints-catalog.md) | 130 endpoint CoinGlass catalogati con tier gating (creato da agent dedicato) |
| [coingecko_coinglass.md](coingecko_coinglass.md) | Cross-mapping CoinGecko ↔ CoinGlass per stesso asset |
| [coinglass.md](coinglass.md) | Doc CoinGlass legacy (validata vs ufficiale) |

### Codice

```
engine/
└── price_feeds.py                        WS Bitget+Binance verificato funzionante
                                           (riutilizzabile, auto-reconnect, ping/pong)

pine-scripts/                              5 Pine Script v6 production-ready per TradingView
├── 01_hurst_regime_filter.pine            Master switch trending/mean-rev (chart 4h BTC)
├── 02_vix_term_structure.pine             VIX9D/VIX/VIX3M slope contrarian (Johnson 2017 JFQA)
├── 03_btcd_usdtd_crypto_regime.pine       Vera altseason vs stablecoin season detector
├── 04_cross_asset_correlation_matrix.pine Macro brain: BTC ↔ SPX/DXY/Gold/NDX/US10Y/VIX
├── 05_ict_smc_confluence.pine             Execution-grade: sweep + FVG + BoS triple confluence
└── README.md                              Setup TradingView + webhook schemas
```

### Configurazione

```
.env                                      3 chiavi presenti:
                                            COINGLASS_API_KEY ($29/mo Hobbyist)
                                            COINGECKO_API_KEY (Demo free)
                                            COINALYZE_API_KEY (Free)
                                          
                                          Hyperliquid: no auth necessaria
                                          Bitget/Binance WS: no auth
                                          investpy + RSS: no auth
                                          CryptoPanic: deprecato 2026, non usato
```

### Cartelle ausiliarie

```
screenshot/                               Screenshot frontend per debug visivo
                                           (vedi README.md interno)
```

---

## Quick start — come iniziare l'implementazione

**Step 1: Verifica setup locale**
```bash
cd /Users/lele/caesoftware/coinglass_api  # (sostituisci con path server)
cat .env  # verifica 3 chiavi
python3 tests/smoke_coinalyze.py --out /tmp/cz_test.md  # verifica chiave Coinalyze
```

**Step 2: Installa dipendenze Python necessarie**
```bash
pip install --user feedparser investpy websockets pandas numpy
# Verificate funzionanti su Python 3.9 e 3.10+
```

**Step 3: Riproduce smoke test** (sanity check completo)
```bash
python3 tests/test_hyperliquid.py     # 10/10 AVAILABLE attesi
python3 tests/test_calendar_news.py   # investpy + 7 RSS + Forex Factory
python3 tests/smoke_coinalyze.py      # 19/21 AVAILABLE attesi
# ... etc
```

**Step 4: Leggi AGENT-ARCHITECTURE-GUIDE.md §6 (priority implementazione)**

Sequenza raccomandata:
1. **Fase 1**: Pipeline core fetch → cache → write context.json (1-2 settimane)
2. **Fase 2**: macro-master agent (slow modifiers) (1 settimana)
3. **Fase 3**: sentinel-agent (safety + kill switch) (1-2 settimane)
4. **Fase 4**: jarvis-main + gex-analyst operativi (1 settimana)
5. **Fase 5**: Calibration loop (adaptive_weights + calibration_monitor) (1 settimana)
6. **Fase 6**: Integration testing paper trading (1 settimana)

---

## Numeri finali del repo

```
DOCUMENTAZIONE:
  INTEGRATION-NOTES.md         2400 righe, 24 sezioni
  AGENT-ARCHITECTURE-GUIDE.md   ~600 righe, 12 sezioni
  README.md                    questo file (entry point)

SKILL:
  16 skill principali markdown (sostanza ragionamento)
   9 reference (loaded da skill principali)

DATI VERIFICATI:
  170+ endpoint testati empiricamente
   3 API paid/free (CoinGlass + CoinGecko + Coinalyze)
   1 native API gratuita (Hyperliquid 230 asset universe)
   2 WebSocket pubblici (Bitget + Binance)
   1 economic calendar (investpy via investing.com)
   1 backup calendar (Forex Factory bypass)
   7 RSS feeds crypto news

AUDIT TRAIL:
   7 smoke test riproducibili in tests/
  12 report markdown (audit empirici)
   1 cross-validation report (CG ↔ CZ)

ARCHITETTURA:
  4 agent dimensionati con ruoli non sovrapposti
  5 dimensioni capacity (Strategico/Strutturale/Tattico/Defensive/Apprendimento)
  3 loop di apprendimento (counterfactual + adaptive weights + calibration)
  7 trigger di kill switch + autorità di veto sentinel-agent
```

---

## Filosofia del repo

```
Le skill sono SOSTANZA, non LEGGE.
  Distillato di logica trading professionale + esperienza retrospettiva +
  framework matematico. Il Claude server le legge come base di ragionamento,
  non come dogma.

Quando il server trova che una skill suggerisce A ma il context dice B,
può decidere B se il rationale è esplicito e loggato.

L'autorità finale resta sull'utente. L'agent suggerisce, esegue secondo
framework, ma l'utente può:
  - Sospendere il sistema (manual override del kill switch)
  - Sovrascrivere decisioni (con motivazione loggata)
  - Modificare le skill per cambiare il framework
  - Aggiungere nuove skill per nuove dimensioni di analisi

Il sistema è SUO. Il framework è MODULARE. Le skill sono VIVE.
```

---

## Avvertenze importanti

0. **★ AUDIT DEL SISTEMA ESISTENTE PRIMA DI TUTTO.** Il gex-analyst sul server
   esegue già trade automatici e fa retrospettive. Capire CHI fa COSA, CHE
   fonti dati usa, QUALI file scrive/legge è il prerequisito #0. Le skill
   in questo repo sono framework di ragionamento, non sostituzione del
   sistema attuale. Integra. Non rimpiazzare ciò che funziona.

1. **Niente tool API call dentro skill markdown.** Le skill ragionano su dati
   già fetchati. Il wiring API → context.json è codice del Claude server.

2. **Counterfactual obbligatorio.** gex-analysis scrive retrospettive con
   simulazione "se avessi fatto Y invece di X". Senza, MONITOR diventa alibi.

3. **Kill switch ha autorità di veto.** Tutti gli agent leggono
   `system_state.kill_switch_active` PRIMA di ogni azione operativa.

4. **Calibration > hardcoded thresholds.** Le soglie nelle skill sono fallback.
   Il sistema usa percentile rolling 30gg da `calibration.json` quando esiste.

5. **Counterfactual + Calibration + Adaptive Weights** = il loop di apprendimento.
   Senza i 2 moduli Python (in `references/spec-*.md`), l'agent NON impara
   quantitativamente — applica sempre le stesse regole.

6. **Bypass anti-bot Cloudflare 1010** è documentato come pattern reusable
   in `AGENT-ARCHITECTURE-GUIDE.md §4.bis`. Etico per uso single-user low-volume
   su feed pubblici. **Non abusare.**

7. **Test sempre PRIMA di documentare.** Tutti i smoke in `tests/` sono
   riproducibili. Non fidarti della doc — riesegui i test prima di iniziare.

8. **NON assumere fonti dati specifiche per GEX/LW.** Le skill (gex-analysis,
   gex-liquidation-forecast) leggono confluence_history/lw_diff_history come
   pre-esistenti. Sul server reale questi possono venire da Pine Script,
   da calcolo proprietario, da terze parti. Verifica la fonte attuale nel
   sistema operativo prima di proporre cambiamenti.

---

## Contatto + storia

```
Repo author: Lele (giannidipie@gmail.com)
Last updated: 2026-05-01
Sessioni di research: ~5 settimane
Compact summaries condensati nel repo: lavoro multi-sessione consolidato
Memoria persistente: ~/.claude/projects/-Users-lele-caesoftware-coinglass-api/memory/

Il sistema è single-user, single-machine, deployato su mini-PC Ubuntu.
Esecuzione trade: Bitget perp.
Budget infrastructure: $29/mo (CoinGlass Hobbyist) + altri free/scraping.

Trading style ottimizzato per: scalp + swing intraday/multiday su BTC, ETH,
top 50 alts, con esposizione limitata e kill switch defensivo.
```

---

**Quando inizi a implementare, parti da [AGENT-ARCHITECTURE-GUIDE.md](AGENT-ARCHITECTURE-GUIDE.md) — è la mappa.**
