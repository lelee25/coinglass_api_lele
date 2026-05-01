---
name: calibration-thresholds
description: >
  Reference per il framework di calibrazione percentile-based dei threshold
  usati nelle skill principali. Sostituisce le soglie hardcoded (str>7, L/S>2.0,
  OI±2%/h, StochRSI 20/80) con percentili rolling adattivi su 30 sessioni.
  Reference, NON skill — caricato dalle skill principali quando devono
  decidere se un valore è "estremo" senza assumere che le soglie statiche
  valgano per l'asset/regime corrente.
---

# Calibration Thresholds — framework percentile

## Premessa: perché le soglie statiche sono fragili

Le skill principali usano soglie come `str > 7`, `L/S > 2.0`, `OI ±2%/h`,
`StochRSI 20/80`, `Bollinger < 0.5%`. Sono ragionevoli **medianamente**, ma:

```
SU BTC IN VOLA 30%:    StochRSI 20 = ipervenduto significativo
SU BTC IN VOLA 80%:    StochRSI 20 = visitato 5 volte al giorno, rumore

SU L/S BTC TIPICO:     2.0 = top 5% del rolling 30d
SU L/S XRP TIPICO:     2.0 = mediana — non significativo
SU L/S DURANTE FUNDING SQUEEZE: anche 0.7 può essere "estremo" l'altra direzione
```

Il framework percentile **adatta automaticamente** le soglie al comportamento
storico effettivo di ogni metrica per ogni asset.

---

## Il principio: percentile rolling > soglia hardcoded

```
SOGLIA HARDCODED:
  is_extreme = value > 2.0

SOGLIA PERCENTILE:
  is_extreme = value > np.percentile(history_30d, 95)

VANTAGGI:
  - Si adatta al regime di volatilità dell'asset
  - Funziona uguale su BTC, ETH, XRP, SOL
  - Si re-calibra automaticamente con nuovi dati
  - Resiste ai regime shift (es. funding rate medio cambia post-evento macro)
```

---

## Quali metriche calibrare

### Calibrazione standard (P95/P5 rolling 30gg)
```
L/S ratio                  -> extreme_high = P95, extreme_low = P5
OI delta % (1h, 4h, 24h)   -> extreme_up = P95, extreme_down = P5
Funding rate cross-exchange spread -> extreme = P90
HHI onchain pool           -> extreme = P90 per pool (TVL-aware)
StochRSI overbought/oversold -> P85 / P15 (più stretti, più reattivi)
Bollinger bandwidth        -> compression = P10 (decile inferiore)
Volume ratio (1h vs MA20)  -> spike = P90
ETF netflow daily          -> extreme = P95 / P5
```

### Calibrazione strutturale (P99/P1 rolling 90gg)
```
str confluence score       -> structural = P99 (top 1% storico)
GEX wall magnitude         -> major = P99 dei wall observed
Liquidations daily         -> outlier = P99
Macro indices (MVRV, Puell, Bubble) -> calibrati con z-score 90gg
```

### Calibrazione regime-adaptive
```
Per metriche sensitive al regime (volatility, trend), applicare scaling:

  vol_regime = "high" if realized_vol_30d > P75(realized_vol_180d) else "low"

  extreme_threshold(value, history, regime):
    base = np.percentile(history, 95)
    if regime == "high":   return base * 1.2   # serve più magnitudo
    elif regime == "low":  return base * 0.8   # basta meno per essere significativo
    return base
```

---

## Schema del file `calibration.json`

Il file viene generato dal Claude server (cron weekly Monday 03:00 UTC) e
letto dalle skill principali. Schema:

```json
{
  "calibration": {
    "computed_at": "2026-04-28T03:00:00Z",
    "lookback_days": 30,
    "asset_thresholds": {
      "BTC": {
        "ls_ratio": {
          "p5": 0.71,
          "p15": 0.84,
          "p50": 1.18,
          "p85": 1.62,
          "p95": 1.94
        },
        "oi_delta_1h_pct": {
          "p5": -1.8,
          "p95": +2.4
        },
        "funding_spread_bps_8h": {
          "p90": 9.1,
          "p95": 14.3
        },
        "stochrsi_30d": {
          "p15": 18.2,
          "p85": 81.7
        },
        "bollinger_bandwidth_15m_pct": {
          "p10": 0.42
        },
        "volume_ratio_1h": {
          "p90": 2.3
        }
      },
      "ETH": { ... },
      "SOL": { ... }
    },
    "structural_thresholds": {
      "BTC": {
        "str_confluence": {"p99": 9.4},
        "gex_wall_magnitude_usd": {"p99": 28.5e6},
        "liquidations_daily_usd": {"p99": 380e6}
      }
    },
    "vol_regime": {
      "BTC": "low",
      "ETH": "high"
    }
  }
}
```

---

## Integrazione nelle skill principali

### gex-analysis.md
```
PRIMA (hardcoded):
  if str > 9.0: structural
  elif str > 7.0: significant

DOPO (percentile):
  thresholds = calibration.structural_thresholds.BTC.str_confluence
  if str > thresholds.p99: structural
  elif str > calibration.asset_thresholds.BTC.str_confluence.p85: significant
```

### derivatives-dashboard.md
```
PRIMA:
  if ls_ratio > 2.0: CROWDING_LONG_EXTREME
  elif ls_ratio > 1.5: CROWDING_LONG_MODERATE

DOPO:
  ls = calibration.asset_thresholds.BTC.ls_ratio
  if ls_ratio > ls.p95: CROWDING_LONG_EXTREME
  elif ls_ratio > ls.p85: CROWDING_LONG_MODERATE
```

### scalp-execution.md
```
PRIMA:
  StochRSI > 75 (Setup 1, Bounce on resistance)

DOPO:
  stoch = calibration.asset_thresholds.BTC.stochrsi_30d
  StochRSI > stoch.p85 (auto-adatta a 76, 81, 79, ecc.)
```

### funding-arb-detector.md
```
PRIMA:
  spread_bps > 8 -> DIVERGENCE_STRESS

DOPO:
  spread_thr = calibration.asset_thresholds.BTC.funding_spread_bps_8h
  spread_bps > spread_thr.p90 -> DIVERGENCE_STRESS
  spread_bps > spread_thr.p95 -> CRITICAL DIVERGENCE
```

---

## Pattern di scrittura lato Claude server

```python
# Pseudo-code per il server
import numpy as np

def compute_thresholds(history: list[float], percentiles: list[int]) -> dict:
    """history: lista valori giornalieri/orari rolling 30d"""
    return {f"p{p}": float(np.percentile(history, p)) for p in percentiles}

def is_extreme(value, asset, metric, side="high", regime=None):
    """Check se value è extreme rispetto al percentile calibrato"""
    cal = load_calibration()
    thr = cal["asset_thresholds"][asset][metric]
    if side == "high":
        return value > thr.get("p95", float("inf"))
    elif side == "low":
        return value < thr.get("p5", float("-inf"))
```

---

## Quando NON usare percentile

```
DATI MACRO LONG-TERM:
  MVRV, Puell, Bubble Index hanno benchmark assoluti storici (decadi).
  Hardcoded thresholds (MVRV<1, Puell<0.5) sono OK e PIÙ INFORMATIVI.

EVENTI BINARI:
  Pi Cycle Indicator (top signal): è binario, non percentilabile.

SOGLIE FISICHE/STRUTTURALI:
  Distanza prezzo da livello (es. 0.5%, 1%): legata a slippage, fee, spread.
  Hardcoded = corretto.

DATI A BASSA FREQUENZA O CON OUTLIER PERSISTENTI:
  ETF flow daily: solo 30 osservazioni in 30gg, P95 instabile.
  Meglio z-score su lookback più lungo (90gg) e regole dual-threshold.
```

---

## Frequenza di refresh

```
WEEKLY (Monday 03:00 UTC):
  Tutte le calibrazioni rolling 30gg/90gg
  Vol regime classification per asset

DAILY (00:30 UTC):
  Vol regime check (può cambiare in giornata su evento estremo)

ON-DEMAND:
  Quando un'analisi richiede percentile su finestra custom
  (es. ETF flow streak su 14gg specifici)
```

---

## Errori da evitare

```
Calibrare su lookback troppo corto:
  Rolling 7gg ha 7 osservazioni daily o 168 hourly. Outlier dominano P95.
  Usare 30gg minimo per metriche orarie, 90gg per daily.

Sovrapporre percentile e z-score senza coerenza:
  Decidere PER METRICA quale framework usare. Non mischiare nello stesso
  blocco (un valore è P95 OPPURE z>1.65, non entrambi confusamente).

Usare percentile per signal binari:
  Pi Cycle, Death Cross sono binari. Percentile non si applica.

Refresh troppo frequente:
  Calibrazione che cambia ogni ora produce flapping di signal. Weekly è
  il giusto compromesso tra adattività e stabilità.

Non versionare calibration.json:
  Quando il regime di mercato cambia drasticamente (es. dopo evento Lehman-like),
  le calibrazioni precedenti diventano inaccurate. Salvare snapshot mensile
  per debug retrospettivo.
```

---

## Cross-reference

```
USATA DA:
  gex-analysis              -> str confluence, GEX wall magnitude
  derivatives-dashboard     -> L/S, OI delta, liquidation
  scalp-execution           -> StochRSI, Bollinger, volume ratio
  price-alert-trigger       -> str (delegato), volume threshold
  funding-arb-detector      -> funding spread, predicted shift
  whale-onchain-monitor     -> HHI per pool, netflow z-score
  etf-flow-interpreter      -> streak threshold (parzialmente)
  macro-regime-monitor      -> z-score on-chain indices

SCRITTA DA:
  cron weekly del Claude server (non da skill)
```
