---
name: proactive-scout
description: >
  Scouting periodico dell'universo trading per identificare opportunità PRIMA
  che l'utente o un alert le segnalino. Skill PROATTIVA (cron 30min) che scansiona
  in parallelo tutti gli asset monitorati + universo discovery (top 250 mcap +
  top trending) e propone i 3 setup migliori del momento con score quantitativo.
  Trigger: "scout opportunita", "cosa sta muovendo", "qualcosa di interessante",
  "trovami un trade", "scan universo", "discovery", "top setup ora",
  "cosa offre il mercato", "scouting periodico", "auto-scan", "ranking setup",
  "best opportunity now". Output: top 3 trade candidates + signal score + delega
  a scalp-execution o gex-analysis per validation. NON apre trade direttamente.
---

# Proactive Scout — discovery dell'universo trading

## Filosofia: l'agent attende non basta — deve cercare

Le skill reattive (price-alert-trigger) aspettano un evento. Le skill periodiche
(gex-analysis cron 4h) analizzano gli asset core. **Tra i due c'è un buco**:
asset che si stanno muovendo MA non hanno alert impostato e non sono nel
core universe. Spesso le opportunità migliori nascono lì.

```
PIPELINE CLASSICA:    asset core (BTC/ETH) -> alert -> reazione
PIPELINE CON SCOUT:   universo top 250 + trending -> ranking -> top 3 -> delega
```

Lo scout è **discovery + ranking**, non execution. Identifica candidati,
li score, e delega la decisione finale alle skill specialistiche.

---

## Data sources

```
UNIVERSO ASSET DA SCANNARE (cron 30min):
  Core (sempre):
    BTC, ETH, SOL, BNB, XRP, DOGE
  Top 50 by market cap (refresh daily):
    CoinGecko /coins/markets?per_page=50&order=market_cap_desc
  Top 10 trending 24h:
    CoinGecko /search/trending
  Top 10 gainers/losers 24h (filtra per volume > $50M):
    CoinGecko /coins/markets order=price_change_percentage_24h_desc
  Top onchain pools attention:
    CoinGecko /onchain/networks/eth/trending_pools
    CoinGecko /onchain/tokens/info_recently_updated

SEGNALI DA AGGREGARE PER OGNI ASSET:
  Da CoinGlass:
    /api/futures/open-interest/exchange-list -> OI snapshot multi-venue
    /api/futures/long-short-account-ratio    -> L/S ratio Binance
    /api/futures/funding-rate/exchange-list  -> funding multi-venue
  Da Coinalyze:
    /open-interest-history?interval=15min&limit=4 -> ΔOI 1h
    /long-short-ratio-history?interval=1hour&limit=8 -> ΔL/S 8h
  Da CoinGecko:
    Price 1h/24h change, volume 24h, market cap rank
  Da context (già popolato):
    macro_regime.modifiers per filtrare setups bloccati dal regime
    whale_alerts per asset menzionati
    funding_signal per outlier divergenti
```

---

## Algoritmo di scoring (per ogni asset)

```
score_total = sum dei seguenti contributi (range -10 a +10, sign = direzione):

A) MOMENTUM SCORE (pesa 25%)
   price_change_1h_pct sign-aware
   +3 se |1h_change| > 1% AND |1h_change| < 4% (momentum sano)
   -2 se |1h_change| > 5% (parabolic, late entry)
   +1 se 24h_change concorda con 1h direction (continuation)
   -1 se 24h_change discorda (reversal in corso)

B) DERIVATIVES SCORE (pesa 30%)
   +3 se OI crescente AND price aligned (TREND_GENUINE)
   +2 se OI crescente AND price contrario (NEW_SHORTS o NEW_LONGS — direzionale)
   -1 se OI scende AND price si muove (de-leveraging — fragile)
   +2 se L/S ratio contrarian al move recente (squeeze potenziale)
   +3 se funding outlier > p95 calibrato (tradeable basis)

C) STRUCTURAL SCORE (pesa 25%)
   +2 se prezzo vicino (< 0.5%) a livello GEX str > p85 (delegato a gex-analysis)
   +3 se whale_alert HIGH per quell'asset, direzione coerente
   -2 se whale_alert HIGH direzione contraria (rischio elevato)

D) MACRO MODIFIER (pesa 20%)
   * (macro_regime.long_w o short_w) per direzione del setup
   * etf_signal modifier se asset == BTC/ETH
   * funding_signal contrarian factor

E) DISQUALIFIERS (set score = 0):
   - Volume 24h < $20M (illiquid, slippage > edge)
   - Asset blocked by regime (es. memecoin in RISK-OFF)
   - Hours_to_macro_event < 0.5h
   - Già aperta posizione su quell'asset (no duplicazione)
```

---

## Output: ranking top 3 + delega

```
=== PROACTIVE SCAN — [data ora UTC] ===

UNIVERSO SCANNATO:
  Asset count:     [N]
  Disqualified:    [N] ([motivi: illiquid X, regime block Y, ...])
  Score range:     [-X.X to +Y.Y]

TOP 3 OPPORTUNITIES:

#1 — [asset] @ $[prezzo]  |  score [+X.X]  |  bias [LONG/SHORT]
  Momentum:        [+/-X.X]  ([1h: +X.X%, 24h: +X.X%])
  Derivatives:     [+/-X.X]  (OI [trend], L/S [val], funding [val])
  Structural:      [+/-X.X]  ([nearest GEX, whale flag])
  Macro modifier:  [x.X]     ([regime] coherent: [Y/N])
  
  Suggested next step:
    [delega skill]: [skill_name] su [asset]
    [conferma]: [cosa cercare per confermare]
  
  Risk:
    [main risk if entered now]

#2 — [asset]  ...
#3 — [asset]  ...

WATCHLIST (score > 3 ma non top 3):
  [list 3-5 asset con score sub-soglia ma interessanti per cron successivo]

NEXT SCAN: [now + 30min]
```

---

## Skill di delega per ogni candidato

```
PER OGNI TOP 3, suggerire chi prendere il caso:

Se asset == core (BTC/ETH):
  -> gex-analysis (analisi profonda)
  -> in parallelo: derivatives-dashboard
  -> output a scratchpad.opportunity_pipeline

Se asset == top 50 ma non core:
  -> chart-pattern-recognition (analisi tecnica visuale)
  -> scalp-execution (cerca setup tra i 6 disponibili)

Se asset == altcoin DEX:
  -> whale-onchain-monitor (verifica concentration velocity)
  -> chart-pattern-recognition

Se asset == funding outlier:
  -> funding-arb-detector (lettura cross-exchange)
  -> price-alert-trigger (imposta alert sul cut funding)
```

---

## Cross-reference con altre skill

```
LETTA DA QUESTA SKILL:
  context.macro_regime          <- macro-regime-monitor
  context.etf_signal            <- etf-flow-interpreter
  context.funding_signal        <- funding-arb-detector
  scratchpad.whale_alerts       <- whale-onchain-monitor
  context.derivatives           <- derivatives-dashboard
  scratchpad.active_positions   (per evitare duplicate)
  calibration.asset_thresholds  <- references/calibration-thresholds.md
  setup_weights                 <- references/spec-adaptive-weights.md (se esiste)

DELEGA A (parallelo, sub-skill):
  gex-analysis             (asset core)
  scalp-execution          (asset top 50)
  whale-onchain-monitor    (altcoin DEX o concentration alert)
  funding-arb-detector     (outlier funding)
  chart-pattern-recognition (sempre per visualizzazione)

SCRIVE:
  scratchpad.opportunity_pipeline (top 3 candidates con score, ts)
  scratchpad.scout_log (rolling 24h, watchlist storico)
```

---

## Errori da evitare

```
Aprire trade direttamente dallo scout:
  Lo scout NON esegue. Identifica e delega. La validazione finale
  spetta alla skill specialistica e all'utente/agent operativo.

Score normalizzati senza weight macro:
  Senza il modifier macro_regime, lo scout proporrebbe long in EUPHORIA.
  Sempre applicare il regime weight come moltiplicatore finale.

Scoring fixed all'asset:
  Score di BTC e di un memecoin non sono comparabili in valore assoluto.
  Sempre normalizzare per asset class (BTC/ETH separati da alts).

Cron troppo frequente:
  30min è il minimum. Più frequente non aggiunge alpha (segnali derivati
  refresh 5-15min comunque) ma esaurisce rate limit CoinGecko Demo.

Ignorare disqualifier:
  Un asset con score 8 ma volume $5M = trap. Sempre filtrare disqualifier
  PRIMA di calcolare score finale.

Non logger gli "scartati":
  Asset che sono stati a score 7 e poi scesi a 3 sono dato prezioso per
  retrospettiva (false positive analysis). Salvare watchlist storico.
```

---

## Threshold operativi (default — calibrabili)

```
SCAN UNIVERSE:
  asset_count_max: 100  (oltre, costo CoinGecko Demo eccessivo)
  cron_frequency_min: 30
  parallel_fetch: 10    (rate limiter constraint)

SCORE THRESHOLDS:
  top_3_min_score: 5.0  (non proporre se nessun asset > 5)
  watchlist_min: 3.0
  disqualifier_volume_24h_usd: 20e6

DELEGA:
  max_parallel_delegations: 3 (contemporanee, sub-skill)
```
