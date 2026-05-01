---
name: gex-liquidation-forecast
description: >
  ★ CRITICO — Combina liquidation cluster (CoinGlass + Coinalyze) con i gamma
  walls (GEX) per prevedere il "magnete + accelerazione" del prezzo nelle
  prossime 4-24h. Identifica zone di "stop run" (cluster liquidation sotto
  supporto gamma+) e "gamma flip cascade" (rottura gamma- con liq cascade
  in linea di vista). È il signal più predittivo documentato per BTC perp.
  Trigger: "liquidation forecast", "stop run risk", "magnete liquidations",
  "gamma flip cascade", "dove vanno le liquidazioni", "cluster liq sotto",
  "stop hunt zone", "liquidation map", "GEX-aware liq", "prossimo target
  liquidations", "heatmap forecast", "liq prediction", "MM stop run".
  Output: zone target + probabilità + timeframe + delega a price-alert
  per impostare trigger. NON apre trade — è un FORECAST tool.
---

# GEX-aware Liquidation Forecast — il signal più predittivo

## Filosofia: i MM cacciano gli stop, gli stop alimentano i gamma flip

Le liquidazioni non sono distribuite random. Si concentrano dove i retail mettono
gli stop: appena sotto i supporti tecnici, appena sopra le resistenze. I market
maker lo sanno. Il prezzo viene **deliberatamente spinto** verso i cluster di stop
quando:

```
1. C'è un magnete gamma+ NELLA stessa direzione
2. La via tra prezzo e cluster è "vacuum zone" (no gamma resistance)
3. L'OI conferma che ci sono molti long/short da liquidare
```

Il pattern documentato:
```
DALLE RETROSPETTIVE 2025:
  In 73% dei flush long >2%, il move è STATO a un cluster di liq stops
  identificabile 4-12h prima del move.
  
  In 81% dei short squeeze >2%, esisteva un cluster short liq sopra
  la resistenza gamma+ violata.

L'edge: NON tradare il cluster — POSIZIONARSI prima del move che lo causa,
        oppure PROTEGGERE posizioni che hanno stop nei cluster identificati.
```

---

## Data sources

```
LIQUIDATION DATA:
  CoinGlass /api/futures/liquidation/exchange-list?range=24h&symbol=BTC
    -> liquidation per exchange ultimi 24h, classified long/short
  CoinGlass /api/futures/liquidation/aggregated-history (4h chunks workaround
    per heatmap che è gated Hobbyist)
  Coinalyze /liquidation-history?symbols=...&interval=1hour&limit=24
    -> serie storica liquidazioni cumulative
  CoinGlass /api/futures/liquidation/heatmap (★ Standard tier — ricostruzione
    da chunks 4h se Hobbyist)

GEX STRUCTURE (assunto in context.json — popolato da gex-analysis):
  context.confluence_history -> cluster gamma+ con str
  context.lw_diff             -> ask/bid walls + diff session-to-session
  context.last_close_per_tf  -> POC, VAH, VAL del Volume Profile

OI DATA (per confermare partecipazione):
  Coinalyze /open-interest-history?symbols=...&interval=15min&limit=96
  CoinGlass /api/futures/open-interest/exchange-list
  
PRICE WS (real-time):
  Bitget WS pubblico (engine/price_feeds.py)
  Binance WS pubblico (cross-validation)
```

---

## Algoritmo di forecast

### Step 1 — Build cluster map (cron 30min)

```
Per ogni asset (BTC, ETH):
  1. Fetch ultime 24h liquidations per livello prezzo (granularità $50 BTC, $5 ETH)
  2. Aggregate per zone: histogram con cluster detection (peak finding)
  3. Classify per side: long_liq_cluster (sotto prezzo) vs short_liq_cluster (sopra)
  4. Filter cluster: minimum $5M cumulative liq per essere "rilevante"

OUTPUT:
  liquidation_map = {
    "BTC": {
      "above": [
        {"price": 65500, "cum_short_liq_usd": 28e6, "cum_long_liq_usd": 0,
         "magnitude": "high"},
        {"price": 66200, "cum_short_liq_usd": 12e6, "magnitude": "medium"}
      ],
      "below": [
        {"price": 62800, "cum_long_liq_usd": 41e6, "magnitude": "very_high"},
        {"price": 61500, "cum_long_liq_usd": 22e6, "magnitude": "high"}
      ],
      "current_price": 64200
    }
  }
```

### Step 2 — Overlay GEX walls

```
Per ogni cluster identificato:
  1. Trova GEX wall più vicino (sopra e sotto)
  2. Distanza prezzo cluster vs prezzo wall
  3. Classifica relazione:

     CLUSTER UNDER WALL+ (più frequente, magnete + freno):
       Cluster long_liq sotto gamma+ wall sopra prezzo
       -> il prezzo tende a SCENDERE al cluster, poi rimbalzare al wall
       -> "stop run pattern": flush long, then bounce
     
     CLUSTER OVER WALL+ (squeeze setup):
       Cluster short_liq sopra gamma+ wall (resistenza)
       -> se il prezzo rompe il wall, accelera al cluster (magnete)
       -> "gamma flip + cascade pattern"
     
     CLUSTER IN GAMMA- ZONE (acceleratore):
       Cluster nella zona gamma- = movimento amplificato verso il cluster
       -> "free fall" o "free rocket"
     
     CLUSTER ISOLATED (no GEX nearby):
       Solo cluster, niente walls -> magnete debole, segnale incerto
```

### Step 3 — Forecast zone + probabilità

```
Per ogni cluster, calcola probability of hit nei prossimi 24h:

base_probability = magnitude_factor (0.4 small, 0.65 medium, 0.85 high)

modifiers:
  + 0.10 se distanza < 1% (vicino in casino)
  + 0.15 se OI in crescita (partecipazione conferma move)
  + 0.10 se vacuum zone tra prezzo e cluster
  + 0.05 se L/S ratio in crowding nella direzione contrarian al cluster
  - 0.20 se gamma+ wall MAGGIORE blocca la rotta (str > 8.5)
  - 0.15 se hours_to_macro_event < 6 (volatilità erratica)
  + 0.10 se whale_alerts segnalano direzione coerente

probability_clipped = clip(base + modifiers, 0.05, 0.95)

timeframe_estimate:
  Vacuum zone + high magnitude: 2-6 ore
  Con resistance intermedia: 8-24 ore
  Cluster < 0.5% lontano: 30min - 2h
```

### Step 4 — Pattern operativi identificati

**Pattern A — STOP RUN (long flush + bounce)**
```
SETUP:
  Cluster long_liq cumulative > $30M sotto prezzo
  GEX gamma+ wall (str > 7) entro 1% sotto cluster
  Prezzo > vacuum zone tra current e cluster
  L/S ratio crowding long
  OI crescente (long buildup recente)

FORECAST:
  Move sequence: prezzo → flush al cluster → bounce al wall
  Timing: 4-12h
  Magnitudo bounce post-flush: 50-80% della distanza vs wall

USO TATTICO:
  - Se hai long aperto sotto: ATTENZIONE ai stop
  - Posizionati per long bounce DOPO il flush (entry @ wall, stop sotto cluster)
  - NON shortare in anticipo (timing impossibile)
```

**Pattern B — GAMMA FLIP CASCADE (squeeze esplosivo)**
```
SETUP:
  Cluster short_liq > $20M sopra resistenza gamma+ str > 7
  Volume crescente nell'avvicinamento alla resistenza
  Bid nuovi sopra resistenza in LW diff (buyer si posizionano sopra)
  OI crescente

FORECAST:
  Move sequence: rottura wall → cascade short liq → accelerazione fino a prossima resistenza
  Timing: 1-4h dopo break wall confermato (close 1h)
  Magnitudo: 60-100% della distanza verso prossimo gamma+ wall

USO TATTICO:
  - Setup long su retest del wall rotto (gamma flip → supporto)
  - Target = livello gamma+ successivo
  - Stop = sotto wall rotto
```

**Pattern C — FREE FALL (cluster in gamma-)**
```
SETUP:
  Cluster long_liq in zona gamma-
  Nessun gamma+ wall fino al cluster
  L/S ratio crowding long
  OI in calo (de-leveraging già iniziato)

FORECAST:
  Move sequence: discesa accelerata, magnetic drop
  Timing: 1-3h, può accelerare drasticamente
  Magnitudo: spesso overshoot del cluster

USO TATTICO:
  - NON comprare il dip (gamma- amplifica)
  - Stop ampi (≥ 2%) o no-trade
  - Riposizionamento solo dopo reversal pattern confermato
```

**Pattern D — PIN RISK (max pain magnete venerdì)**
```
SETUP:
  Venerdì options expiry T-24h
  Max pain level (CoinGlass /api/option/max-pain) > 1% lontano dal prezzo
  Cluster liquidation tra prezzo e max pain

FORECAST:
  Prezzo gravita verso max pain entro l'expiry
  Cluster nel mezzo possono essere "raggiunti" prima del pin

USO TATTICO:
  - No swing nuovi nel giorno expiry
  - Stop allargati (1.5x normale) entro 6h dall'expiry
```

---

## Output: scrittura context.json + push notify

### context.liquidation_forecast (refresh 30min)
```json
{
  "liquidation_forecast": {
    "ts": "2026-05-01T12:00:00Z",
    "ttl_hours": 4,
    "BTC": {
      "current_price": 64200,
      "active_patterns": [
        {
          "pattern": "STOP_RUN",
          "direction": "DOWN",
          "target_price": 62800,
          "target_distance_pct": -2.18,
          "probability": 0.72,
          "magnitude": "high",
          "timeframe_hours": "4-12",
          "trigger_conditions": ["L/S > p85", "OI crescente", "vacuum zone"],
          "blocking_levels": [],
          "narrative": "Cluster long liq $41M @ $62.8k. Gamma+ wall str 8.2 @ $63.0k.
                        Vacuum 1.5%. Stop run probabile, bounce al wall."
        },
        {
          "pattern": "PIN_RISK",
          "direction": "PIN",
          "target_price": 65000,
          "max_pain": 65000,
          "probability": 0.55,
          "timeframe_hours": "T-24h to expiry",
          "narrative": "Options expiry venerdì. Max pain $65k, prezzo $64.2k."
        }
      ],
      "key_levels": {
        "long_liq_clusters": [
          {"price": 62800, "cum_usd": 41e6, "magnitude": "very_high"},
          {"price": 61500, "cum_usd": 22e6, "magnitude": "high"}
        ],
        "short_liq_clusters": [
          {"price": 65500, "cum_usd": 28e6, "magnitude": "high"},
          {"price": 66200, "cum_usd": 12e6, "magnitude": "medium"}
        ]
      }
    }
  }
}
```

### Alert push (probability > 0.7 + magnitude high)
```
[LIQ FORECAST] BTC STOP_RUN target $62.8k (-2.2%, prob 72%)
Pattern: cluster long liq $41M sotto gamma+ str 8.2.
Timeframe: 4-12h. Stop attualmente in zona = at risk.
Suggested: review stop SL su long aperti BTC.
```

---

## Cross-reference con altre skill

```
LETTA DA QUESTA SKILL:
  context.confluence_history  <- gex-analysis (gamma+ walls + str)
  context.lw_diff             <- gex-analysis (LW changes)
  context.macro_regime        <- macro-regime-monitor (modulates probabilità)
  context.derivatives         <- derivatives-dashboard (OI/L/S conferma)
  scratchpad.whale_alerts     <- whale-onchain-monitor (direzione confermata)
  
DELEGA A:
  price-alert-trigger    (imposta alert sui livelli forecast)
  scalp-execution        (per setup long bounce post-flush)
  risk-forward           (se PIN_RISK identificato, integra calendar event)

LETTO DA:
  gex-analysis           (PASSO 5 — scenario operativi enriched con liq forecast)
  scalp-execution        (pre-validation Setup 1/3 con liquidation map)
  proactive-scout        (asset con liq forecast HIGH = priority scan)

SCRIVE:
  context.liquidation_forecast (autoritativo)
  retrospettive.md (entry per pattern confermati o invalidati)
```

---

## Errori da evitare

```
Tradare il cluster come trigger:
  Il cluster è UN MAGNETE. Trigger è il break del livello che lo precede.
  Comprare al cluster "perché è scritto $41M long liq" = cattura coltello.

Confondere probabilità con certezza:
  72% probability = 28% non si avvera. Sempre size congruente con prob.

Ignorare blocking levels:
  Gamma+ wall MAGGIORE (str > 8.5) tra prezzo e cluster = ostacolo serio.
  Probability deve scendere significativamente.

Forecast in macro event imminent:
  hours_to_event < 6 = volatilità erratica, modello statistico fallisce.
  Sempre downgrade probability con flag.

Sovrastimare cluster < $5M:
  Cluster troppo piccoli sono rumore retail. Sempre filtrare cumulative.

Non aggiornare il forecast dopo move:
  Quando il cluster è stato HIT, va invalidato e il forecast ricalcolato.
  Stale forecast è peggio di nessun forecast.
```

---

## Threshold operativi

```
CLUSTER MIN:           cumulative > $5M (BTC), > $1.5M (ETH)
CLUSTER VERY_HIGH:     > $30M (BTC), > $10M (ETH)
PROBABILITY MIN:       0.55 per emit alert
DISTANCE MAX:          5% (oltre, signal degrades)
TTL FORECAST:          4 ore (ricalcola se stale)
```
