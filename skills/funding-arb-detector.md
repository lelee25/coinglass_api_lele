---
name: funding-arb-detector
description: >
  Rileva divergenze di funding rate cross-exchange (Bitget, Binance, Bybit, OKX)
  e confronta predicted funding (Coinalyze ★ unico) vs current per anticipare
  shift di regime nelle prossime 8h. Risolve due problemi reali del sistema:
  (1) cost-aware sizing — quanto paga il funding il trade attuale, (2) signal —
  funding divergente = stress strutturale o mispricing tradeable.
  Trigger: "funding rate", "predicted funding", "basis cross-exchange",
  "arb opportunity", "Bitget funding", "Binance vs OKX funding", "funding cost",
  "8h funding payment", "funding flip", "funding divergence", "spread basis",
  "funding spike". NON è uno scalp signal — è un cost/risk modifier per
  posizioni perp esistenti + early warning per regime shift.
---

# Funding Arb Detector — divergenze cross-exchange

## Filosofia: il funding è un thermometer, non un trigger

Il funding rate misura la pressione tra long e short su un perp. Quando
diverge tra exchange, succede una di due cose:

```
1. MISPRICING TRADEABLE (raro):
   Bitget paga +25 bps/8h, Binance +5 bps/8h.
   Stesso underlying, prezzo simile.
   -> Spread di 20 bps annualizzato = ~218% APY. Bisogna chiedersi PERCHE.
   -> Solitamente: liquidity bassa Bitget, retail squeezato in long.

2. STRESS SIGNAL (frequente):
   Tutti gli exchange convergono ai limiti di funding (es. >+30 bps)
   = euphoria; tutti negativi = capitulation imminente.
   -> Non arb: signal di posizionamento estremo.
```

**L'edge primario di questa skill non è arbitrare.** È:
- Dare cost-awareness all'agent che esegue su Bitget mentre il funding sale
- Dare leading signal di shift di regime (predicted vs current)
- Identificare exchange-specific stress (un exchange diverge molto = retail
  intrappolato lì, contrarian opportunity sul venue)

---

## Data sources

```
COINALYZE (free 40 rpm — verificato §22, smoke_coinalyze.py):
  /funding-rate?symbols=BTCUSDT_PERP.A,BTCUSDT.6,BTCUSDT.3
    -> snapshot funding rate cross-exchange in singola call
    -> Symbol code: A=Binance, 6=Bybit, 3=OKX, ... (mapping da /exchanges)
  /predicted-funding-rate?symbols=BTCUSDT_PERP.A   ★ unico
    -> funding rate previsto per il prossimo periodo 8h
    -> leading 1-8h sul current
  /funding-rate-history?symbols=...&interval=1hour&from=...&to=...
    -> serie storica per calcolo z-score

COINGLASS (Hobbyist verificato §22):
  /api/futures/funding-rate/exchange-list?symbol=BTC
    -> funding cross-venue includendo Bitget (non in Coinalyze symbol set)
  /api/futures/funding-rate/oi-weight-history -> funding pesato per OI
  /api/futures/funding-rate/vol-weight-history -> funding pesato per volume

CALCOLI CLIENT-SIDE:
  spread_bps = (max_funding - min_funding) * 10000 / 8h_period
  apy_equivalent = spread_bps / 8h * 24 * 365 (annualizzato)
  z_score(spread, history_30d) -> calibrazione percentile
```

---

## I 3 segnali leggibili

### Segnale 1 — DIVERGENCE STRESS (uno o più exchange diverge)
```
CONDIZIONI:
  spread_bps cross-exchange > 8 bps (default — calibrabile rolling 30gg)
  Almeno 1 exchange in zona estrema (> 95° percentile o < 5° percentile)
  Persistente per ≥ 2 cicli (i.e. 2 funding settlement = 16h)

INTERPRETAZIONE:
  Mispricing strutturale, l'exchange diverge ha posizionamento sbilanciato.
  Es. Bitget +30 bps mentre Binance +8 bps -> retail Bitget over-long
  -> contrarian short Bitget al funding cut

OPERATIVO:
  NON è arbitraggio puro (slippage e size limits negano spesso il funding edge)
  È un signal: l'exchange diverge è "il debole della catena"
  -> evita open trades nella direzione del crowd su quell'exchange
  -> considera contrarian se segnale tecnico aggiuntivo

ALERT LEVEL: MEDIUM
```

### Segnale 2 — PREDICTED SHIFT (Coinalyze leading)
```
CONDIZIONI:
  abs(predicted_funding - current_funding) > 5 bps
  La direzione è coerente cross-exchange (no rumore)

INTERPRETAZIONE:
  Il funding sta per cambiare regime nelle prossime 8h.
  Es. current +12 bps, predicted +2 bps -> rilassamento posizioni long
  -> probabile inizio de-leveraging
  Es. current -5 bps, predicted +8 bps -> short squeeze in formazione
  -> potenziale squeeze rialzista nelle prossime ore

OPERATIVO:
  Combinare con derivatives-dashboard P2 (L/S ratio):
  - Predicted funding sale + L/S ratio in flessione = squeeze imminente, long
  - Predicted funding crolla + L/S ratio crescente = top retail, short setup

ALERT LEVEL: HIGH (raro, alta predittività)
```

### Segnale 3 — REGIME EXTREME (tutti convergono ai limiti)
```
CONDIZIONI:
  Mediana funding cross-exchange > 25 bps per ≥ 3 cicli (24h)
  o < -10 bps per ≥ 3 cicli (24h)
  Spread cross-exchange < 5 bps (convergenza)

INTERPRETAZIONE:
  Tutti i venue concordano = posizionamento globale estremo.
  > 25 bps mediana = euforia retail strutturale -> top imminente
  < -10 bps mediana = capitulation -> bottom imminente

OPERATIVO:
  Modifier per macro-regime-monitor (input addizionale al regime EUPHORIA/CAPIT)
  Per le skill veloci: peso contrarian +30% sul lato saturo
  Stop logici sui livelli GEX vicini, NON inseguire il momentum

ALERT LEVEL: STRUCTURAL (entra nel regime classification)
```

---

## Algoritmo di detection

```
STEP 1 — Snapshot cross-exchange (cron 1h)
  Chiama Coinalyze /funding-rate per BTC + ETH multi-symbol
  Chiama Coinalyze /predicted-funding-rate per gli stessi
  Chiama CoinGlass /funding-rate/exchange-list per copertura Bitget

STEP 2 — Normalizza
  Tutti i funding in bps per periodo 8h (alcuni exchange espongono 4h o 1h)
  Costruisci dict: { "binance": +8.4, "bybit": +9.1, "okx": +7.9, "bitget": +29.5 }

STEP 3 — Detection
  spread = max - min
  median = statistics.median(values)
  predicted_delta = predicted - current (per ogni exchange)

STEP 4 — Pattern matching (vedi sezione precedente)

STEP 5 — Z-score calibration (vedi references/calibration-thresholds.md)
  spread_z = (spread - mean_30d) / std_30d
  Se spread_z > 1.5 -> signal forte, qualunque sia il valore assoluto

STEP 6 — Output
  Se signal attivo -> scrivi context.funding_signal + alert push
  Sempre -> aggiorna context.funding_costs per cost-awareness
```

---

## Output: scrittura context.json

### context.funding_costs (sempre aggiornato, anche senza alert)
```json
{
  "funding_costs": {
    "ts": "2026-05-01T12:00:00Z",
    "next_settlement_in_min": 47,
    "by_exchange": {
      "BTC": {
        "bitget": {"current_8h_bps": 12.3, "predicted_8h_bps": 8.1},
        "binance": {"current_8h_bps": 6.5, "predicted_8h_bps": 5.2},
        "bybit": {"current_8h_bps": 7.8, "predicted_8h_bps": 6.0},
        "okx": {"current_8h_bps": 5.9, "predicted_8h_bps": 4.7}
      }
    }
  }
}
```

### context.funding_signal (solo se signal attivo)
```json
{
  "funding_signal": {
    "ts": "2026-05-01T12:00:00Z",
    "ttl_hours": 4,
    "signal": "DIVERGENCE_STRESS",
    "asset": "BTC",
    "exchange_outlier": "bitget",
    "spread_bps": 23.4,
    "spread_z": 2.1,
    "median_bps": 8.3,
    "interpretation": "Bitget retail crowd over-long, +29.5 bps vs median +8.3.
                       Contrarian setup possibile su rejection 4h.",
    "modifier_for_other_skills": {
      "bitget_long_size_factor": 0.6,
      "bitget_short_setups_weight": 1.3,
      "global_regime_input": "neutral"
    }
  }
}
```

---

## Cost-awareness — il caso d'uso quotidiano

```
DOMANDA OPERATIVA:
  "Sto per aprire un long BTC su Bitget. Quanto mi costerà il funding?"

CALCOLO:
  bitget.current_8h_bps = 12.3 bps
  Posizione: $10k size, leva 5x -> notional $50k
  Costo per settlement: $50k * 12.3 / 10000 = $61.5 ogni 8h
  Costo giornaliero (3 settlement): $184.5/giorno

  Contesto storico: la funding mediana 30gg è 7 bps. 12.3 è al 75° percentile.
  Confrontabile con altri exchange: Binance +6.5 bps -> stesso trade costerebbe
  $32.5/8h (-50%).

DECISIONE:
  Se l'edge di trade è > $200/giorno: open su Bitget OK (l'esecuzione conta)
  Se l'edge è marginale (~$100/giorno): considera open su Binance e gestisci
  prezzo execution tramite WS Bitget per i livelli SL/TP (vedi engine/price_feeds.py)
```

---

## Cross-reference con altre skill

```
LETTA DA:
  scalp-execution         -> filtro 7 nuovo: "funding cost > $X/giorno -> -20% edge"
  price-alert-trigger     -> in checklist: "funding signal contrarian -> downgrade"
  gex-analysis            -> integra signal in PASSO 0 (lettura derivati)
  derivatives-dashboard   -> P2/P3 leggono funding signal per pesare L/S e liq
  macro-regime-monitor    -> usa REGIME_EXTREME come input voto regime

SCRIVE:
  context.funding_costs (sempre, refresh ogni 1h)
  context.funding_signal (solo se signal attivo, TTL 4h)
  retrospettive.md (solo signal STRUCTURAL e DIVERGENCE persistenti)
```

---

## Errori da evitare

```
Tradare l'arb funding nudo:
  20 bps di spread ANNUALIZZATO sembra molto, ma il costo di hedging
  cross-exchange (slippage, depth, withdrawal fee, basis risk) spesso
  > dell'edge. Il funding arb puro è un mestiere da firma, non da retail.

Confondere funding alto con bullish:
  Funding +25 bps = retail molto long, NON = trend rialzista.
  Spesso precede flush long. Lettura corretta: contrarian short su rejection.

Calcolare funding cost senza moltiplicare per leva:
  Il funding si paga sul NOTIONAL, non sul margin. Posizione $10k @ 5x =
  paga su $50k. Errore comune.

Ignorare il next_settlement:
  Aprire 3 minuti prima del cutoff = paghi 8h pieni. Strategie scalp veloci
  spesso meglio aprire dopo il cut e chiudere prima del prossimo.

Trattare predicted funding come certezza:
  Coinalyze usa modello statistico — l'errore tipico è ±3 bps. Predicted
  serve come bias, non come numero esatto.
```

---

## Threshold operativi (default — calibrabili)

```
DIVERGENCE_STRESS:
  spread_bps_min: 8.0   (calibrazione: 90° percentile rolling 30gg)
  spread_z_min: 1.5
  persist_cycles: 2

PREDICTED_SHIFT:
  delta_bps_min: 5.0
  consistency_check: tutti gli exchange con stessa direzione predicted

REGIME_EXTREME:
  median_high: +25 bps
  median_low: -10 bps
  cycles: 3 (24h)
  spread_max: 5.0 bps (convergenza)
```
