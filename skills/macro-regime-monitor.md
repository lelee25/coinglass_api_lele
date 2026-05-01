---
name: macro-regime-monitor
description: >
  Classifica il regime macro globale di crypto (CAPITULATION / RECOVERY / NEUTRAL /
  EUPHORIA / RISK-OFF) leggendo 12 indici on-chain CoinGlass + ETF flow + DXY proxy
  + dominance. Skill SLOW (cron 4h, scrive context.json.macro_regime). Le altre
  skill leggono il regime come MODIFIER dei loro segnali, non lo ricalcolano.
  Trigger: "che regime siamo?", "macro check", "siamo in euforia?", "capitulation?",
  "risk-off?", "ETF flow", "MVRV", "Pi Cycle", "Bubble Index", "200W RSI",
  "Puell Multiple", "DXY crypto", "BTC dominance", "macro update", "regime update",
  "modifier macro", "headwind/tailwind".
  NON tradare in base al regime — il regime modifica i pesi. Il trade decide
  gex-analysis, scalp-execution, price-alert-trigger.
---

# Macro Regime Monitor — il modificatore globale

## Filosofia: il regime non dice quando, dice quanto pesare i segnali

Il regime macro **non è un trigger di trade**. È il moltiplicatore che dice
quanto pesare i segnali delle altre skill:

```
Stesso segnale GEX (str=8, gamma+ a $X):
  In RECOVERY  -> setup long edge ALTO (trend continuation favorevole)
  In EUPHORIA  -> setup long edge BASSO (mean reversion imminente)
  In RISK-OFF  -> setup long IGNORATO (size -30% o no-trade automatico)
```

Il regime cambia in 4h-7gg. È il "tempo geologico" del trading. Le skill veloci
(price-alert-trigger, scalp-execution) lo leggono come read-only; questa skill
è l'unica che lo aggiorna.

---

## Data sources (data fornito dal Claude server tramite tool precostruiti)

```
LONG-TERM ON-CHAIN OSCILLATORS (CoinGlass /api/index/*):
  /bitcoin-bubble-index           -> 0-100, soglia euforia > 80
  /pi-cycle-indicator             -> top signal binario
  /puell-multiple                 -> miner stress, < 0.5 = capitulation, > 4 = top
  /2-year-ma-multiplier           -> regime macro long
  /200w-ma-heatmap                -> RSI 200W, oversold < 30, overbought > 80
  /mvrv                           -> market vs realized, < 1 = capit., > 3.5 = euph.
  /sopr (gated, fallback skip)
  /lth-supply-distribution        -> long-term holder behavior
  /reserve-risk                   -> macro top-bottom oscillator

INSTITUTIONAL FLOW (CoinGlass):
  /api/etf/bitcoin/flow-history   -> netflow daily ETF spot BTC USA
  /api/etf/ethereum/flow-history  -> netflow daily ETF spot ETH USA
  /api/etf/solana/flow-history    -> SOL ETF (early stage)
  /api/hk-etf/bitcoin/flow-history -> Hong Kong (Asia session signal)
  /api/coinbase-premium-index     -> US institutional vs retail premium
  /api/grayscale-premium/list     -> GBTC discount/premium history

CROSS-ASSET (CoinGecko Demo):
  /global                          -> total_market_cap, btc_dominance, eth_dom
  /exchange_rates                  -> BTC vs USD/EUR/JPY/CNY (DXY proxy inverso)
  /global/decentralized_finance_defi -> DeFi mcap, DeFi dominance

REFRESH POLICY:
  Indici on-chain      -> daily refresh (cron 00:30 UTC)
  ETF flow             -> daily refresh + intraday se US market open
  Cross-asset          -> 4h refresh
  Regime ricomputato   -> 4h
```

---

## I 5 regime macro (definizioni quantitative)

### 1. CAPITULATION — fondi reali, edge contrarian long
```
CONDIZIONI (almeno 4 su 6):
  [ ] MVRV < 1.0
  [ ] Puell Multiple < 0.5
  [ ] Bitcoin Bubble Index < -2 (dataset z-scored)
  [ ] 200W RSI < 30
  [ ] ETF netflow outflow per > 5 sessioni consecutive
  [ ] BTC dominance crescente in calo prezzo (flight to safety dentro crypto)

PSICOLOGIA: panic selling esaurito, retail capitulato, miners in stress.
EDGE: posizioni long contrarian con stop ampi, scale-in tollerato.
DURATA TIPICA: 2-12 settimane.
```

### 2. RECOVERY — trend continuation favorevole
```
CONDIZIONI (almeno 3 su 5):
  [ ] MVRV in range 1.0-2.0 e in aumento
  [ ] 200W RSI 30-60 e in aumento
  [ ] ETF netflow positive per > 3 sessioni consecutive (mixed OK)
  [ ] BTC dominance stabile o leggermente calante (rotation in alts)
  [ ] Coinbase Premium positivo

PSICOLOGIA: capitale istituzionale rientra, retail cauto.
EDGE: trend continuation, breakout reali, momentum-based long.
DURATA TIPICA: 1-4 mesi.
```

### 3. NEUTRAL — usa soglie standard
```
CONDIZIONI: nessuno dei 5 regime soddisfatto, oppure segnali misti.
PSICOLOGIA: indecisione strutturale, mercato in attesa catalizzatore.
EDGE: nessun bias macro. Le skill veloci usano thresholds standard.
DURATA TIPICA: 1-3 settimane (regime di transizione).
```

### 4. EUPHORIA — edge contrarian short
```
CONDIZIONI (almeno 4 su 6):
  [ ] MVRV > 3.5
  [ ] Puell Multiple > 4
  [ ] Bitcoin Bubble Index > +2
  [ ] 200W RSI > 80
  [ ] ETF netflow inflow per > 7 sessioni consecutive con accelerazione
  [ ] Pi Cycle Indicator: TOP triggered

PSICOLOGIA: FOMO retail al massimo, leverage retail estremo.
EDGE: short contrarian su resistenze gamma+, long-only riduce size -50%.
DURATA TIPICA: 2-8 settimane prima di rollover.
ATTENZIONE: euforia può estendersi più del previsto. Non shortare blind —
            aspetta segnale tecnico (rejection 4h, OI divergenza).
```

### 5. RISK-OFF — size globalmente ridotta
```
CONDIZIONI (almeno 3 su 5):
  [ ] DXY proxy > 2σ sopra media 30gg (USD strength)
  [ ] ETF netflow outflow > 2 sessioni con accelerazione
  [ ] BTC dominance in salita rapida + total mcap in calo (flight)
  [ ] Coinbase Premium negativo
  [ ] Hong Kong ETF flow contrario a USA (divergenza Asia/USA)

PSICOLOGIA: macro headwind, capitale esce da risk assets.
EDGE: tutte le posizioni size -30%, no swing nuovi, scalp solo Setup 1/3
      (rimbalzo + breakdown), stop minimo 1.5%.
DURATA TIPICA: 1-3 settimane (può sovrapporsi a CAPITULATION).
```

---

## Algoritmo di classificazione

```
STEP 1 — Calcola gli score di ogni indicatore (z-score normalizzato 30gg)
  score_i = (value_i - mean_30d_i) / std_30d_i

STEP 2 — Assegna voti a ciascun regime
  capitulation_votes = sum([
    1 if mvrv < 1.0,
    1 if puell < 0.5,
    1 if bubble_z < -2,
    1 if rsi200w < 30,
    1 if etf_streak_out >= 5,
    1 if dom_rising_in_falling_price
  ])
  ... idem per gli altri 4 regime

STEP 3 — Soglia di attivazione
  Regime "vincente" = quello con votes >= soglia (4 per CAPITULATION/EUPHORIA,
  3 per RECOVERY/RISK-OFF). Se nessuno -> NEUTRAL.

STEP 4 — Tie breaking
  Se due regime scorrono pari, vince quello con magnitudine indici maggiore
  (somma |z-score|). RISK-OFF e CAPITULATION possono coesistere — scrivi
  entrambi con primario il più "votato".

STEP 5 — Smoothing temporale
  Non cambiare regime se quello precedente è valido da < 3 cicli (12h).
  Evita whipsaw su soglie marginali.
```

---

## Output: scrittura context.json.macro_regime

```json
{
  "macro_regime": {
    "primary": "RECOVERY",
    "secondary": null,
    "score": 7.2,
    "ts": "2026-05-01T08:00:00Z",
    "ttl_hours": 4,
    "key_signals": {
      "mvrv": 1.42,
      "puell": 1.1,
      "bubble_index_z": -0.3,
      "rsi_200w": 48.5,
      "etf_btc_netflow_7d_usd": 1.8e9,
      "etf_eth_netflow_7d_usd": 0.4e9,
      "btc_dominance": 56.4,
      "dxy_proxy_z": -0.8
    },
    "modifiers_for_other_skills": {
      "long_setups_weight": 1.2,
      "short_setups_weight": 0.8,
      "stop_min_pct": 1.0,
      "size_factor": 1.0,
      "swing_allowed": true,
      "scalp_allowed_setups": [1, 2, 3, 4, 5, 6]
    },
    "narrative": "Recovery confermato: MVRV in salita, ETF inflow streak 4gg,
                  dominance stabile. Trend continuation long ha edge superiore."
  }
}
```

---

## Tabella modifier per regime — letta dalle altre skill

```
                  | long_w | short_w | stop_min | size_f | swing | setups_blocked
------------------|--------|---------|----------|--------|-------|----------------
CAPITULATION      |  1.4   |   0.5   |   2.0%   |  1.0   |  YES  | 3 (no breakdown)
RECOVERY          |  1.2   |   0.8   |   1.0%   |  1.0   |  YES  | nessuno
NEUTRAL           |  1.0   |   1.0   |   1.0%   |  1.0   |  YES  | nessuno
EUPHORIA          |  0.6   |   1.3   |   1.5%   |  0.7   | RIDOTTO| 4 (no breakout)
RISK-OFF          |  0.5   |   1.1   |   1.5%   |  0.7   |  NO   | 4, 6 (no breakout/div)
```

Le altre skill leggono questa tabella e moltiplicano l'edge:
```
edge_finale = edge_base * (long_w o short_w) * size_factor
```

---

## Formato output narrativo (per report user-facing)

```
=== MACRO REGIME UPDATE — [date hh:mm UTC] ===

REGIME PRIMARIO: [nome]   (score [X.X]/10, confidence [HIGH/MED/LOW])
REGIME SECONDARIO: [nome o "nessuno"]

INDICATORI CHIAVE:
  On-chain:
    MVRV:           [X.XX]  ([above/below] threshold)
    Puell Multiple: [X.XX]  ([interpretation])
    200W RSI:       [XX.X]  ([zone])
    Bubble Index:   [X.X]   ([z-score])

  Institutional:
    ETF BTC 7d:     [+/-$X.XB]  ([streak in/out, X gg])
    ETF ETH 7d:     [+/-$X.XB]
    Coinbase Prem:  [+/-X.XX%]

  Cross-asset:
    BTC dominance:  [XX.X%]    ([rising/falling])
    DXY proxy:      [z=X.X]    ([USD strength/weakness])

CAMBIAMENTO DA ULTIMO CICLO ([X]h fa):
  [transitions: es. "RECOVERY -> EUPHORIA: MVRV crossed 3.5"]
  [oppure "stabile in [regime]"]

IMPLICAZIONI OPERATIVE:
  Long setups:    moltiplicatore [X.X], allowed: [list]
  Short setups:   moltiplicatore [X.X], allowed: [list]
  Stop minimo:    [X.X%]
  Size factor:    [X.X]
  Swing nuovi:    [YES/NO/REDUCED]

NEXT REVIEW: [timestamp + 4h]
```

---

## Errori da evitare

```
Tradare il regime direttamente:
  Il regime NON è un trade signal. EUPHORIA non significa "short adesso".
  Aspetta segnale tecnico (gex-analysis o scalp-execution) e applica modifier.

Cambiare regime troppo spesso:
  Il smoothing temporale (3 cicli) esiste per un motivo. Whipsaw di regime
  produce whipsaw di size factor — gli agent veloci lo leggono in continuo.

Sovrapesare i singoli indici:
  L'algoritmo è di voting. Un singolo indice in zona estrema NON forza il regime.
  Es. MVRV > 3.5 da solo non è EUPHORIA se gli altri 5 indicatori sono neutri.

Ignorare il regime secondario:
  RISK-OFF + CAPITULATION coesistono in panic con USD strong. Il modifier deve
  considerare entrambi (la stop_min più larga dei due, la size più piccola).

Dimenticare il TTL:
  Se ts > 6h, il regime è stale — le skill veloci dovrebbero re-triggerare
  il refresh prima di leggere. Il claude server gestisce TTL/cache.
```

---

## Cross-reference con altre skill

```
LETTO DA:
  gex-analysis            -> usa long_w/short_w come macro_modifier (PASSO 3)
  scalp-execution         -> usa setups_blocked per filtro filtro 2 (eventi)
  price-alert-trigger     -> usa size_factor + stop_min nella checklist
  derivatives-dashboard   -> usa il regime per pesare divergenze (P1)

SCRIVE:
  context.json.macro_regime (autoritativo)
  retrospettive.md         (entry quando avviene transizione di regime)

INTEGRAZIONE CON funding-arb-detector:
  Funding divergente cross-exchange in RISK-OFF -> stress confermato
  Funding convergente in EUPHORIA -> rischio flush imminente
```
