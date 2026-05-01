---
name: spec-adaptive-weights
description: >
  SPEC tecnica di un MODULO PYTHON (non skill markdown) che il Claude server
  deve implementare per chiudere il loop di apprendimento dei setup scalp.
  Aggrega retrospettive 30gg, calcola edge per setup (1-6) e produce
  setup_weights.json letto da scalp-execution per pesare proporzionalmente
  le opportunità. Senza questo modulo, ogni setup ha sempre lo stesso peso
  teorico — niente apprendimento.
---

# SPEC — Adaptive Weights Module (Python, non skill)

## Cosa è e cosa NON è

```
È:    modulo Python che gira weekly (cron lunedì 03:30 UTC)
      legge retrospettive.md, scratchpad logs, trade execution log
      produce setup_weights.json
      
NON è: skill markdown che l'agent carica
       l'agent NON esegue questo logic — lo fa il server una volta a settimana
```

L'output `setup_weights.json` viene poi LETTO da `scalp-execution.md` come
modifier dell'edge dei 6 setup.

---

## Input richiesti

```
SOURCE 1 — retrospettive.md (parsed)
  Per ogni entry:
    - data, ora, asset
    - cascata_decision (SWING NO/YES, SCALP NO/YES, SETUP_TYPE, FINAL_DECISION)
    - counterfactual outcome (TP_HIT/SL_HIT/OPEN/MANCATA/CORRETTA)
    - osservazione

SOURCE 2 — trade_execution_log.json (mantenuto dall'agent operativo)
  [{
    "ts_open": "...",
    "ts_close": "...",
    "asset": "BTC",
    "side": "long",
    "setup_id": 2,        # 1-6 dei 6 setup di scalp-execution
    "entry_price": ...,
    "exit_price": ...,
    "stop_price": ...,
    "target_price": ...,
    "size_usd": ...,
    "outcome": "WIN|LOSS|BREAKEVEN",
    "pnl_pct": ...,
    "pnl_usd": ...,
    "duration_minutes": ...,
    "regime_at_entry": "RECOVERY"
  }, ...]

SOURCE 3 — context history (per regime context)
  context_history/[date].json -> snapshot regime giornaliero
```

---

## Algoritmo di calcolo

```python
# Pseudocode per il modulo
import json
from collections import defaultdict
from pathlib import Path
from datetime import datetime, timedelta

def compute_adaptive_weights(lookback_days=30, base_weight=1.0):
    """
    Calcola peso adattivo per ognuno dei 6 setup di scalp-execution.
    Bayesian-flavor con shrinkage verso base_weight per setup poco campionati.
    """
    cutoff = datetime.utcnow() - timedelta(days=lookback_days)
    trades = [t for t in load_trades() if parse_ts(t["ts_open"]) >= cutoff]
    
    weights = {}
    
    for setup_id in range(1, 7):
        setup_trades = [t for t in trades if t["setup_id"] == setup_id]
        n = len(setup_trades)
        
        if n == 0:
            weights[setup_id] = base_weight
            continue
        
        # Edge basico: hit rate * avg_win - (1-hit_rate) * avg_loss
        wins = [t for t in setup_trades if t["outcome"] == "WIN"]
        losses = [t for t in setup_trades if t["outcome"] == "LOSS"]
        hit_rate = len(wins) / n
        avg_win_pct = sum(t["pnl_pct"] for t in wins) / max(1, len(wins))
        avg_loss_pct = abs(sum(t["pnl_pct"] for t in losses)) / max(1, len(losses))
        
        edge = hit_rate * avg_win_pct - (1 - hit_rate) * avg_loss_pct
        
        # Shrinkage Bayesian (regularization): meno trades = più tirato verso base
        # k = 10 trade è la "scala" — sotto k il peso è ammorbidito
        k = 10
        shrunk_weight = (n / (n + k)) * (1 + edge / 2) + (k / (n + k)) * base_weight
        
        # Clip su [0.3, 2.0] per evitare degenerate
        weights[setup_id] = max(0.3, min(2.0, shrunk_weight))
    
    return {
        "computed_at": datetime.utcnow().isoformat() + "Z",
        "lookback_days": lookback_days,
        "base_weight": base_weight,
        "weights_by_setup": weights,
        "trade_count_by_setup": {sid: len([t for t in trades if t["setup_id"] == sid])
                                 for sid in range(1, 7)},
        "by_regime": compute_per_regime_weights(trades)
    }

def compute_per_regime_weights(trades):
    """Pesa anche separatamente per regime — alcuni setup brillano in regime specifici"""
    regimes = ["CAPITULATION", "RECOVERY", "NEUTRAL", "EUPHORIA", "RISK-OFF"]
    out = {}
    for regime in regimes:
        regime_trades = [t for t in trades if t.get("regime_at_entry") == regime]
        out[regime] = {}
        for setup_id in range(1, 7):
            st = [t for t in regime_trades if t["setup_id"] == setup_id]
            if len(st) >= 5:  # min sample for regime-specific
                hit = sum(1 for t in st if t["outcome"] == "WIN") / len(st)
                out[regime][setup_id] = round(hit, 3)
    return out
```

---

## Output: setup_weights.json

```json
{
  "computed_at": "2026-04-28T03:30:00Z",
  "lookback_days": 30,
  "base_weight": 1.0,
  "weights_by_setup": {
    "1": 1.15,
    "2": 1.42,
    "3": 0.85,
    "4": 0.95,
    "5": 0.65,
    "6": 1.10
  },
  "trade_count_by_setup": {
    "1": 14,
    "2": 9,
    "3": 18,
    "4": 7,
    "5": 9,
    "6": 12
  },
  "by_regime": {
    "RECOVERY": {"1": 0.71, "2": 0.78, "3": 0.55, "4": 0.62, "6": 0.65},
    "EUPHORIA": {"1": 0.45, "5": 0.30}
  },
  "narrative": "Setup 2 (bounce gamma+) outperforming +42% vs base — peso 1.42.
                Setup 5 (squeeze) sottoperformante in tutti i regime — peso 0.65.
                Setup 6 (divergenza) particolarmente forte in RECOVERY (65%)."
}
```

---

## Come scalp-execution.md leggerà questo file

```
PRIMA (no learning):
  edge_setup_2 = base_edge_2  # sempre uguale

DOPO (con adaptive weights):
  weights = json.load("setup_weights.json")
  edge_setup_2 = base_edge_2 * weights["weights_by_setup"]["2"]
  
  # Optional: regime-aware weight
  current_regime = context.macro_regime.primary
  if current_regime in weights["by_regime"]:
    regime_hit = weights["by_regime"][current_regime].get("2")
    if regime_hit:
      edge_setup_2 *= (1 + (regime_hit - 0.5) * 0.5)  # boost per regime hit
```

---

## Frequenza & operative

```
CRON:                   weekly Monday 03:30 UTC
LOOKBACK:               30 days rolling
MIN TRADES PER SETUP:   5 per regime-specific weight, 0 per global
SHRINKAGE k:            10 (calibrabile)
WEIGHT CLIP:            [0.3, 2.0]

OUTPUT FILE:            calibration/setup_weights.json
                        (separato da calibration.json per chiarezza)

INTEGRAZIONE:
  scalp-execution.md     legge weights["weights_by_setup"]
  proactive-scout.md     usa per pesare setups nello score
```

---

## Errori da evitare nel modulo

```
Sample size troppo piccolo:
  Setup con n=2 trade non danno informazione statistica. Lo shrinkage
  Bayesian protegge contro questo, ma anche logging trade_count per
  l'utente per chiarezza.

Reweighting troppo aggressivo:
  Clip [0.3, 2.0] è il default. Tightening (es. [0.5, 1.5]) protegge
  contro reazione eccessiva a streak short.

Confondere edge totale con hit rate:
  Setup con hit rate 40% ma R/R 3:1 ha EDGE POSITIVO. Setup hit rate 70%
  ma R/R 1:2 ha edge NEGATIVO. Sempre considerare R/R.

Non separare per asset:
  Setup 2 può funzionare su BTC e fallire su altcoin volatili. Versione
  v2 di questo modulo dovrebbe includere weights per asset class.

Calcolare adaptive weights senza include regime:
  Stesso setup ha hit rate diversa per regime. Always compute by_regime
  table anche se l'integrazione iniziale usa solo flat weight.
```

---

## Riferimento implementativo

Il Claude server deve implementare questo modulo come:

```
~/gex-agentkit/calibration/adaptive_weights.py
~/gex-agentkit/calibration/setup_weights.json   (output)
~/gex-agentkit/cron/weekly_calibration.sh        (orchestrator)
```

Le skill markdown in `skills/` non hanno awareness della logica di calcolo —
leggono solo il JSON output via tool precostruito (es. `read_setup_weights()`).
