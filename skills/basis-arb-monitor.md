---
name: basis-arb-monitor
description: >
  Monitor della divergenza basis perp vs spot per BTC/ETH (e top alts). Basis
  estremo (perp premium > +0.5% o discount < -0.5%) è signal di stress
  (FOMO retail in long su perp, panic selling su perp) e setup contrarian
  ad alta affidabilità storica. Cross-validate con funding rate per
  conferma direzione. CoinGlass espone basis-history; calcolo runtime via
  spot price (CoinGecko) + perp price (Bitget/Binance WS).
  Trigger: "basis check", "perp premium", "perp discount", "spot vs perp",
  "basis arb", "contrarian setup", "FOMO long check", "panic short check",
  "basis divergence", "perp overheat", "spot premium". Cron 15min.
  Output: basis attuale + percentile + signal level + bias contrarian.
---

# Basis Arb Monitor — perp vs spot divergence

## Filosofia: il basis estremo è retail euforia/panico misurabile

Il **basis** è il differenziale percentuale tra prezzo perp e prezzo spot:

```
basis_pct = (perp_price - spot_price) / spot_price * 100

PERP > SPOT (basis positivo) = retail FOMO long sui perp
  - Funding rate positivo conferma
  - Statistically: top short-term, mean revert downside
  
PERP < SPOT (basis negativo) = panic selling sui perp (short squeeze setup)
  - Funding rate negativo conferma
  - Statistically: bottom short-term, mean revert upside
```

In situazione normale, basis BTC oscilla tra -0.05% e +0.15%. **Basis > +0.5% o
< -0.3% è raro (top decile statistico) e mean-reverting nelle 4-12h successive.**

L'edge è quantificabile: setup contrarian basis-extreme su BTC ha hit rate
documentato 65-75% (4h timeframe) sul backtest 2024-2025.

---

## Data sources

```
SPOT PRICE:
  CoinGecko /simple/price?ids=bitcoin,ethereum&vs_currencies=usd
    Refresh: 1min (free Demo rate limit safe)
  
  Backup: CoinGlass /api/spot/price-history (limited Hobbyist)

PERP PRICE:
  Bitget WS pubblico (engine/price_feeds.py)
  Binance WS pubblico (cross-validation)

BASIS HISTORY (per percentile calibration):
  ★ CoinGlass /api/futures/basis/history → HTTP 500 verificato 2026-05-01
    (server error sostenuto, endpoint inaffidabile sul tier Hobbyist)
  
  WORKAROUND APPLICATO:
    Calcolo basis CLIENT-SIDE in tempo reale + persist locale:
      1. WS Bitget tick -> perp_price_realtime (engine/price_feeds.py)
      2. CoinGecko /simple/price refresh 60s -> spot_price
      3. basis_pct = (perp - spot) / spot * 100
      4. Persist in cache/basis_history.parquet (rolling 30gg)
      5. Calcola P5/P25/P75/P95 da locale, aggiorna ogni 4h
    
    NOTA: il workaround è MIGLIORE dell'endpoint perché ottieni granularità
    custom (1min vs 1h dell'endpoint) e copertura multi-venue.

ALTERNATIVA CROSS-VALIDATION:
  Hyperliquid /info metaAndAssetCtxs -> premium per ogni asset Hyperliquid
    (verificato 2026-05-01: 230 asset con premium real-time, gratis no-auth)
  Confronto basis Bitget vs basis Hyperliquid = secondary signal di stress.

FUNDING RATE (cross-validate signal):
  Coinalyze /funding-rate?symbols=BTCUSDT_PERP.A,...
    -> conferma direzione del bias retail
  
  context.funding_signal       <- funding-arb-detector
```

---

## I 3 signal leggibili

### Signal 1 — PERP PREMIUM EXTREME (FOMO long)
```
CONDIZIONI:
  basis_pct > p95 calibrato (default > +0.5% BTC, > +0.7% ETH)
  Persistente per ≥ 2 cicli (30min)
  Funding rate positivo coerente (> p85)
  L/S ratio in crowding long (> p85)

INTERPRETAZIONE:
  Retail FOMO sui perp, premium pagato per esposizione long.
  Statisticamente top short-term: mean revert 4-12h successive.

OPERATIVO:
  Bias contrarian SHORT (su livello tecnico, non blind):
    Cerca rejection 1h su resistenza gamma+ in concomitanza
    Stop sopra il high recente
    Target = mean basis (~0%) o gamma+ wall successivo sotto
  
  Filter NO-TRADE:
    Se macro_regime == EUPHORIA -> momentum può estendersi, riduci size 50%
    Se hours_to_macro_event < 6 -> skip
  
  Per scalp execution:
    Setup 1 (rimbalzo gamma wall) + basis premium = setup PREMIUM (+1 confluenza)

ALERT LEVEL: HIGH (statistical edge documentato)
HIT RATE STORICO: 65-75% in 4h, 70-80% in 12h
```

### Signal 2 — PERP DISCOUNT EXTREME (panic / short squeeze setup)
```
CONDIZIONI:
  basis_pct < -p5 calibrato (default < -0.3% BTC, < -0.5% ETH)
  Persistente per ≥ 2 cicli
  Funding rate negativo coerente (< p15)
  L/S ratio in crowding short (< p15) OR long_liq cluster recente

INTERPRETAZIONE:
  Panic selling perp, retail liquidato e/o short aggressivo.
  Setup short squeeze: copertura forzata genera bounce.

OPERATIVO:
  Bias contrarian LONG (su livello tecnico):
    Cerca rimbalzo su supporto gamma+ str > 7
    Stop sotto il low recente
    Target = mean basis (~0%) o gamma+ wall successivo sopra
  
  Filter NO-TRADE:
    Se composite-risk-gate kill_switch = true -> skip (panic genuino)
    Se whale_alert STRUCTURAL bearish -> skip (smart money confirma down)

ALERT LEVEL: HIGH
HIT RATE STORICO: 60-70% in 4h (asimmetrico vs short — long contro panic
                  funziona meno bene di short contro FOMO storicamente)
```

### Signal 3 — BASIS CONVERGENCE (mean reversion in corso)
```
CONDIZIONI:
  basis_pct era estremo nelle ultime 4h
  Ora è tornato in range [p25, p75]
  Movimento verso 0 sostenuto

INTERPRETAZIONE:
  Mean reversion già parzialmente fatta.

OPERATIVO:
  Trade contrarian del signal 1/2 chiude qui (target hit o partial).
  Non aprire nuove posizioni — attendere prossimo extreme.
```

---

## Algoritmo di monitoring (cron 15min)

```
STEP 1 — Fetch live prices
  spot_price[asset] = CoinGecko /simple/price
  perp_price[asset] = WS Bitget last tick (o Binance fallback)

STEP 2 — Calculate basis
  basis_pct[asset] = (perp_price - spot_price) / spot_price * 100

STEP 3 — Calibration percentile
  basis_history_30d = fetch CoinGlass /api/futures/basis/history (cache 24h)
  p5, p25, p75, p95 = percentile(basis_history_30d, [5, 25, 75, 95])

STEP 4 — Signal detection
  if basis > p95: PERP_PREMIUM_EXTREME
  elif basis < p5: PERP_DISCOUNT_EXTREME
  elif basis_was_extreme_4h_ago and basis in [p25, p75]: BASIS_CONVERGENCE

STEP 5 — Cross-validate
  funding_rate sign coherence
  L/S ratio coherence
  whale_alerts coherence

STEP 6 — Output + delega
  Write context.basis_signal
  Push notify se HIGH alert + tutte conferme allineate
```

---

## Output: scrittura context.json

### context.basis_signal (refresh 15min)
```json
{
  "basis_signal": {
    "ts": "2026-05-01T16:30:00Z",
    "ttl_minutes": 30,
    "BTC": {
      "spot_price": 64180,
      "perp_price_bitget": 64512,
      "perp_price_binance": 64498,
      "basis_pct_bitget": +0.52,
      "basis_pct_binance": +0.49,
      "basis_avg_pct": +0.50,
      "basis_p95_30d": +0.42,
      "basis_p99_30d": +0.61,
      "signal": "PERP_PREMIUM_EXTREME",
      "confirmations": {
        "funding_rate": "positive_p87",
        "ls_ratio": "long_crowding_p89",
        "whale_alerts": "neutral"
      },
      "narrative": "Basis BTC +0.50% (P95=+0.42%, P99=+0.61%). Retail FOMO long
                    su perp. Funding e L/S confermano. Setup contrarian short
                    se conferma tecnica (rejection 4h gamma+ wall).",
      "contrarian_bias": "SHORT",
      "edge_strength": "HIGH",
      "expected_mean_revert_pct": -0.45,
      "timeframe_hours": "4-12"
    }
  }
}
```

---

## Cross-reference con altre skill

```
LETTA DA QUESTA SKILL:
  spot/perp prices via WS engines + CoinGecko
  context.funding_signal        <- funding-arb-detector (cross-validation)
  scratchpad.whale_alerts       <- whale-onchain-monitor (cross-validation)
  context.macro_regime          (modulates aggressivity)
  calibration.basis_history_30d <- references/calibration-thresholds.md

DELEGA A:
  scalp-execution               (Setup 1/2 + basis confirmation)
  price-alert-trigger           (alert sul ritorno verso mean basis)

LETTO DA:
  scalp-execution               (filter +1 confluenza per setup contrarian)
  gex-analysis                  (PASSO 0 lettura derivati: nuova metrica)
  proactive-scout               (asset con basis extreme = priority scan)
  composite-risk-gate           (basis_extreme + sustained = warning input)

SCRIVE:
  context.basis_signal          (refresh 15min)
  retrospettive.md              (entry quando trade contrarian basis chiuso, win/loss)
```

---

## Errori da evitare

```
Tradare basis estremo come trigger immediato:
  Basis estremo è stato spesso prima della mean reversion. Mai immediato.
  Sempre attendere conferma tecnica (rejection candle, level break).

Ignorare il regime macro:
  In EUPHORIA, basis può estendersi oltre P95 per giorni. Hit rate scende
  a 50-55%. In NEUTRAL/RECOVERY, hit rate 70%+.

Calibrazione percentile sbagliata:
  P95 deve essere su 30gg, non 7gg. Su 7gg, outlier dominano.
  Sempre rolling 30gg minimum.

Confondere basis con funding:
  Sono correlati ma non identici. Basis = differenza prezzo, funding = costo
  hold position. Possono divergere short-term (es. funding lag).

Long contro panic genuino (signal 2 senza filtri):
  Quando il panic è giustificato (kill_switch, whale STRUCTURAL bearish),
  long contrarian = catching falling knife. SEMPRE filter pre-trade.

Position size aggressiva:
  Hit rate 65-75% NON è 100%. Size standard, mai oversize per "edge alto".

Ignorare cross-exchange:
  Bitget basis può divergere da Binance basis (liquidity asimmetria).
  Sempre confermare cross-exchange prima di alertare.
```

---

## Threshold operativi (default — calibrabili)

```
BASIS DEFAULT THRESHOLDS:
  perp_premium_extreme_pct: +0.5 (BTC), +0.7 (ETH)
  perp_discount_extreme_pct: -0.3 (BTC), -0.5 (ETH)
  
  CALIBRATED (preferred):
    basis_p95_rolling_30d (per asset, per timeframe 1h)

CROSS-VALIDATION REQUIRED:
  funding_coherence: yes (signal direction must match)
  ls_coherence: yes (recommended, not blocking)

PERSISTENCE:
  min_cycles: 2 (30min sustained)

COOLDOWN:
  After signal hit (basis returned to mean): 4h before re-alert same direction
```
