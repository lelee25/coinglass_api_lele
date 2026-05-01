---
name: spec-calibration-monitor
description: >
  SPEC tecnica di un MODULO PYTHON (non skill markdown) che il Claude server
  deve implementare per il controllo qualità delle confidence dichiarate
  dall'agent. Calcola Brier score + calibration curve sui claim "confidence X%"
  vs outcome reale. Se l'agent è overconfident, applica correzione automatica
  letta dalle skill principali.
---

# SPEC — Calibration Monitor Module (Python, non skill)

## Cosa è e cosa NON è

```
È:    modulo Python che gira monthly (cron 1° del mese 03:30 UTC)
      legge confidence_log.json dell'agent
      calcola Brier score + calibration curve
      produce confidence_correction.json (offset multiplier)

NON è: skill markdown caricabile
       l'agent NON esegue la logica — la legge come correzione
```

L'output `confidence_correction.json` viene letto da gex-analysis,
scalp-execution, derivatives-dashboard quando dichiarano confidence.

---

## Premessa: cos'è la calibration di una confidence

```
Un agent ben calibrato dice "70% confidence" quando il 70% delle volte
quel claim si avvera. Un agent overconfident dice "70%" ma si avvera
solo il 50% delle volte → calibration off di -20pp.

Brier score = mean((forecast - actual)^2)
  Range: 0 (perfetto) a 1 (peggio possibile)
  Brier 0.10 = ben calibrato
  Brier > 0.20 = problemi seri di calibration

Calibration curve (reliability diagram):
  X = confidence dichiarata (0.0-1.0 in 10 bin)
  Y = hit rate effettivo per quel bin
  Diagonale = perfectly calibrated
  Sopra diagonale = under-confident
  Sotto diagonale = over-confident (più comune negli LLM)
```

---

## Input richiesti

```
SOURCE — confidence_log.json (logging continuo dell'agent)
  Ogni claim di confidence va loggata:
  
  [{
    "ts": "2026-04-28T14:00:00Z",
    "claim_id": "uuid",
    "skill": "gex-analysis",
    "asset": "BTC",
    "claim_type": "scenario_principale",
    "confidence_pct": 75,          # 0-100
    "scenario": "long bounce a $63k str>8 con target $65.5k",
    "key_levels": {"entry": 63000, "stop": 62370, "target": 65500},
    "ttl_hours": 24,
    "outcome": null,                # populated later
    "outcome_ts": null,
    "actual_outcome": null          # "TP_HIT", "SL_HIT", "EXPIRED", "INVALIDATED"
  }, ...]

L'agent deve loggare confidence ogni volta che dice "X% probabilità",
"alta confidence", etc. Il modulo poi va a verificare l'esito.
```

---

## Algoritmo

```python
import json
import numpy as np
from datetime import datetime, timedelta

def update_outcomes(log_path):
    """Aggiorna outcome dei claim in scadenza usando il prezzo storico"""
    log = json.load(open(log_path))
    for claim in log:
        if claim["outcome"] is not None:
            continue
        # check if TTL expired
        ts = datetime.fromisoformat(claim["ts"].replace("Z", "+00:00"))
        ttl_end = ts + timedelta(hours=claim["ttl_hours"])
        if datetime.utcnow() < ttl_end:
            continue
        # determine outcome by checking price history in [ts, ttl_end]
        prices = fetch_price_window(claim["asset"], ts, ttl_end)
        target = claim["key_levels"]["target"]
        stop = claim["key_levels"]["stop"]
        # for long claims:
        if min(prices) <= stop:
            claim["actual_outcome"] = "SL_HIT"
            claim["outcome"] = 0
        elif max(prices) >= target:
            claim["actual_outcome"] = "TP_HIT"
            claim["outcome"] = 1
        else:
            claim["actual_outcome"] = "EXPIRED"
            claim["outcome"] = 0  # expired = non realizzato
    save(log_path, log)
    return log

def compute_brier_and_calibration(log, lookback_days=90):
    """Compute Brier score + calibration curve"""
    cutoff = datetime.utcnow() - timedelta(days=lookback_days)
    claims = [c for c in log
              if c["outcome"] is not None
              and datetime.fromisoformat(c["ts"].replace("Z","+00:00")) >= cutoff]
    
    if len(claims) < 30:
        return None  # insufficient data
    
    forecasts = np.array([c["confidence_pct"] / 100 for c in claims])
    outcomes = np.array([c["outcome"] for c in claims])
    
    brier = np.mean((forecasts - outcomes) ** 2)
    
    # Calibration curve: 10 bin
    bins = np.linspace(0, 1, 11)
    bin_indices = np.digitize(forecasts, bins) - 1
    calibration = []
    for b in range(10):
        mask = bin_indices == b
        if mask.sum() < 3:
            continue
        avg_forecast = forecasts[mask].mean()
        hit_rate = outcomes[mask].mean()
        calibration.append({
            "bin": [bins[b], bins[b+1]],
            "n": int(mask.sum()),
            "avg_forecast": float(avg_forecast),
            "actual_hit_rate": float(hit_rate),
            "delta_pp": float((hit_rate - avg_forecast) * 100)
        })
    
    return {"brier": float(brier), "calibration_curve": calibration}

def derive_correction(calibration_curve):
    """Estimate global multiplier o offset per correggere"""
    # Simple linear regression: actual = a + b * forecast
    fcs = np.array([c["avg_forecast"] for c in calibration_curve])
    acs = np.array([c["actual_hit_rate"] for c in calibration_curve])
    if len(fcs) < 4:
        return {"multiplier": 1.0, "offset": 0.0, "method": "insufficient"}
    a, b = np.polyfit(fcs, acs, 1)  # acs = a + b*fcs
    # corrected_confidence(claim) = a + b * claim_confidence
    return {
        "multiplier": float(b),
        "offset": float(a),
        "method": "linear_regression",
        "note": "corrected_confidence = offset + multiplier * declared_confidence"
    }
```

---

## Output: confidence_correction.json

```json
{
  "computed_at": "2026-05-01T03:30:00Z",
  "lookback_days": 90,
  "n_claims_evaluated": 142,
  "brier_score": 0.187,
  "interpretation": "leggermente overconfident",
  "calibration_curve": [
    {"bin": [0.5, 0.6], "n": 18, "avg_forecast": 0.55, "actual_hit_rate": 0.50, "delta_pp": -5.0},
    {"bin": [0.6, 0.7], "n": 32, "avg_forecast": 0.65, "actual_hit_rate": 0.59, "delta_pp": -6.0},
    {"bin": [0.7, 0.8], "n": 47, "avg_forecast": 0.74, "actual_hit_rate": 0.62, "delta_pp": -12.0},
    {"bin": [0.8, 0.9], "n": 28, "avg_forecast": 0.84, "actual_hit_rate": 0.68, "delta_pp": -16.0},
    {"bin": [0.9, 1.0], "n": 17, "avg_forecast": 0.93, "actual_hit_rate": 0.71, "delta_pp": -22.0}
  ],
  "correction": {
    "multiplier": 0.78,
    "offset": 0.05,
    "method": "linear_regression",
    "note": "corrected_confidence = 0.05 + 0.78 * declared_confidence"
  },
  "narrative": "Brier 0.187 - tendenza overconfident specie sopra 80%.
                Quando l'agent dichiara 90%, il vero hit rate è 71% (-22pp).
                Applicare la correzione lineare per output user-facing."
}
```

---

## Come le skill leggeranno questo file

```
PRIMA (no calibration):
  output: "confidence 80%"

DOPO (con calibration_correction):
  declared = 0.80
  corr = json.load("confidence_correction.json")["correction"]
  corrected = corr["offset"] + corr["multiplier"] * declared  # 0.05 + 0.78*0.80 = 0.674
  output: "confidence 80% (corretta 67% per overconfidence storica)"

Le skill che dichiarano confidence:
  gex-analysis           (scenario principale + alternativo, %)
  scalp-execution        (edge stimato BASSO/MEDIO/ALTO mappato a %)
  derivatives-dashboard  (confidence ALTA/MEDIA/BASSA mappato a %)
  proactive-scout        (score normalizzato a confidence %)
  macro-regime-monitor   (regime score → confidence di classificazione)
```

---

## Frequenza & operative

```
CRON:                   monthly (1° del mese 03:30 UTC)
LOOKBACK:               90 days
MIN CLAIMS:             30 per calibration, 50+ raccomandato
RECOMPUTE TRIGGER:      manual quando regime cambia drasticamente

OUTPUT FILE:            calibration/confidence_correction.json
LOG FILE:               calibration/confidence_log.json (append-only)

INTEGRAZIONE:
  - le skill loggano confidence in ogni output (append a log)
  - cron monthly chiude i claim expirati e ricalibra
  - skill leggono correction al runtime per aggiustare output
```

---

## Errori da evitare nel modulo

```
Considerare claim non ancora chiusi:
  Solo claim con TTL scaduto E outcome assegnato vanno nel calc.
  Claim pending falsificherebbero il dataset.

Calibration curve con bin sotto 3 osservazioni:
  Drop bin con n<3, sono rumore. Almeno 5 raccomandato.

Brier score solo:
  Brier non distingue under/over confidence. Sempre includere
  la calibration curve completa.

Correzione overshooting:
  Se l'agent dichiara 90% e il vero hit è 70%, NON correggere a 50%.
  La regressione lineare fa già lo smoothing corretto.
  Clip output corrected nel range [0.05, 0.95] per safety.

Non versionare:
  Salvare snapshot delle correzioni mensili. Il regime di calibration
  cambia con il regime di mercato — utile per debugging retrospettivo.

Applicare correzione SENZA dichiararlo:
  Output user-facing deve mostrare la correzione esplicita
  ("80% dichiarato, 67% corretto") per trasparenza e fiducia utente.
```

---

## Riferimento implementativo

```
~/gex-agentkit/calibration/calibration_monitor.py
~/gex-agentkit/calibration/confidence_log.json   (append-only)
~/gex-agentkit/calibration/confidence_correction.json  (output)
~/gex-agentkit/cron/monthly_calibration.sh
```

Le skill markdown leggono `confidence_correction.json` via tool precostruito
(es. `read_confidence_correction()`) e applicano la correzione lineare
al claim prima dell'output.
