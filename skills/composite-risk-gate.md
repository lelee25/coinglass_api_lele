---
name: composite-risk-gate
description: >
  Kill switch quantitativo del sistema. Aggrega segnali multi-fonte (drawdown,
  realized vol, exchange health, news critical, whale STRUCTURAL bearish,
  funding extreme, macro RISK-OFF) e decide se DISABILITARE temporaneamente
  l'esecuzione automatica. È l'unica skill con AUTORITÀ DI VETO sul sistema —
  altri agent leggono system_state.kill_switch_active e si fermano.
  Trigger: "kill switch", "stop trading", "sospendi sistema", "circuit breaker",
  "risk gate", "panic mode", "stop automatic", "BTC crash check",
  "exchange outage", "exploit notify", "vola estrema", "system health".
  Asimmetria intenzionale: può fermare il sistema, non può aprire trade.
  Cron 5min + event-driven (news critical immediate, drawdown breach immediate).
---

# Composite Risk Gate — il guardian del sistema

## Filosofia: il guardian dice solo NO

Un sistema automatico che fa solo trade ha un punto cieco: nessuno guarda il
sistema STESSO. Quando le cose vanno male (exploit, exchange halt, flash crash,
modello errato), l'agent operativo continua a eseguire seguendo le sue regole
locali — ma le regole non sono valide in quel momento.

```
ASIMMETRIA DEL GUARDIAN:
  - Può DISABILITARE il sistema (write system_state.kill_switch_active = true)
  - NON può aprire/chiudere/modificare trade direttamente
  - L'autorità è "stop everything", non "do something"
  
PERCHÉ ASIMMETRICO:
  Un agent che può solo dire NO è strutturalmente più sicuro.
  Errori del guardian = pause inutili = costo basso (opportunity cost).
  Errori dell'esecutore = trade in regime invalid = costo alto (loss reale).
```

Quando il kill switch si attiva:
- jarvis-main / gex-analyst / macro-master leggono `system_state.kill_switch_active = true`
- Tutti smettono di aprire nuovi trade
- Le posizioni aperte rimangono (chiusura manuale o via risk-forward esplicito)
- Il sistema resta in pause finché le condizioni di resume sono soddisfatte

---

## I 7 trigger del kill switch

### 1. PRICE DRAWDOWN ESTREMO
```
CONDIZIONI:
  BTC price drop > 8% in 1h, OR > 12% in 4h
  Confermato cross-exchange (Bitget + Binance + OKX)

INTERPRETAZIONE:
  Flash crash o evento sistemico. Modelli statistici falliscono.

RESUME CONDITION:
  Prezzo stabile (vola realized < 2σ) per 1h consecutiva
  AND drawdown 24h < -5%
```

### 2. REALIZED VOLATILITY EXTREME
```
CONDIZIONI:
  Realized vol 1h > 3σ sopra media 7gg
  Per ≥ 2 cicli consecutivi (5min)

INTERPRETAZIONE:
  Mercato erratico, slippage estremo, stop infallible-mente saltati.

RESUME CONDITION:
  Realized vol 1h < 1.5σ per 30min
```

### 3. EXCHANGE OUTAGE / WS DISCONNECT
```
CONDIZIONI:
  Bitget WS no tick > 60s    (execution venue)
  OR Binance WS no tick > 90s
  OR Coinalyze API > 2 fail consecutive
  OR CoinGlass API 5xx > 3 in 5min

INTERPRETAZIONE:
  Health del provider compromesso. Esecuzione non affidabile.

RESUME CONDITION:
  Tutti i provider rispondenti per 5min consecutivi
```

### 4. NEWS CRITICAL EVENT
```
CONDIZIONI:
  news-sentiment-monitor segnala CRITICAL category:
    - Exchange hack/halt
    - Stablecoin de-peg
    - Smart contract exploit (asset detenuti)
    - Regulation announcement major (SEC enforcement, etc.)
  
  OR sentiment score < -0.7 (very bearish) sostenuto 30min

INTERPRETAZIONE:
  Catalyst che azzera analisi tecnica. Reazione market unpredictable.

RESUME CONDITION:
  News categorizzata come "CONTAINED" + 2h cooldown
```

### 5. WHALE STRUCTURAL BEARISH (system-wide)
```
CONDIZIONI:
  whale-onchain-monitor segnala STRUCTURAL DISTRIBUTION
  Per BTC AND ETH simultaneamente
  Persistente per ≥ 4 cicli (1h)

INTERPRETAZIONE:
  Smart money in fuga sistemica. Trade contrarian = combattere big money.

RESUME CONDITION:
  whale signal NEUTRAL o BULLISH su almeno BTC OR ETH
```

### 6. FUNDING EXTREME REGIME
```
CONDIZIONI:
  funding-arb-detector segnala REGIME_EXTREME
  median > +50 bps OR < -25 bps
  Per ≥ 3 cicli (24h)

INTERPRETAZIONE:
  Posizionamento estremo globale. Flush imminente in una direzione.

RESUME CONDITION:
  Median funding rientra in range [-15, +30] bps per 4h
```

### 7. PORTFOLIO LOSS CIRCUIT
```
CONDIZIONI:
  Active positions aggregate PnL < -5% del portfolio in 24h
  OR max drawdown da peak > -10% in 7gg

INTERPRETAZIONE:
  Performance fuori specifica. Possibile bias persistente nel sistema.

RESUME CONDITION:
  Manual review (richiede intervento utente per resume)
  AND aggregate PnL non peggiora ulteriormente
```

---

## Algoritmo di valutazione

```
STEP 1 — Fetch state (cron 5min, event-driven critical)
  Per ogni trigger:
    raw_value = fetch_metric()
    triggered = evaluate_condition(raw_value, threshold)

STEP 2 — Aggregate
  active_triggers = [t for t in triggers if triggered]
  
  Se active_triggers contiene "CRITICAL_NEWS" o "PORTFOLIO_LOSS":
    -> kill_switch_active = true (single trigger sufficient)
  
  Se ≥ 2 trigger non-critical attivi simultaneamente:
    -> kill_switch_active = true
  
  Se 1 trigger non-critical attivo:
    -> kill_switch_warning = true (monitor + alert, no kill)

STEP 3 — Persist + notify
  Write system_state.json
  Push notify se cambio stato (off->warning, off->kill, kill->off)

STEP 4 — Auto-resume check (every cycle)
  Per ogni trigger ancora attivo, verifica resume condition
  Se TUTTI i resume soddisfatti -> kill_switch_active = false
  Eccezione: PORTFOLIO_LOSS richiede manual review (no auto-resume)
```

---

## Output: system_state.json (autoritativo)

```json
{
  "system_state": {
    "ts": "2026-05-01T14:30:00Z",
    "kill_switch_active": true,
    "kill_switch_warning": false,
    "active_triggers": [
      {
        "trigger": "PRICE_DRAWDOWN_EXTREME",
        "activated_at": "2026-05-01T14:25:00Z",
        "details": "BTC -9.2% in 38min, cross-validated all venues",
        "resume_condition": "Realized vol 1h < 1.5σ AND drawdown 24h < -5%"
      },
      {
        "trigger": "WHALE_STRUCTURAL_BEARISH",
        "activated_at": "2026-05-01T14:00:00Z",
        "details": "BTC + ETH STRUCTURAL distribution per 4 cicli",
        "resume_condition": "whale signal NEUTRAL/BULLISH su BTC o ETH"
      }
    ],
    "narrative": "DOUBLE TRIGGER: price drawdown + whale distribution.
                  Sistema sospeso. Posizioni aperte mantenute, no nuovi trade.
                  Auto-resume quando condizioni soddisfatte.",
    "last_state_change": {
      "from": "off",
      "to": "kill",
      "ts": "2026-05-01T14:25:00Z"
    },
    "stats": {
      "kills_24h": 1,
      "avg_kill_duration_minutes": 48,
      "false_positive_rate_30d": 0.12
    }
  }
}
```

---

## Come gli altri agent leggono il kill switch

```
PRIMA DI OGNI AZIONE OPERATIVA:
  state = read("system_state.json")
  if state.kill_switch_active:
    log("Action blocked by kill switch")
    return  # NO new trade, NO modifica posizioni esistenti

PRIMA DI OGNI ANALISI (gex-analysis, derivatives-dashboard):
  state = read("system_state.json")
  if state.kill_switch_warning:
    output += "\n[WARNING] Kill switch in pre-trigger state. Caution."

L'analisi può continuare anche con kill_switch_active — ma non deve produrre
trade signal eseguibili. Output di tipo "MONITOR" o "INFORMATIVE" sono OK.
```

---

## Cross-reference con altre skill

```
LETTA DA QUESTA SKILL (input multi-fonte):
  context.macro_regime          <- macro-regime-monitor (RISK-OFF aggrava)
  context.funding_signal        <- funding-arb-detector (REGIME_EXTREME)
  context.etf_signal            <- etf-flow-interpreter (outflow streak amplifier)
  scratchpad.whale_alerts       <- whale-onchain-monitor (STRUCTURAL flag)
  scratchpad.news_alerts        <- news-sentiment-monitor (CRITICAL events)
  scratchpad.active_positions   (per portfolio loss check)
  Bitget/Binance WS health      (latency monitoring)
  External: API health endpoints (CoinGlass, Coinalyze, CoinGecko)

SCRIVE:
  system_state.json (autoritativo, letto da TUTTI gli altri agent)
  scratchpad.kill_switch_log (rolling 30gg per analisi false positive)
  retrospettive.md (entry per ogni kill triggered + outcome)

NON DELEGA — è terminale.
NON ESEGUE TRADE — non può aprire/chiudere/modificare.
```

---

## Errori da evitare

```
False positive frequenti:
  Threshold troppo strette = sistema spesso pause = utente perde fiducia.
  Calibrare su 30gg storico per minimizzare. Target: < 0.15 FP rate.

Auto-resume troppo aggressivo:
  Resume dopo 1 ciclo OK = whipsaw. Sempre richiedere ≥ 2 cicli pulite.

Kill su single weak trigger:
  Solo CRITICAL_NEWS e PORTFOLIO_LOSS sono single-trigger.
  Gli altri richiedono ≥ 2 attivi simultaneamente.

Non differenziare warning vs kill:
  Warning state preserva il sistema operativo ma alza l'attenzione.
  Kill ferma completamente. Distinguere è essenziale.

Non loggare il rationale:
  Ogni kill deve avere narrative chiara nel log per analisi retro.
  Senza, impossibile capire FP causes.

Manual override silenzioso:
  Se user vuole sovrascrivere il kill, deve essere ESPLICITO e LOGGATO
  con motivazione. Mai bypass automatico.

Confondere kill switch con stop loss:
  Stop loss = chiusura posizione. Kill switch = pause sistema.
  Le posizioni aperte SOPRAVVIVONO al kill switch — gestione separata.
```

---

## Threshold operativi (default — calibrabili)

```
PRICE DRAWDOWN:
  1h_pct: -8%
  4h_pct: -12%

REALIZED VOL:
  1h_z_score: 3.0
  persist_cycles: 2

EXCHANGE HEALTH:
  ws_no_tick_seconds: 60 (Bitget), 90 (Binance)
  api_5xx_count_5min: 3
  api_fail_consecutive: 2

NEWS:
  critical_categories: ["hack", "halt", "depeg", "exploit", "enforcement"]
  sentiment_threshold: -0.7

WHALE:
  structural_assets_required: 2 (BTC + ETH simultaneous)
  persist_cycles: 4

FUNDING:
  median_high: +50 bps
  median_low: -25 bps
  persist_cycles: 3 (24h)

PORTFOLIO:
  loss_24h_pct: -5%
  max_drawdown_7d_pct: -10%
```
