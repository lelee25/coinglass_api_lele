# Agent Architecture Guide — gex-agentkit / tradevalue

> **Audience**: Claude Code sul server (mini-PC Ubuntu via SSH).
> **Scopo**: guida sostanziale per implementare/orchestrare il sistema multi-agent
> trading basato su 16 skill markdown + 9 reference + 170+ endpoint API verificati.
>
> Questo file NON è una skill. È la **mappa architetturale** che il server
> deve leggere PRIMA di iniziare l'implementazione tecnica. Tutto qui descritto
> è validato empiricamente (vedi INTEGRATION-NOTES.md per i dettagli tecnici).
>
> ## ⚠️ PRECONDIZIONE OBBLIGATORIA: audit del sistema esistente
>
> Il **gex-analyst** sul server è **già operativo automatico** — esegue trade
> reali e produce retrospettive. Non è in questo repo, è codice tuo sul server.
>
> **Procedura corretta:**
> 1. **Prima**: capire cosa fa il sistema attuale, quali file produce/consuma,
>    quali fonti dati usa effettivamente (es. GEX/LW: Pine Script? proprietario?
>    terzi? — verifica, non assumere)
> 2. **Poi**: confrontare con questa guida + le 16 skill markdown
> 3. **Poi**: decidere cosa **integrare** (capability nuove) vs cosa **migliorare**
>    (calibration percentile, adaptive weights, kill switch) vs cosa **conservare
>    intatto** (logica già validata empiricamente dall'utente)
>
> Le skill di questo repo sono **framework di ragionamento + sostanza**.
> Non meccanismi di sostituzione. Se il sistema attuale ha già una pipeline
> GEX/LW/derivati funzionante, NON rifarla — adatta le skill a quella pipeline.
>
> La regola d'oro: **migliorare ciò che funziona, integrare ciò che manca,
> non duplicare**.

---

## 0. Stato di partenza (verità del repo)

```
✅ FATTO (verificato):
  - 152 endpoint API AVAILABLE su 3 provider (CoinGlass + CoinGecko + Coinalyze)
  - WS Bitget + Binance verificati funzionanti (engine/price_feeds.py)
  - 16 skill markdown sostanziali in skills/
  - 9 reference markdown in skills/references/
  - 5 smoke test scripts in tests/
  - INTEGRATION-NOTES.md (~2200 righe, 23 sezioni)

⏳ DA IMPLEMENTARE (compito del Claude server):
  - Pipeline tool calls API → context.json/scratchpad.json (wiring)
  - Orchestratore cron multi-agent
  - Persistence layer (SQLite per token bucket, file JSON per state)
  - Tool precostruiti esposti agli agent (read_context, write_alert, etc.)
  - Moduli Python complementari (adaptive_weights, calibration_monitor)
  - 4 agent processes (jarvis-main, gex-analyst, macro-master, sentinel-agent)
```

---

## 1. I 4 agent — ruoli, autorità, file owned

### `gex-analyst` (ATTUALE — esecutore automatico)
```
RUOLO:           Analisi strutturale + esecuzione trade automatico + retrospettive
AUTORITÀ:        APRE/CHIUDE/MODIFICA trade su Bitget
TRIGGER:         Cron 1h (lettura), cron 4h (analisi profonda),
                 webhook prezzo (price-alert-trigger via jarvis)
SKILL OWNED:     gex-analysis, derivatives-dashboard, chart-pattern-recognition
                 + 6 reference (candlestick/chart/harmonic/fibonacci/stochrsi+vol/chart-reading)
SCRIVE:          context.json (resistances/supports/lw_trend/derivatives)
                 scratchpad.json (active_thesis, last_decision, active_positions)
                 retrospettive.md (counterfactual obbligatorio)
                 confluence_history.md (livelli GEX × LW)
LEGGE:           system_state.json (kill switch — si ferma se attivo)
                 context.macro_regime, context.etf_signal, context.funding_signal
                 context.news_signal, context.basis_signal, context.liquidation_forecast
                 setup_weights.json (peso adattivo dei 6 setup)
                 confidence_correction.json (correzione confidence linear)
```

### `jarvis-main` (orchestratore + UI + reattivo)
```
RUOLO:           Orchestratore alert real-time + UI utente + discovery proattivo
AUTORITÀ:        DELEGA a gex-analyst per execution; può RIDURRE size
                 ma non aprire trade autonomamente
TRIGGER:         WS price tick, cron 30min (proactive-scout),
                 cron 1h (risk-forward), comando user
SKILL OWNED:     price-alert-trigger, scalp-execution, whale-onchain-monitor,
                 proactive-scout, risk-forward
SCRIVE:          scratchpad.opportunity_pipeline, scratchpad.whale_alerts,
                 scratchpad.risk_forward_plan, scratchpad.notes
LEGGE:           system_state.json (kill switch),
                 tutto il context.* + scratchpad.*
```

### `macro-master` (strategico long-term)
```
RUOLO:           Produce modifier globali che gli altri agent leggono
AUTORITÀ:        SOLA SCRITTURA modifier (gli altri agent leggono read-only)
TRIGGER:         Cron 4h (regime + funding), daily 22:00 UTC (ETF flow)
SKILL OWNED:     macro-regime-monitor, funding-arb-detector,
                 etf-flow-interpreter, narrative-rotation-monitor
SCRIVE:          context.macro_regime, context.funding_signal,
                 context.funding_costs, context.etf_signal,
                 context.narrative_signal
LEGGE:           system_state.json
```

### `sentinel-agent` ★ NEW (safety + contrarian intelligence)
```
RUOLO:           Safety layer + kill switch + signal contrarian + liquidation forecast
AUTORITÀ:        UNICA AUTORITÀ DI VETO — può scrivere
                 system_state.kill_switch_active = true
                 NON apre/chiude/modifica trade
TRIGGER:         Cron 5min (news + composite-risk-gate),
                 cron 15min (basis), cron 30min (liquidation-forecast),
                 event-driven CRITICAL (immediate)
SKILL OWNED:     news-sentiment-monitor, composite-risk-gate,
                 gex-liquidation-forecast, basis-arb-monitor
SCRIVE:          system_state.json (autoritativo, letto da TUTTI),
                 context.news_signal, context.basis_signal,
                 context.liquidation_forecast,
                 scratchpad.news_alerts, scratchpad.kill_switch_log
LEGGE:           Tutto context.* + scratchpad.* + active_positions per portfolio loss check
```

---

## 2. File system convention — chi scrive cosa, chi legge cosa

```
~/gex-agentkit/
├── state/
│   ├── system_state.json            # autorità: sentinel-agent
│   ├── context.json                  # multi-writer (vedi tabella sotto)
│   ├── scratchpad.json               # multi-writer
│   └── active_positions.json         # autorità: gex-analyst (esecutore)
├── history/
│   ├── retrospettive.md              # autorità: gex-analyst (counterfactual)
│   ├── confluence_history.md         # autorità: gex-analyst
│   ├── lw_diff_history.md            # autorità: gex-analyst
│   ├── confidence_log.json           # append-only, scritto da tutte le skill che dichiarano %
│   └── trade_execution_log.json      # autorità: gex-analyst (esecutore)
├── calibration/
│   ├── calibration.json              # autorità: cron weekly Mon
│   ├── setup_weights.json            # autorità: cron weekly Mon (adaptive_weights.py)
│   └── confidence_correction.json    # autorità: cron monthly 1st (calibration_monitor.py)
├── cache/
│   ├── coinglass/                    # cache risposte API per TTL
│   ├── coinalyze/
│   └── coingecko/
└── ...
```

### Tabella ownership context.json (namespace)

| Namespace | Owner agent | TTL | Letto da |
|---|---|---|---|
| `context.macro_regime` | macro-master | 4h | tutti |
| `context.funding_signal`, `context.funding_costs` | macro-master | 1h | tutti |
| `context.etf_signal` | macro-master | 24h | tutti |
| `context.narrative_signal` | macro-master | 4h | jarvis-main, gex-analyst |
| `context.news_signal` | sentinel-agent | 30min | tutti |
| `context.basis_signal` | sentinel-agent | 30min | tutti |
| `context.liquidation_forecast` | sentinel-agent | 4h | tutti |
| `context.derivatives` | gex-analyst | 1h | tutti |
| `context.confluence_history` (key in context) | gex-analyst | 4h | tutti |
| `context.lw_trend` | gex-analyst | 4h | tutti |

### Tabella ownership scratchpad.json (namespace)

| Namespace | Owner agent | TTL/policy | Letto da |
|---|---|---|---|
| `scratchpad.active_thesis` | gex-analyst | persistent | tutti |
| `scratchpad.last_decision` | jarvis-main + gex-analyst | latest wins | tutti |
| `scratchpad.notes` | tutti (append) | rolling 24h | tutti |
| `scratchpad.whale_alerts` | jarvis-main (whale-onchain) | rolling 24h, max 50 | tutti |
| `scratchpad.opportunity_pipeline` | jarvis-main (proactive-scout) | refresh ogni 30min | tutti |
| `scratchpad.risk_forward_plan` | jarvis-main (risk-forward) | refresh ogni 1h | tutti |
| `scratchpad.news_alerts` | sentinel-agent | rolling 7gg, append CRITICAL only | tutti |
| `scratchpad.kill_switch_log` | sentinel-agent | rolling 30gg | sentinel + analytics |

---

## 3. Flow decisionale tra agent (acyclic)

```
                    ┌─────────────────┐
                    │ sentinel-agent  │  ← cron + event-driven CRITICAL
                    │ (SAFETY layer)  │
                    └────────┬────────┘
                             │ kill_switch_active flag
                             │ news/basis/liq signals
                             ▼
   ┌─────────────────────────────────────────────────┐
   │           system_state.json + context.*          │
   │           (read-only per gli altri agent)        │
   └─────┬───────────┬───────────┬───────────────────┘
         │           │           │
         ▼           ▼           ▼
   ┌──────────┐ ┌──────────┐ ┌──────────────┐
   │ macro-   │ │ jarvis-  │ │ gex-analyst  │
   │ master   │ │ main     │ │ (operativo)  │
   │ (slow)   │ │ (orch.)  │ │ (esegue trade)│
   └──────────┘ └────┬─────┘ └──────────────┘
                     │ delega a gex-analyst
                     │ per execution finale
                     ▼
                 (trade)
```

**Regole del flow:**
1. Tutti gli agent leggono `system_state.json` PRIMA di ogni azione operativa
2. Se `kill_switch_active = true` → no nuovi trade (analisi continuano OK)
3. Le skill non chiamano API direttamente — leggono context popolato dal server
4. Il server orchestratore fa il fetch + cache + write nei file di state
5. Counterfactual obbligatorio in gex-analyst dopo ogni decisione

---

## 4. Pipeline cron — orchestratore consigliato

```
Ogni 5min:
  - sentinel-agent: news-sentiment-monitor (fetch CryptoPanic)
  - sentinel-agent: composite-risk-gate (re-evaluate triggers)

Ogni 15min:
  - sentinel-agent: basis-arb-monitor (calc basis, percentile check)
  - jarvis-main: whale-onchain-monitor (Hyperliquid + onchain pools, HHI velocity)

Ogni 30min:
  - jarvis-main: proactive-scout (universe scan + score)
  - sentinel-agent: gex-liquidation-forecast (build liquidation map + overlay GEX)

Ogni 1h:
  - gex-analyst: gex-analysis lite (refresh derivati + check tesi)
  - jarvis-main: risk-forward (calendar event check + action plan)
  - macro-master: funding-arb-detector (cross-exchange funding)

Ogni 4h:
  - gex-analyst: gex-analysis full + derivatives-dashboard (deep analysis,
                 retrospective writing, confluence_history update)
  - macro-master: macro-regime-monitor (5-state classification + modifier table)
  - macro-master: narrative-rotation-monitor (sector momentum)

Daily 22:00 UTC:
  - macro-master: etf-flow-interpreter (post US market close)
  - housekeeping: cache rotation, log compression

Weekly Monday 03:30 UTC:
  - calibration: adaptive_weights.py → setup_weights.json
  - calibration: refresh calibration.json (percentile rolling 30gg)

Monthly 1st 03:30 UTC:
  - calibration: calibration_monitor.py → confidence_correction.json
```

---

## 4.bis. Pattern bypass anti-bot per public feeds (verificato 2026-05-01)

Diversi feed pubblici (Forex Factory, CoinDesk RSS) sono dietro Cloudflare 1010
quando chiamati senza headers. Funzionano correttamente con browser-like headers.

```python
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml, application/json, text/xml, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",  # NO brotli — meno complessità decoding
    "Cache-Control": "no-cache",
    "Referer": "https://<source-site>/",  # site originario del feed
}
```

**Quando applicarlo:**
- Public feed RSS/JSON che ritorna HTTP 403 con default urllib User-Agent
- Volume: 1 fetch ogni N min/h/day (NON scraping massivo)
- Usage: single-user, single-machine

**Quando NON applicarlo:**
- API che richiede auth key — usa l'auth key, non il bypass
- Volume alto (>10 req/min) → potenziale ToS violation
- Feed che ritorna 404 reale (endpoint chiuso, es. CryptoPanic free 2026)

**Verificato funzionante per:**
- Forex Factory `nfs.faireconomy.media/ff_calendar_thisweek.json` (HTTP 200, 118 eventi)
- CoinDesk RSS `coindesk.com/arc/outboundfeeds/rss` (no trailing slash, 25 items)

**Rate limit gestione:**
```python
def fetch_with_retry(url, headers, retries=3, base_backoff=30):
    for attempt in range(retries):
        try:
            return fetch(url, headers)
        except HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                time.sleep(base_backoff * (2 ** attempt))
                continue
            raise
```

Riferimento implementativo: `tests/test_calendar_news.py` (smoke test riproducibile).

---

## 5. Tool precostruiti da esporre agli agent

Le skill markdown NON conoscono i tool. Il server deve esporre questi tool
agli agent come "primitive" — gli agent ragionano in linguaggio naturale e
chiamano questi tool quando serve:

```
READ TOOLS (idempotent, cache-friendly):
  read_context(namespace)              -> dict
  read_scratchpad(namespace)           -> dict
  read_system_state()                  -> dict (kill switch + active triggers)
  read_calibration(asset, metric)      -> dict (percentile thresholds)
  read_setup_weights(setup_id)         -> float (adaptive weight)
  read_confidence_correction()         -> dict (offset, multiplier)
  read_active_positions()              -> list[dict]
  read_retrospettive(lookback_days)    -> list[dict] (per skill che fanno query)

WRITE TOOLS (require permissions check):
  write_context(namespace, data, ttl)  -> bool
  write_scratchpad_entry(...)          -> bool
  push_alert(level, asset, narrative)  -> bool (notify utente)
  log_confidence_claim(...)            -> bool (per calibration)
  set_kill_switch(active, reason, resume_condition)  -> bool [SENTINEL ONLY]

EXECUTION TOOLS (gex-analyst only):
  open_position(asset, side, size, leverage, sl, tp)  -> trade_id
  close_position(trade_id, partial_pct=100)           -> exit_price
  modify_stop(trade_id, new_sl)                       -> bool
  modify_target(trade_id, new_tp)                     -> bool

API FETCH TOOLS (rate-limited, cached):
  fetch_coinglass(endpoint, params)    -> dict (auto-cached per TTL)
  fetch_coingecko(endpoint, params)    -> dict
  fetch_coinalyze(endpoint, params)    -> dict
  fetch_cryptopanic_posts(filter, currencies)  -> list[dict]
  fetch_hyperliquid(type, params)      -> dict (POST a /info)

WS TOOLS (long-running, server-managed):
  subscribe_price_ws(asset, callback)  -> subscription_id
  unsubscribe_price_ws(subscription_id)
```

**Nota auth:** chiavi in `.env`. Il server le inietta nei tool, mai esposte alle
skill. `COINGLASS_API_KEY`, `COINGECKO_API_KEY`, `COINALYZE_API_KEY`,
`CRYPTOPANIC_API_KEY` (free).

---

## 6. Priority di implementazione (raccomandata)

### Fase 1 — Core (1-2 settimane)
```
1. Pipeline fetch + cache + write context.json (per gex-analyst attuale)
2. Tool precostruiti read_context, read_scratchpad
3. Skill loader (matching frontmatter description ai trigger phrase)
4. Counterfactual writing in retrospettive.md (già parte di gex-analysis)
```

### Fase 2 — Macro slow modifiers (1 settimana)
```
5. macro-regime-monitor + cron 4h
6. etf-flow-interpreter + cron daily
7. funding-arb-detector + cron 1h
8. narrative-rotation-monitor + cron 4h
9. context.json schema completo
```

### Fase 3 — Sentinel & safety (1-2 settimane)
```
10. composite-risk-gate + cron 5min + event-driven
11. news-sentiment-monitor + cron 5min
12. system_state.json read enforcement in altri agent (tutti leggono kill switch)
13. gex-liquidation-forecast + cron 30min
14. basis-arb-monitor + cron 15min
```

### Fase 4 — Reattivo & proattivo (1 settimana)
```
15. price-alert-trigger (WS-driven)
16. scalp-execution + integration con setup_weights.json
17. proactive-scout + cron 30min
18. risk-forward + calendar API integration
19. whale-onchain-monitor + Hyperliquid + DEX pools
```

### Fase 5 — Calibration & learning loop (1 settimana)
```
20. adaptive_weights.py module + cron weekly
21. calibration_monitor.py module + cron monthly
22. calibration.json percentile-based thresholds
23. confidence_correction.json applied in tutti gli output
```

### Fase 6 — Integration testing (1 settimana)
```
24. End-to-end test su BTC con paper trading
25. Verifica counterfactual + retrospettive coerenti
26. False positive rate kill switch < 0.15
27. Latency benchmarks: price-alert-trigger < 60s, scalp-execution < 30s
```

---

## 7. Failure modes & safety

```
SCENARIO 1 — Kill switch stuck on
  Sintomo: kill_switch_active = true ma condizioni di resume sono soddisfatte
  Mitigation: dashboard utente con "force resume" button + audit log
  Fail-safe: dopo 4h di kill, alert utente per manual review

SCENARIO 2 — Stale context (server cron non gira)
  Sintomo: context.macro_regime ts > 6h
  Mitigation: ogni skill verifica TTL e rifiuta se stale
  Fail-safe: skill output "INSUFFICIENT_DATA" invece di trade signal

SCENARIO 3 — API rate limit hit
  Sintomo: fetch_coinglass restituisce HTTP 429
  Mitigation: rate limiter token bucket (SQLite condiviso 3 agent, 30 rpm)
  Fail-safe: degrade con cache stale, alert se cache > TTL+50%

SCENARIO 4 — WS disconnect
  Sintomo: Bitget/Binance WS no tick > 60s
  Mitigation: composite-risk-gate trigger #3 attivo, kill switch
  Fail-safe: posizioni aperte non chiuse autonomamente — manual

SCENARIO 5 — gex-analyst loop stuck
  Sintomo: cron 4h non scrive context aggiornato
  Mitigation: heartbeat check ogni 5min nello scratchpad.notes
  Fail-safe: orchestratore ricarica processo se silente > 30min

SCENARIO 6 — Retrospettiva inconsistente
  Sintomo: counterfactual classifica come MANCATA ma trade era CORRETTA_ASTENSIONE
  Mitigation: review weekly del log, manual flag per data quality
  Fail-safe: adaptive_weights ignora retrospettive flagged
```

---

## 8. Considerazioni espansione futura

```
DA CONSIDERARE SE/QUANDO IL SISTEMA È STABILE:

A. Multi-asset esecuzione:
   Attualmente focus BTC/ETH. Espansione SOL, top 10 alts post-validation.
   Richiede: per-asset calibration, per-asset weight, multi-position management.

B. Multi-exchange execution:
   Attualmente Bitget. Aggiungere Binance/OKX richiede:
   - venue-router skill (best execution routing)
   - basis-aware decision (open su exchange con basis migliore)
   - Cross-exchange position consolidation

C. Options trading:
   CoinGlass espone option data. Skill option-strategy potrebbe gestire
   spread, condor, calendar — ma molto complessa, non priority.

D. Backtesting framework:
   Per validare adaptive_weights e calibration_monitor su storico.
   Replay con context.json snapshot orari → simulate skill decisions.

E. UI dashboard:
   Read-only dashboard per visualizzare:
   - Active positions + PnL
   - Kill switch state + history
   - Confidence calibration curve
   - Setup performance breakdown
   - Whale alerts feed
   - Retrospettive recenti
```

---

## 9. Glossario sistemico

```
context.json     = stato letto multi-agent (refresh frequente, TTL stretti)
scratchpad.json  = bridge tra sessioni (active_thesis, last_decision, notes)
system_state.json = kill switch + system-wide flags (sentinel-agent autorità)
retrospettive.md = audit trail decisioni con counterfactual
confluence_*.md  = livelli GEX × LW storici per gex-analyst

skill            = file markdown con frontmatter description (Claude Code matching)
reference        = file markdown caricato esplicitamente da skill principali
modulo Python    = compute aggregato weekly/monthly, NON skill, output JSON

cron             = orchestratore esterno che richiama agent + skill
TTL              = time-to-live di un dato in cache/state
read-only        = un agent legge ma non scrive una namespace specifica
autoritativo     = un agent è L'UNICO che scrive una namespace specifica

PROATTIVO        = trigger periodico (cron) per discovery
REATTIVO         = trigger event-driven (alert, webhook)
RETROATTIVO      = post-mortem analysis (retrospettive + counterfactual)
PRE-EMPTIVE      = adjust pre-evento (calendar-driven)
DEFENSIVE        = safety + veto (sentinel-agent)
STRATEGICO       = long-horizon modifier (macro-master)
```

---

## 10. Punti aperti per il Claude server

```
DECISIONI TECNICHE LASCIATE AL CLAUDE SERVER (non dogmate qui):

1. Linguaggio: Python è naturale, ma anche Go/Rust per orchestratore
   ad alta concurrency è valido.

2. Storage: file JSON sufficienti per single-machine. SQLite per token
   bucket condiviso. Considerare Redis se scaling multi-node.

3. Process isolation: 4 agent come 4 processi separati? Threadpool?
   AsyncIO single process? Dipende da volumi e safety boundaries.

4. WS lifecycle: chi gestisce reconnect? Subscribe management?
   engine/price_feeds.py è una base, ma multi-agent management complica.

5. Skill loading: lazy load (carico file su trigger) o eager (boot-time)?
   Trade-off memoria vs latenza.

6. Notification channels: Telegram bot, email, Slack, push notify mobile?
   La skill dichiara push_alert() — il server sceglie il canale.

7. Backtesting: framework dedicato o snapshot replay? Trade-off
   accuracy vs complessità.

8. Logging: livello info vs debug, rotation policy, retention.

9. Secrets: .env locale vs vault vs HSM. Single-machine = .env OK.

10. Multi-utente: il sistema è single-user per ora. Eventuale espansione
    richiede tenancy + auth + isolation.
```

Tutte queste decisioni dipendono da vincoli operativi specifici
(hardware, latency target, safety budget, costo) che il server conosce
meglio di chi ha scritto le skill.

---

## 11. Riferimenti incrociati nel repo

```
NECESSARIO leggere PRIMA di implementare:
  - INTEGRATION-NOTES.md             (verità tecnica completa, 23 sezioni)
  - skills/*.md                      (sostanza ragionamento agent)
  - skills/references/*.md           (logica supporto + spec moduli Python)
  - tests/smoke_*.py                 (esempio chiamate API funzionanti)
  - engine/price_feeds.py            (base WS Bitget+Binance)

UTILE leggere se serve approfondire:
  - coinglass-endpoints-catalog.md   (130 endpoint catalogati)
  - cg_report_v2.md                  (CoinGecko Demo smoke v2 — 51/61 AVAILABLE)
  - cz_report.md                     (Coinalyze Free smoke — 19/21 AVAILABLE)
  - smoke_report_v5_official.md      (CoinGlass Hobbyist smoke v5 — 82/171)
  - cross_report.md                  (CoinGecko ↔ Coinalyze cross validation)
```

---

## 12. Una raccomandazione finale

> Le skill sono **sostanza, non legge**. Sono il distillato di logica
> trading professionale + esperienza retrospettiva + framework matematico.
> Il Claude server le legge come **base di ragionamento**, non come dogma.
>
> Quando il server trova che una skill suggerisce A ma il context dice B,
> il server può decidere B se il rationale è esplicito e loggato.
>
> L'autorità finale resta sull'utente. L'agent suggerisce, esegue secondo
> framework, ma l'utente può:
> - Sospendere il sistema
> - Sovrascrivere il kill switch (con motivazione loggata)
> - Modificare le skill per cambiare il framework
> - Aggiungere nuove skill per nuove dimensioni di analisi
>
> Il sistema è **suo**. Il framework è **modulare**. Le skill sono **vive**.
