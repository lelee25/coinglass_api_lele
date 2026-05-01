---
name: etf-flow-interpreter
description: >
  Interpreta i flussi ETF spot crypto USA (BTC, ETH, SOL) + Hong Kong tramite
  i 16 endpoint /api/etf/* di CoinGlass (verificati Hobbyist AVAILABLE).
  Capitale ETF è istituzionale e regolamentato → leading 6-24h sul prezzo BTC,
  più affidabile dei segnali derivati per trend strutturale settimanale.
  Trigger: "ETF flow", "ETF inflow", "ETF outflow", "spot BTC ETF", "IBIT",
  "FBTC", "BlackRock ETF", "Fidelity ETF", "ETH ETF", "SOL ETF",
  "Hong Kong ETF", "premium NAV", "discount ETF", "AUM ETF", "issuer breakdown",
  "rotation BTC ETH ETF", "streak inflow", "streak outflow", "BTC ETF streak".
  Output: signal score + narrative settimanale + modifier per gex/macro.
  NON è un trade trigger intraday — è un trend filter strategico.
---

# ETF Flow Interpreter — capitale istituzionale leading

## Filosofia: gli ETF spot crypto sono il segnale più "lento" e più "vero"

Chi compra IBIT/FBTC/BITB non è un retail. È:
- Wealth manager con mandati istituzionali
- Hedge fund con strategie sistematiche
- Treasury aziendali (Tesla, Strategy = ex MicroStrategy, etc.)
- Pension fund che ora possono allocare crypto via wrapper regolato

Questo capitale è:
```
LENTO: decisioni T+1, settlement T+2, no scalp
GRANDE: ticket size $10M+ tipico, $100M+ frequente
INFORMATO: research-driven, accesso macro privilegiato
PERSISTENTE: streak in/out durano settimane, non giorni
```

L'edge di osservare ETF flow non è "intraday alpha". È **trend filter
settimanale**: se i flussi BTC ETF sono outflow per 5 giorni consecutivi,
qualunque scalp long deve avere stop più stretti e size ridotta.

---

## Data sources (16 endpoint AVAILABLE Hobbyist — verificati §22)

```
BTC ETF USA (10 issuer principali — IBIT, FBTC, BITB, ARKB, GBTC...):
  /api/etf/bitcoin/list                       -> issuer breakdown attuale
  /api/etf/bitcoin/flow-history               -> netflow daily (USD)
  /api/etf/bitcoin/aum                        -> AUM totale + per issuer
  /api/etf/bitcoin/net-assets/history         -> evoluzione AUM
  /api/etf/bitcoin/premium-discount-history   -> NAV vs spot price
  /api/etf/bitcoin/price/history              -> ETF share price
  /api/etf/bitcoin/history                    -> volume, AUM, holdings BTC

ETH ETF USA (8 issuer — ETHA, FETH, ETHE...):
  /api/etf/ethereum/list
  /api/etf/ethereum/flow-history
  /api/etf/ethereum/net-assets-history

SOL ETF (early stage, dati parziali):
  /api/etf/solana/list
  /api/etf/solana/flow-history

HONG KONG ETF (Asia session signal — diverge spesso da USA):
  /api/hk-etf/bitcoin/flow-history
  /api/hk-etf/ethereum/flow-history

GRAYSCALE PREMIUM (storica — GBTC discount/premium):
  /api/grayscale-premium/list

REFRESH POLICY:
  Daily refresh dopo close US market (21:00 UTC)
  Hong Kong refresh dopo close HKEX (08:00 UTC)
  Premium/discount intraday se posizioni attive
```

---

## I 5 segnali leggibili

### Segnale 1 — INFLOW STREAK (institutional bid solido)
```
CONDIZIONI:
  Net inflow > 0 per ≥ 5 sessioni consecutive (BTC) o ≥ 3 (ETH)
  Magnitudine cumulativa > +$2B (BTC) o +$500M (ETH) sulla streak
  Aggregato senza GBTC (GBTC è in declino strutturale, distorce il segnale)

INTERPRETAZIONE:
  Capitale istituzionale in modalità accumulazione.
  -> Bias bullish strategico settimanale
  -> Modifier per gex-analysis: long_setups_weight +20%
  -> Pullback tecnici diventano buy opportunity, non distribution

ALERT LEVEL: STRUCTURAL (entra in macro-regime come input)
NOTA: streak inflow > 10 sessioni storicamente preludio rally 8-15%
```

### Segnale 2 — OUTFLOW STREAK (institutional risk-off)
```
CONDIZIONI:
  Net outflow per ≥ 3 sessioni consecutive (BTC) o ≥ 2 (ETH)
  Magnitudine cumulativa < -$1B (BTC) o -$300M (ETH)
  Coerente con DXY rising e/o S&P risk-off

INTERPRETAZIONE:
  Distribution istituzionale o de-risking macro.
  -> Bias bearish strategico
  -> Modifier per gex-analysis: short_setups_weight +20%, long_size -30%

ALERT LEVEL: HIGH
COMBINAZIONE: outflow ETF + macro RISK-OFF + funding extreme = risk regime entrato
```

### Segnale 3 — PREMIUM ANOMALY
```
CONDIZIONI:
  Premium ETF vs NAV > +0.5% (raro su ETF spot, indica forte bid primario)
  Oppure Discount > -0.3% (indica selling pressure)

INTERPRETAZIONE:
  Premium positivo = autorized participants stanno creando shares aggressivamente
  -> domanda eccede supply -> bid pressure prossime sessioni
  Discount = redemption > creation -> selling pressure

ALERT LEVEL: MEDIUM
NOTA: ETF spot tipicamente trade entro ±0.05% NAV. Anomalia oltre 0.3%
      è raro e predittivo a 1-3 giorni.
```

### Segnale 4 — ROTATION BTC <-> ETH (preludio altseason o reverse)
```
CONDIZIONI:
  ETH ETF inflow > BTC ETF inflow per ≥ 3 sessioni
  In valore assoluto OR come % AUM rispettivo
  Conferma con ratio ETH/BTC price che inverte trend

INTERPRETAZIONE:
  Capitale ruota da BTC a ETH (o inverso)
  -> Bias direzionale ETH outperformance 1-4 settimane
  -> Per scalp: setup ETH long preferiti, short ETH ridotti

ALERT LEVEL: HIGH (direzionale + duraturo)
HISTORICAL: rotation BTC->ETH precedette di 1-3 settimane le 3 altseason
            principali del 2024-2025
```

### Segnale 5 — HK vs USA DIVERGENCE
```
CONDIZIONI:
  Hong Kong ETF flow opposto a USA per ≥ 2 sessioni
  Magnitudine HK > +/-$50M (significativa per dimensione mercato)

INTERPRETAZIONE:
  Asia diverge da USA nel posizionamento.
  HK inflow + USA outflow = capitale asiatico bullish, USA bearish
  -> spesso preludio a inversione (chi si muove primo viene confermato dopo)

ALERT LEVEL: MEDIUM
LIMITAZIONE: HK ETF mercato relativamente piccolo. Significativo se persistente.
```

---

## Algoritmo di interpretazione

```
STEP 1 — Aggregation daily (cron 22:00 UTC dopo close US)
  Fetch /api/etf/bitcoin/flow-history?range=14d
  Fetch /api/etf/ethereum/flow-history?range=14d
  Fetch /api/etf/solana/flow-history?range=14d
  Fetch /api/hk-etf/bitcoin/flow-history?range=14d

STEP 2 — Normalize (escludi GBTC dal BTC aggregato)
  net_btc[day] = sum(issuer_flow[day] for issuer in btc_issuers if issuer != 'GBTC')

STEP 3 — Streak detection
  streak_in[asset] = count consecutive days with net > 0 ending today
  streak_out[asset] = count consecutive days with net < 0 ending today

STEP 4 — Cumulative & threshold
  cum_7d[asset] = sum(net_flow[asset] for last 7d)
  cum_30d[asset] = sum(net_flow[asset] for last 30d)

STEP 5 — Premium check
  premium_pct = (etf_price - nav) / nav * 100
  Significant if abs(premium_pct) > 0.3

STEP 6 — Pattern matching (vedi sezione precedente)

STEP 7 — Output narrative + signal modifiers
```

---

## Output: scrittura context.json + report

### context.etf_signal (refresh daily)
```json
{
  "etf_signal": {
    "ts": "2026-05-01T22:00:00Z",
    "ttl_hours": 24,
    "btc": {
      "streak_in_days": 5,
      "streak_out_days": 0,
      "cum_7d_usd": 2.4e9,
      "cum_30d_usd": 5.8e9,
      "premium_pct_avg": 0.12,
      "top_issuer": "IBIT",
      "top_issuer_share_pct": 56.3
    },
    "eth": {
      "streak_in_days": 3,
      "streak_out_days": 0,
      "cum_7d_usd": 0.6e9,
      "cum_30d_usd": 1.4e9,
      "premium_pct_avg": 0.08
    },
    "rotation": {
      "active": false,
      "direction": null
    },
    "hk_divergence": false,
    "active_signals": ["INFLOW_STREAK_BTC", "INFLOW_STREAK_ETH"],
    "narrative": "BTC inflow streak 5gg ($2.4B 7d) trainata da IBIT 56% share.
                  ETH conferma con streak 3gg. Rotation non attiva.
                  Bias bullish strategico settimanale. Pullback = buy.",
    "modifier_for_other_skills": {
      "long_setups_weight": 1.2,
      "short_setups_weight": 0.85,
      "swing_long_size_factor": 1.1,
      "macro_input": "INSTITUTIONAL_BULLISH"
    }
  }
}
```

### Report user-facing weekly (lunedì mattina)
```
=== ETF FLOW WEEKLY — settimana [date - date] ===

BTC ETF SPOT (USA):
  Net flow 7d:     [+/-$X.XB]
  Streak attiva:   [N giorni in/out]
  Top issuer flow: [IBIT $X.XB | FBTC $X.XB | BITB $X.XB]
  AUM totale:      [$X.XB] ([+/-X.X% wow])
  Premium medio:   [+/-X.XX%]

ETH ETF SPOT (USA):
  Net flow 7d:     [+/-$X.XB]
  Streak attiva:   [N giorni in/out]
  Top issuer flow: [ETHA $X.XB | FETH $X.XB]
  AUM totale:      [$X.XB]

SOL ETF (early stage):
  Net flow 7d:     [+/-$X.XM]
  AUM totale:      [$X.XM]

HONG KONG (Asia signal):
  BTC net 7d:      [+/-$XM]
  ETH net 7d:      [+/-$XM]
  Divergenza vs USA: [SI/NO]

ROTATION SIGNALS:
  BTC <-> ETH:     [direzione e magnitudo]
  Crypto <-> stablecoin (via on-chain — vedi whale-onchain-monitor)

NARRATIVE SETTIMANALE:
  [3-5 righe: cosa sta facendo il capitale istituzionale,
   cosa cambia rispetto alla settimana precedente]

MODIFIER PER LA SETTIMANA:
  Bias strategico: [BULLISH / BEARISH / NEUTRAL]
  Long setups:     moltiplicatore [X.X]
  Short setups:    moltiplicatore [X.X]
  Trade horizon preferito: [scalp / swing / hold]
```

---

## Cross-reference con altre skill

```
LETTA DA:
  macro-regime-monitor    -> input institutional flow per voto regime
  gex-analysis            -> usa long/short_weight come modifier
  scalp-execution         -> filtro qualità setups in/out di trend strategico
  whale-onchain-monitor   -> conferma o nega rotation segnalata onchain

SCRIVE:
  context.etf_signal (autoritativo, refresh daily 22:00 UTC)
  retrospettive.md (entry settimanale + transizioni significative)

NON LETTA DA:
  price-alert-trigger     -> troppo lento per real-time alert
                             (ma l'agent vede bias indirettamente via context.macro_regime)
```

---

## Errori da evitare

```
Tradare ETF flow intraday:
  Lo statement giornaliero arriva alle 21:00 UTC dopo close. Tutto quello
  che succede prima è proiezione/leak. L'edge è settimanale, non intraday.

Includere GBTC nel BTC aggregato:
  GBTC è in trend di declino strutturale (post-conversione 2024). Outflow
  GBTC NON è negativo per il mercato — è sostituzione con altri ETF.
  Sempre escluderlo o riportarlo separato.

Confondere AUM con flow:
  AUM cresce se prezzo BTC sale anche senza inflow. Flow = creation/redemption
  di shares (positions reali). Sempre guardare flow, non AUM ratio.

Trattare la rotation come "altseason":
  ETH rotation può preludere a outperformance ETH ma NON è altseason.
  Altseason richiede BTC dominance falling + altcoin > ETH outperformance.

Tradare il premium intraday:
  Premium > 0.3% è un signal predittivo a 1-3 giorni, non scalp setup.
  L'arbitraggio del premium è di market maker autorizzati, non retail.
```

---

## Threshold operativi (default — calibrabili)

```
INFLOW STREAK BTC:    consecutive days >= 5, cum_7d > +$2B
OUTFLOW STREAK BTC:   consecutive days >= 3, cum_7d < -$1B
INFLOW STREAK ETH:    consecutive days >= 3, cum_7d > +$500M
OUTFLOW STREAK ETH:   consecutive days >= 2, cum_7d < -$300M

PREMIUM ANOMALY:      abs(premium_pct) > 0.3% (calibrazione: 95° percentile rolling 30gg)
ROTATION BTC->ETH:    eth_flow_pct_aum > btc_flow_pct_aum per ≥ 3 sessioni
HK DIVERGENCE:        opposite sign per ≥ 2 sessioni AND abs(hk) > $50M
```
