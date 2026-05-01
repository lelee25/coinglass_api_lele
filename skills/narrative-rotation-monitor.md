---
name: narrative-rotation-monitor
description: >
  Identifica quale narrativa "tira" nel mercato crypto (AI, DeFi, RWA, L2,
  Memes, Gaming, Privacy, Stablecoin, Liquid Staking) tramite tracking
  performance di sector via CoinGecko /coins/categories. Rileva rotation
  (sector che entra/esce dalla top performance) per asset selection swing.
  La rotation precede di 1-3 settimane gli outperformance migliori.
  Trigger: "narrative attiva", "sector rotation", "AI tokens", "DeFi recovery",
  "RWA narrative", "L2 momentum", "che narrativa tira", "alt season check",
  "rotation BTC altcoin", "category leader", "narrative shift", "theme detect",
  "settore migliore". Cron 4h. Output: top 3 narrative + asset selezionati per
  ogni narrative + bias swing per gli asset core.
---

# Narrative Rotation Monitor — il radar dei sector

## Filosofia: i token salgono per categoria, non da soli

Le altcoin raramente salgono in isolamento. Salgono quando la **narrativa
del sector** attira capitale:

```
2024 Q1 — AI tokens (FET, RNDR, AGIX) — narrativa "AI agent x crypto"
2024 Q2 — RWA (ONDO, CFG, MKR) — narrativa "real world assets"
2024 Q3 — Memecoin (DOGE, SHIB, WIF) — narrativa "retail euforia"
2024 Q4 — L2 (ARB, OP, MATIC) — narrativa "rollup adoption"
2025 Q1 — DePIN (HNT, FIL, RNDR) — narrativa "decentralized infrastructure"

Ogni narrative dura 4-12 settimane. Chi entra nella TOP 3 sector all'inizio
della rotation outperforma il mercato del +30-100%.
Chi entra dopo che è in TOP 3 da 4 settimane = late, magnitudo residua minore.
```

L'edge è **detection precoce della rotation**: identificare la narrativa che
sta SALENDO nelle top performance, non quella già lì.

---

## Data sources

```
PRIMARY — CoinGecko /coins/categories:
  GET /coins/categories?order=market_cap_change_24h_desc
  GET /coins/categories?order=market_cap_change_24h_asc
    Output: list di {category_id, name, market_cap, market_cap_change_24h,
                     content, top_3_coins, volume_24h}
  
  Categorie chiave (filtrare per relevance):
    - Artificial Intelligence (AI)
    - Real World Assets (RWA)
    - DeFi
    - Layer 2 (L2)
    - Memes
    - Gaming
    - Liquid Staking
    - DePIN
    - Privacy
    - Stablecoins (escludere — non rotation, è infrastructure)

SECONDARY — Per ogni sector top:
  GET /coins/markets?category={cat_id}&order=volume_24h_desc&per_page=10
    -> top 10 token del sector per volume

CROSS-VALIDATE:
  CoinGlass /api/futures/funding-rate per asset core di ogni narrative
  CoinGecko /search/trending (correlation con interesse retail)
  Coinalyze /open-interest-history per confermare volume futures

CALCOLI CLIENT-SIDE:
  Sector momentum score = weighted(price_change_pct: 1d=0.3, 7d=0.5, 30d=0.2)
  Sector flow ratio = sector_volume_24h / total_crypto_volume_24h
  Rotation index = position_change_in_ranking_7d
```

---

## Algoritmo di rotation detection

### Step 1 — Snapshot daily performance per category (cron 4h)

```
Per ogni category nei top 30 by mcap:
  performance_1d_pct
  performance_7d_pct  
  performance_30d_pct
  volume_24h_usd
  market_cap_usd
  position_in_ranking_now
  position_in_ranking_7d_ago

momentum_score = 0.3 * perf_1d + 0.5 * perf_7d + 0.2 * perf_30d
```

### Step 2 — Rotation classification

```
EMERGING (new leader):
  position_now in top 3
  position_7d_ago > 5
  -> "novità positiva", probabilità outperformance prossima settimana

ESTABLISHED (stable leader):
  position_now in top 3
  position_7d_ago in top 3
  -> momentum confermato, edge moderato (parte del move già fatto)

FADING (loss of leadership):
  position_now > 5
  position_7d_ago in top 3
  -> momentum esausto, evitare nuovi long sul sector

DORMANT (no leadership):
  position_now > 10 stable
  -> nessun signal
```

### Step 3 — Asset selection per narrative attiva

```
Per ogni EMERGING o ESTABLISHED category:
  fetch /coins/markets?category={cat_id}&order=volume_24h_desc
  
  Filter top 5 token con:
    - volume_24h > $50M (liquidity safe)
    - market_cap > $200M (not micro cap)
    - perp futures available su Bitget/Binance/Bybit
    - non già in active_positions
  
  Per ogni token:
    - performance vs sector (alpha vs beta)
    - perp funding rate (overheat check)
    - whale_alerts onchain status

OUTPUT:
  top_3_picks_per_narrative
```

### Step 4 — Cross-validation con altri signal

```
Conferma narrative con:
  - Trending CoinGecko: sector token in /search/trending?
  - News sentiment: news cluster bullish per il sector?
  - ETF flow: se BTC, è coerente con narrative?
  - Macro regime: in CAPITULATION, narrative emergent = fake bounce?

Se ≥ 2 conferme: narrative_strength = HIGH
Se 1 conferma: MEDIUM
Se 0: LOW (potrebbe essere rumore short-term)
```

---

## Output: scrittura context.json

### context.narrative_signal (refresh 4h)
```json
{
  "narrative_signal": {
    "ts": "2026-05-01T16:00:00Z",
    "ttl_hours": 4,
    "active_narratives": [
      {
        "category_id": "artificial-intelligence",
        "name": "AI Tokens",
        "status": "EMERGING",
        "momentum_score": 4.2,
        "perf_1d_pct": +3.8,
        "perf_7d_pct": +18.5,
        "perf_30d_pct": +42.1,
        "ranking_change_7d": "+5 positions",
        "volume_share_pct": 8.4,
        "narrative_strength": "HIGH",
        "confirmations": ["news_cluster_bullish_7d", "trending_3_tokens"],
        "top_picks": [
          {"symbol": "FET", "perf_alpha_pct": +2.1, "funding_8h_bps": 9.2,
           "whale_status": "ACCUMULATION_SILENT", "risk_flag": null},
          {"symbol": "RNDR", "perf_alpha_pct": +1.5, "funding_8h_bps": 12.4,
           "whale_status": "neutral", "risk_flag": "funding_high"},
          {"symbol": "AGIX", "perf_alpha_pct": +0.8, "funding_8h_bps": 7.1,
           "whale_status": "neutral", "risk_flag": null}
        ],
        "narrative_text": "AI tokens in rotation EMERGING. Movement strutturale,
                           news cluster bullish 7gg, top 3 tokens trending.
                           FET miglior alpha + whale accumulation in corso."
      },
      {
        "category_id": "real-world-assets",
        "name": "Real World Assets",
        "status": "ESTABLISHED",
        "momentum_score": 2.1,
        "narrative_strength": "MEDIUM",
        "narrative_text": "RWA stable in top 3 da 3 settimane. Edge ridotto."
      }
    ],
    "fading_narratives": [
      {
        "category_id": "memes",
        "name": "Memecoin",
        "perf_7d_pct": -4.2,
        "ranking_change_7d": "-4 positions",
        "narrative_text": "Memes esauriti, evitare new long."
      }
    ],
    "btc_eth_modifier": {
      "btc_dominance_trend": "stable",
      "rotation_pressure": "low",
      "interpretation": "Narrative rotation in alts non sta drenando BTC dominance.
                         Edge BTC core mantenuto, alts opportunità tattica."
    }
  }
}
```

---

## Cross-reference con altre skill

```
LETTA DA QUESTA SKILL:
  context.macro_regime          (regime modula relevance — in EUPHORIA, narrative emerging = pump frenzy)
  context.news_signal           (conferma narrative via news cluster)
  context.etf_signal            (BTC dominance shift integra narrative)
  scratchpad.whale_alerts       (whale flag per asset selezionati)
  External: CoinGecko /coins/categories, /coins/markets

DELEGA A (per asset selezionati):
  proactive-scout              (trigger scan dedicato dei top picks narrative)
  whale-onchain-monitor        (deep check sui token selezionati)

LETTO DA:
  proactive-scout              (priorità asset narrative emerging)
  scalp-execution              (boost edge su asset narrative HIGH)
  gex-analysis                 (BTC core: ignora narrative, ETH: considera RWA/L2 link)

SCRIVE:
  context.narrative_signal     (autoritativo, refresh 4h)
  retrospettive.md             (entry settimanale per narrative shift confermati)
```

---

## Errori da evitare

```
Tradare la rotation late:
  Quando una narrative è ESTABLISHED da 4+ settimane, la maggior parte del move
  è fatta. EMERGING è dove c'è alpha, non ESTABLISHED.

Confondere narrative con singolo token spike:
  Un singolo memecoin che fa +100% NON è narrative rotation.
  Narrative richiede ≥ 5 token del sector con momentum coerente.

Ignorare il regime macro:
  In RISK-OFF, narrative emergent sono rimbalzi tecnici corti, non rotation.
  Sempre cross-validate con macro_regime.

Asset selection senza filtro liquidità:
  Token narrative con volume < $20M = slippage uccide alpha.
  Sempre filtrare volume_24h_usd minimo.

Sovrapposizione sector:
  Un token può essere in più category (es. "AI" + "DePIN").
  Sempre primary category per non doppiare segnali.

Ignorare funding overheat:
  Narrative HIGH + funding > p95 = top short-term, NOT entry.
  Sempre attendere funding regress o pullback.

Trattare narrative come BTC/ETH context:
  BTC/ETH hanno proprio regime. Narrative serve per ALT SELECTION, non
  per modificare bias BTC/ETH (eccetto quando rotation è "fuga da BTC").
```

---

## Threshold operativi

```
CATEGORY UNIVERSE:
  top_categories_by_mcap: 30
  min_category_mcap_usd: 1e9
  
EMERGING DETECTION:
  position_now: <= 3
  position_7d_ago: > 5
  momentum_score_min: 2.0

ASSET SELECTION:
  min_volume_24h_usd: 50e6
  min_market_cap_usd: 200e6
  funding_overheat_p95: true (skip asset)
  perp_futures_available: required

CONFIRMATION:
  narrative_strength_high: ≥ 2 confirmations
  narrative_strength_medium: 1 confirmation
  ttl_hours: 4 (recompute frequently in fast moves)
```
