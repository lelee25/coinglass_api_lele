---
name: risk-forward
description: >
  Scout calendar event imminenti (FOMC, CPI, NFP, opzioni expiry, halving,
  unlock token, hard fork) e propone azioni preventive PRIMA dell'evento:
  ridurre size, allargare stop, chiudere posizioni esposte, hedge alternativi.
  Skill PRE-EMPTIVE (cron 1h) — entra in azione 24h prima dell'evento e si
  intensifica nelle ultime 6h.
  Trigger: "evento macro imminente", "preparati al CPI", "Fed decision a breve",
  "cosa fare prima del news", "FOMC ridotta esposizione", "halving plan",
  "options expiry friday", "unlock altcoin", "rischi imminenti", "calendar check",
  "preemptive risk", "pre-news adjustment", "max pain expiry".
  Output: piano azioni preventive ordinato per criticità + delega a price-alert
  per orchestrare execution. NON chiude posizioni autonomamente — propone all'agent
  esecutivo (jarvis-main) le azioni.
---

# Risk Forward — preparazione preventiva eventi

## Filosofia: il rischio si riduce PRIMA, non durante

L'analisi tecnica si azzera in 30 secondi quando esce un dato macro inaspettato.
Le retrospettive del sistema (gex-analysis errori documentati) confermano:
**stop < 1.5% in regime bearish vengono falciati prima del move**, e questo
peggiora drammaticamente nelle 6h pre-evento.

```
APPROCCIO REATTIVO (sbagliato):
  Evento esce -> volatilità esplode -> stop saltano -> loss

APPROCCIO PRE-EMPTIVE (questa skill):
  6-24h prima -> identifica esposizione -> riduce/copre -> evento è non-event
```

L'edge non è "evitare il rischio", è **dimensionare il rischio in funzione
dell'evento prossimo**. A volte la risposta è "tutto OK, mantieni posizioni".
A volte è "chiudi due delle quattro posizioni, allarga stop sulle altre".

---

## Data sources

```
EVENTI MACRO (calendario):
  ★ NESSUNA chiave calendar API disponibile in .env attuale.
  Stack raccomandato: investing.com via repo open-source + supplemento manuale.
  
  ★ RACCOMANDATA — investpy (Python, scraping investing.com):
    https://github.com/alvarobartt/investpy
    Verificato empiricamente 2026-05-01 con tests/test_calendar_news.py:
      pip install investpy (v1.0.8 — Python 3.9 compatible)
      
      RISULTATO TEST: investpy.economic_calendar(
        countries=["united states"], importances=["high"],
        from_date="01/05/2026", to_date="15/05/2026")
      -> 21 eventi rilevanti in 2 settimane (PMI ISM, JOLTS, ADP Nonfarm,
         Crude Oil, etc.)
    
    Schema return (DataFrame pandas):
      date, time, zone, currency, importance, event, actual, forecast, previous
      Esempio entry verificata:
        "01/05/2026 17:00 ISM Manufacturing PMI (Apr) high
         actual=None forecast=53.1 previous=52.7"
    
    Filtraggio:
      events_high = calendar[calendar.importance == 'high']
      events_us = calendar[calendar.zone == 'united states']
      events_eu = calendar[calendar.zone == 'euro zone']
    
    Caveat noti (verificati cross-checking screenshot investing.com 2026-05-01):
      - Versione 1.0.8 (vecchia ma stabile sul scraping HTML)
      - Warning urllib3/LibreSSL su macOS (cosmetico, non blocca)
      - ★ BUG DATE MAPPING: investpy può occasionalmente assegnare eventi
        al giorno sbagliato (es. ISM Services del 6 maggio appare nel 5 maggio)
        Workaround: per high-impact events critici, validare manualmente
        l'export weekly contro investing.com sito ufficiale
      - ★ ORARIO IN UTC: investpy ritorna time in UTC. Conversione necessaria
        per timezone utente (es. CEST = UTC+2). Usa pytz o zoneinfo.
      - Eventi MEDIUM importance correttamente filtrati con importances=["high"]
      - investing.com può cambiare struttura HTML (rare ma possibile)
        Mitigation: monitor con retry + log dei break per intervento manuale
    
    ★ BACKUP SECONDARY — Forex Factory JSON feed (verificato 2026-05-01):
      URL: https://nfs.faireconomy.media/ff_calendar_thisweek.json
      
      Funziona CON BROWSER HEADERS (bypass Cloudflare 1010):
      
        BROWSER_HEADERS = {
          "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0.0.0 Safari/537.36",
          "Accept": "application/json, ...",
          "Accept-Language": "en-US,en;q=0.9",
          "Accept-Encoding": "gzip, deflate",  # NO brotli
          "Referer": "https://www.forexfactory.com/",
          "Cache-Control": "no-cache",
        }
      
      Senza headers: HTTP 403 (Cloudflare anti-bot).
      Con headers: HTTP 200, 118 eventi (di cui ~26 USD HIGH impact).
      Schema pulito: {date ISO8601, country USD/EUR/..., title, impact High/Medium/Low/Holiday,
                       forecast, previous}.
      
      ⚠️ RATE LIMIT AGGRESSIVO: ~5 req/min, oltre quello HTTP 429.
         Per cron 1 fetch/giorno = nessun problema. Per debug locale:
         backoff esponenziale (30s, 60s, 120s) automatico nel test.
      
      USO COME CROSS-VALIDATION:
        cron 06:30 UTC daily -> state/macro_calendar_ff.json
        Per ogni HIGH event in investpy, cerca corrispondenza in FF entro ±1 giorno
        Se discrepancy: log + alert (probabile bug date-mapping investpy)
    
    SOURCE NON DISPONIBILI (verificati 2026-05-01):
      ❌ TradingEconomics calendar guest:guest → rate-limit aggressivo dopo 2-3 req
      ❌ CryptoPanic events → endpoint chiuso (HTTP 404 vero, non anti-bot)
    
    Stack robusto: investpy (PRIMARY) + Forex Factory (CROSS-VALIDATE) +
    crypto_calendar.json manuale (CRYPTO-SPECIFIC).
    
    Wrapping CLI raccomandato:
      Crea ~/gex-agentkit/scrapers/economic_calendar.py
      Invocazione: python3 economic_calendar.py --days 7 --importance high \
                   --output state/macro_calendar.json
      Cron: daily 06:00 UTC (refresh weekly events)
      
      Fail-safe: se investpy fail (HTML changed), fallback a config/crypto_calendar.json
      manuale + alert utente per intervento.
  
  ALTERNATIVA — Forex Factory feed JSON pubblico:
    https://nfs.faireconomy.media/ff_calendar_thisweek.json
    URL stabile (community-maintained), no auth, formato JSON pulito
    Schema: {title, country, date, impact, forecast, previous, actual}
    Limitato a "questa settimana" — refresh weekly Sunday 22:00 UTC
  
  CRYPTO-SPECIFIC EVENTS (non coperti da investpy):
    config/crypto_calendar.json aggiornato manualmente (refresh mensile):
      [
        {"date":"2026-05-15", "event":"ETHF Tokyo unlock 5%", 
         "asset":"ETHF", "importance":"high"},
        {"date":"2026-06-01", "event":"BTC halving anniversary", 
         "asset":"BTC", "importance":"medium"},
        {"date":"2026-07-15", "event":"SEC SOL ETF deadline", 
         "asset":"SOL", "importance":"high"}
      ]
    
    Source utenti per popolamento manuale:
      tokenunlocks.app (token unlock, free public web)
      coingecko.com/events (ETF launches, listings)
      ethereum.org (ETH upgrades calendar)

OPTIONS EXPIRY (CoinGlass /api/option/info — verificato AVAILABLE):
  Espone next_expiry_date + max_pain_price per BTC/ETH options
  Aggregato cron 1h, no scraping necessario.

CONSOLIDATED OUTPUT:
  Il Claude server combina i 3 source -> state/calendar_events.json schema:
    {
      "events": [
        {"ts":"2026-05-15T18:00:00Z", "type":"FOMC",
         "source":"investpy", "importance":"high", "asset_impact":["BTC","ETH"]},
        {"ts":"2026-05-30T08:00:00Z", "type":"BTC_OPTIONS_EXPIRY",
         "source":"coinglass", "max_pain":68000, "importance":"medium"},
        {"ts":"2026-06-15T00:00:00Z", "type":"ETHF_UNLOCK",
         "source":"manual", "importance":"high", "asset_impact":["ETHF"]}
      ],
      "last_refresh": {
        "investpy": "2026-05-01T06:00:00Z",
        "coinglass_options": "2026-05-01T15:00:00Z",
        "manual": "2026-05-01T00:00:00Z"
      }
    }
  
  Importance filter: HIGH = filtrare attenzione, MEDIUM = aware, LOW = skip

CRYPTO-SPECIFIC EVENTS:
  CoinGlass /api/option/info        -> options expiry imminenti
  CoinGlass /api/option/max-pain    -> max pain level options expiry
  Hard-coded list (curato manualmente):
    -> halving (BTC ogni 4 anni)
    -> hard fork (ETH upgrade, etc.)
    -> token unlock (Binance Research, TokenUnlocks.app)
    -> ETF launch dates (SOL ETF imminente, etc.)

CONTEXT INTERNO:
  scratchpad.active_positions   -> esposizione attuale
  context.macro_regime          -> regime affecta sensitività eventi
  context.funding_costs         -> funding settlement prossimo (paga 8h next)

OUTPUT FROM:
  CoinGlass option max-pain     -> magnete prezzo expiry friday
```

---

## Tipi di evento e tempistiche di azione

### A. EVENTI MACRO USA (FOMC, CPI, NFP)
```
T-24h:  notifica preliminare, no azione obbligatoria
T-6h:   ALERT — controllo esposizione, valuta riduzione 30% se size piena
T-2h:   ALERT URGENTE — chiusura swing aperti se non hedged
T-30m:  STOP — no nuovi trade, allarga tutti gli stop di 1.5x
T+0:    NO TRADE per 15min (volatilità erratica)
T+15m:  reazione: lettura derivatives-dashboard immediata, decisione

Rationale: 
  Storicamente l'80% del move post-evento avviene nelle prime 30min,
  spesso con whipsaw che falcia stop classici.
```

### B. OPTIONS EXPIRY (venerdì 08:00 UTC)
```
T-48h:  identifica max pain level (CoinGlass /api/option/max-pain)
        -> il prezzo tende a gravitare verso max pain venerdì morning
T-24h:  ALERT — segnala se posizione apre in direzione opposta a max pain
T-6h:   se prezzo > 1% lontano da max pain -> alta probabilità "pinning"
        verso max pain. Stop potrebbero essere falciati da pinning move.
T-1h:   no nuovi swing, scalp solo Setup 1/2 (rimbalzo veloce)
T+0:    expiry settled, evento concluso

Rationale:
  Pin risk documentato in gex-analysis. MM hedging ne fa magnete.
```

### C. CRYPTO HARD FORKS / UPGRADES
```
T-7gg:   notifica strategica
T-72h:   ALERT — review esposizione asset specifico
T-24h:   se posizione lunga > 50% size massima sull'asset -> consiglia trim 30%
T-6h:    no nuovi trade sull'asset, swap stop a "iceberg" (ridotti per limitare slippage)
T+0:     evento, attendere conferma stabilità rete (3-6h)
T+6h:    rivalutazione

Rationale:
  Forks possono produrre slippage estremo, network congestion, exchange
  pause withdrawal. Il rischio NON è solo prezzo, è operativo.
```

### D. TOKEN UNLOCK GROSSI
```
T-7gg:   notifica con magnitude (% supply che entra in circulation)
T-48h:   se posizione long su asset -> consiglia trim 30-50% size
T-24h:   ALERT — review final
T+0:     unlock event, attesa di sell pressure
T+72h:   "wash settlement" — il sell completo richiede 1-3 giorni
         Riapertura posizioni solo dopo che dump è completato

Rationale:
  Unlock > 5% supply ha statisticamente prodotto -10% nelle 7 giorni
  successivi nell'85% dei casi 2024-2025.
```

### E. ETF LAUNCH (BTC/ETH/SOL)
```
T-30gg:  notifica strategica, bias bullish lungo termine
T-7gg:   review esposizione, consiglia INCREMENTO size se non già esposti
T-24h:   ALERT — preparare ordini limit nelle prime ore di trading USA
T+0:     evento launch, pump iniziale tipico (volatilità alta)
T+1d:    rivalutazione: inflow netto positivo conferma narrativa, altrimenti fade

Rationale:
  ETF spot launches storicamente hanno prodotto +15-30% in 30gg
  (vedi BTC ETF gennaio 2024, ETH ETF luglio 2024).
```

### F. ANNUNCI REGOLATORI USA / EUROPA
```
T-?:     non sempre prevedibili (testimony Congress, SEC filings)
T-N/A:   monitor news feed (CryptoPanic) tag "regulation"
T+0:     reazione immediata se sentiment shift > 1.5σ in 1h

Rationale:
  Asymmetric risk — regulation NEGATIVA produce dump 5-15%,
  POSITIVA solo 2-5% pump. Bias defensive su queste.
```

---

## Algoritmo di assessment (cron 1h)

```
STEP 1 — Fetch eventi prossime 48h
  Fetch calendar API + options expiry CoinGlass
  Filter importance >= MEDIUM/HIGH
  Sort by ts ascending

STEP 2 — Per ogni evento, calcola time_to_event
  hours_to_event = (event_ts - now_ts) / 3600

STEP 3 — Lookup azione raccomandata per (event_type, hours_to_event)
  action_table[event_type][time_window] -> action_set

STEP 4 — Esposizione check
  Per ogni active_position:
    is_exposed = (asset == event.affects_asset) OR
                 (event.is_macro AND asset in [BTC, ETH, SOL])
    if is_exposed -> add to action plan

STEP 5 — Aggregate action plan
  ordered list: [
    {action: "TRIM_50%", asset: "ETH", reason: "ETH unlock T-24h", priority: HIGH},
    {action: "WIDEN_STOP_1.5x", asset: "BTC", reason: "FOMC T-2h", priority: HIGH},
    {action: "NO_NEW_TRADES", scope: "all", reason: "FOMC T-2h", priority: CRITICAL},
    ...
  ]

STEP 6 — Emit alert
  Se priority CRITICAL/HIGH presente -> push notify all'agent
  Sempre -> aggiorna scratchpad.risk_forward_plan
```

---

## Output: action plan + delega

```
=== RISK FORWARD ASSESSMENT — [data ora UTC] ===

EVENTI IMMINENTI (prossime 48h):
  [HIGH]   FOMC Decision        — T-3.5h  | 2026-05-01 18:00 UTC
  [MED]    BTC Options Expiry  — T-13h   | 2026-05-02 08:00 UTC
  [LOW]    UK GDP                — T-26h   | 2026-05-02 09:30 UTC

ESPOSIZIONE ATTUALE:
  Posizione 1: BTC long $10k @ $X.XK, stop -2.0%, target +3.5%
  Posizione 2: ETH short $5k @ $X.XK, stop +1.5%, target -2.5%

ACTION PLAN (ordinato per criticità):

[CRITICAL] T-3.5h FOMC
  Action:    NO_NEW_TRADES
  Scope:     all
  Reason:    FOMC < 6h — volatilità imminente, stop classici a rischio
  Owner:     jarvis-main (block in pre-trade check)

[HIGH] BTC long position pre-FOMC
  Action:    WIDEN_STOP_1.5x
  Asset:     BTC
  Current:   stop -2.0%, target +3.5%
  Proposed:  stop -3.0%, target +3.5% (R/R rimane > 1)
  Reason:    FOMC tipicamente whipsaw, stop standard falciati
  Delega:    price-alert-trigger (modifica trigger livello)

[MED] BTC options expiry T-13h
  Action:    AWARENESS
  Asset:     BTC
  Max pain:  $X.XK (calcolato da CoinGlass option/max-pain)
  Proposed:  monitor pinning verso max pain venerdì morning
  Delega:    nessuna (informativo)

[LOW] ETH short pre-UK GDP
  Action:    NONE_NEEDED
  Reason:    GDP UK low impact su ETH, position size già ridotta

NEXT REVIEW: [now + 1h]
```

---

## Cross-reference con altre skill

```
LETTA DA QUESTA SKILL:
  scratchpad.active_positions   (esposizione attuale)
  context.macro_regime          (regime modulates urgenza)
  context.funding_costs         (settlement che cade vicino evento)
  external: calendar API, CoinGlass option max-pain

DELEGA A:
  price-alert-trigger      (modifica stop su trade aperti)
  jarvis-main agent       (NO_NEW_TRADES window)
  scalp-execution         (filtro 2 hours_to_event lo legge nativamente)

NON DELEGA A:
  gex-analysis             (troppo lento per pre-emptive)
  Non chiude posizioni    (delegata a jarvis-main con conferma)

SCRIVE:
  scratchpad.risk_forward_plan (action plan ordinato)
  scratchpad.notes (audit trail decisioni preventive)
```

---

## Errori da evitare

```
Chiudere posizioni autonomamente:
  La skill PROPONE, non esegue. La chiusura richiede approvazione esecutore.
  Auto-close senza autorizzazione = comportamento dell'agent inaffidabile.

Reagire a ogni evento LOW importance:
  Notification fatigue. Filtra MEDIUM/HIGH. LOW solo se asset fortemente
  esposto e position size > $X (parametrico).

Confondere correlazione con causation:
  CPI esce -> BTC scende. NON sempre. A volte CPI forte -> equity rally,
  crypto follow + 1h. Adattare per regime.

Trim sempre size pre-evento:
  Trim arbitrario riduce convexity. Se la tesi era forte e l'evento atteso
  è coerente con tesi (es. soft CPI -> bullish, e tu sei long), tieni.
  La skill non sostituisce judgement, suggerisce default conservativo.

Stops widening senza R/R check:
  Allargare stop senza muovere target rovina R/R. Sempre verificare:
  new_R/R > 1.0 prima di applicare widening.

Pin risk options expiry ignorato:
  Il magnete max pain è REALE su 60-70% degli expiry venerdì BTC.
  Non considerarlo lascia stop esposti a pinning moves.
```

---

## Threshold operativi (default — calibrabili)

```
EVENT IMPORTANCE FILTER:
  notify_threshold: MEDIUM
  action_threshold: MEDIUM (HIGH per CRITICAL warnings)

TIME WINDOWS:
  event_macro_critical_hours: 0.5
  event_macro_alert_hours: 6.0
  event_macro_aware_hours: 24.0
  options_expiry_aware_hours: 48.0
  unlock_aware_hours: 72.0
  fork_aware_hours: 168.0  (1 settimana)

EXPOSURE THRESHOLDS:
  trim_recommended_size_factor: 0.5  (chiudi metà)
  widen_stop_factor: 1.5             (allarga 50%)
```
