# Pine Scripts — gex-agentkit TradingView signal layer

> **Status**: 5 script production-ready, Pine Script v6, validati syntax 2026-05-08.
> **Costo runtime**: €0 (sfruttano TradingView Premium €67.95/mo già pagato).
> **Bandwidth**: 5 alert sui 400 disponibili Premium tier.

## Architettura del flusso

```
TradingView Premium
  ├─ 01_hurst_regime_filter.pine          (chart 4h BTC)
  ├─ 02_vix_term_structure.pine           (chart daily SPX o VIX)
  ├─ 03_btcd_usdtd_crypto_regime.pine     (chart daily BTC.D)
  ├─ 04_cross_asset_correlation_matrix.pine (chart 4h BTC)
  └─ 05_ict_smc_confluence.pine           (chart 15m/1h BTC, ETH)
       │
       │ webhook POST JSON
       ↓
  https://your-server.com/api/tv/webhook
       │
       │ ack 200 < 50ms
       ↓
  Cloudflare Worker / Lambda → queue → backend gex-agentkit
       │
       ↓
  Multi-agent decision (jarvis-main, gex-analyst, macro-master, sentinel-agent)
```

## Setup TradingView (per ogni script)

1. Apri chart dell'asset target (vedi tabella sotto per timeframe)
2. Pine Editor → "New" → "Indicator"
3. Copia-incolla il contenuto del file `.pine`
4. **Modifica l'input "Webhook secret token"** con il tuo token reale (al posto di `REPLACE_WITH_SECRET`)
5. Click "Save" → assegna nome
6. Click "Add to chart"
7. Click destro sul chart → "Add Alert..."
8. Condition: `[nome script]` → `Any alert() function call`
9. Webhook URL: `https://your-server.com/api/tv/webhook`
10. Frequency: `Once Per Bar Close`
11. Save

### Asset/Timeframe consigliati

| Script | Asset chart | Timeframe | Note |
|---|---|---|---|
| 01 Hurst Regime | BTCUSDT | 4h | Master switch — regime stabile su 4h |
| 02 VIX Term Structure | SPX o VIX (daily) | 1D | Macro signal slow |
| 03 BTC.D + USDT.D | CRYPTOCAP:BTC.D | 1D | Regime crypto secolare |
| 04 Cross-Asset Correlation | BTCUSDT | 4h | Macro brain |
| 05 ICT/SMC Confluence | BTCUSDT, ETHUSDT | 15m + 1h | Execution-grade entry |

## Webhook payload schemas

### 01 Hurst Regime
```json
{
  "event": "hurst_regime_change",
  "asset": "BTCUSDT",
  "timeframe": "4h",
  "regime": "trending|mean_reverting|random",
  "prev_regime": "...",
  "hurst": 0.6234,
  "length": 100,
  "price": 64200.50,
  "ts": "2026-05-08T14:00:00Z",
  "secret": "..."
}
```

### 02 VIX Term Structure
```json
{
  "event": "vix_ts_regime_change|vix_ts_rollover_hook",
  "regime": "deep_backwardation|backwardation|neutral|contango|strong_contango",
  "regime_score": 2,
  "vix": 24.50,
  "ratio_vix_vix3m": 1.087,
  "forward_5d_bias": "long_equity_long_crypto",
  "confidence": 0.65,
  "academic_source": "Johnson_2017_JFQA",
  "ts": "...",
  "secret": "..."
}
```

### 03 Crypto Regime
```json
{
  "event": "crypto_regime_change",
  "regime": "btc_season|eth_season|alt_season|stablecoin_season|neutral",
  "confidence": 0.82,
  "universe_recommendation": "btc_eth_only|top_50_alts_enabled|defensive_size_reduce_30pct|...",
  "metrics": {
    "btc_dom": 56.42,
    "usdt_dom": 5.83,
    "total3_momentum_pct": 12.4,
    "ethbtc_above_ma_pct": 8.3
  },
  "ts": "...",
  "secret": "..."
}
```

### 04 Cross-Asset Correlation
```json
{
  "event": "crossasset_regime_change",
  "regime": "risk_on_liquidity|flight_to_safety|decoupled|transitioning",
  "confidence": 0.78,
  "strongest_link": "NDX",
  "strongest_corr": 0.74,
  "correlations": {
    "btc_spx": 0.7234,
    "btc_dxy": -0.6112,
    "btc_gold": -0.1245,
    ...
  },
  "agent_filter": "follow_equity_lead_size_normal|reduce_size_50pct_no_swing|enable_arb_agent_full_size",
  "ts": "...",
  "secret": "..."
}
```

### 05 ICT/SMC Confluence
```json
{
  "event": "smc_confluence_long|smc_confluence_short",
  "asset": "BTCUSDT",
  "timeframe": "15",
  "confluence_score": 92,
  "components": {
    "sweep_sellside": true,
    "sweep_level": 63420.0,
    "near_bullish_fvg": true,
    "fvg_top": 63680.0,
    "fvg_bottom": 63420.0,
    "bos_bullish": true,
    "htf_bias_bullish": true
  },
  "htf_period": "4H",
  "price": 63550.0,
  "atr": 320.0,
  "suggested_stop": 63070.0,
  "suggested_target_1r": 64030.0,
  "suggested_target_2r": 64510.0,
  "ts": "...",
  "secret": "..."
}
```

## Sicurezza webhook

TradingView **non supporta autenticazione header nativa**. Mitigation usata in tutti gli script:

1. **Secret token nel JSON body**: il backend valida `body.secret == expected`
2. **IP whitelist** (TV usa 4 IP fissi documentati 2025):
   ```
   52.89.214.238
   34.212.75.30
   54.218.53.128
   52.32.178.7
   ```
3. **HTTPS obbligatorio** + URL non condiviso (effective secret)

### Backend validation pseudocodice

```python
def webhook_handler(request):
    # 1. IP whitelist
    if request.client_ip not in ALLOWED_TV_IPS:
        return 403

    # 2. Parse JSON
    try:
        payload = json.loads(request.body)
    except:
        return 400

    # 3. Secret validation
    if payload.get("secret") != EXPECTED_SECRET:
        return 401

    # 4. Timestamp freshness (anti-replay)
    ts = parse_iso(payload["ts"])
    if (now() - ts).seconds > 60:
        return 410  # Gone (stale)

    # 5. Push to queue, ack rapido
    queue.push(payload)
    return 200
```

## Limiti tecnici Pine v6 rispettati

| Limite TradingView | Valore max | Usato dagli script |
|---|---:|---:|
| `request.security()` calls | 40 (Premium) | max 8 (script #4) |
| `max_lines_count` | 500 | 500 (script #5) |
| `max_boxes_count` | 500 | 500 (script #5) |
| `max_bars_back` | 5000-10000 | 2000 (script #1) |
| Compiled tokens | 100k | < 5k tutti |
| Loop execution per bar | 500ms | < 50ms tutti |

## Roadmap implementazione

| Settimana | Script | Stato | Effort | Priorità |
|---|---|---|---|---|
| 1 | 01 Hurst, 02 VIX TS, 03 Crypto Regime | Pronti, da deployare | 4-5gg totali | ALTA |
| 2-3 | 04 Cross-Asset Correlation | Pronto | 2-3gg integration | ALTA |
| 4 | 05 SMC Confluence | Pronto, da validare paper trading 1 settimana | 7-10gg testing | MEDIA |

## Caveat & verifiche pre-deploy

⚠️ **PRIMA di salvare ognuno script in TradingView:**

1. **Verifica simbolo nel symbol search** — alcuni ticker potrebbero non essere disponibili sul tuo piano specifico. Es. `CBOE:VIX9D` richiede subscription dati Cboe (free su Premium ma controllare).

2. **Test in Pine Editor**: dopo aver incollato, click "Add to chart" — se compaiono errori, verifica simbolo o syntax.

3. **Backtest visivo**: valuta se i segnali storici hanno senso PRIMA di abilitare webhook (specialmente script #5 SMC).

4. **Webhook test**: prima di andare live, usa endpoint di test (es. webhook.site) per vedere il payload esatto che TradingView invia.

5. **Modificare secret**: TUTTI gli script hanno `"REPLACE_WITH_SECRET"` come default. **Cambia con un token forte** (32+ caratteri random) prima di salvare.

## Limiti noti

- **TradingView non riprova webhook falliti**. Se backend down → alert perso.
  → Mitigation: usa Cloudflare Worker / Lambda con queue dietro.

- **Latency 1-5s tipica, fino a 10s in stress events**.
  → Non adatto per HFT. Per scalp sub-secondo usa Bitget WS.

- **Symbol potrebbe non essere disponibile in real-time**. US equities su Premium possono avere 15min delay (per real-time CME servono subscription extra).

- **Pine Script v6 può evolvere**: questi script usano sintassi v6 stabile a 2026-05-08. Verificare al primo deploy.

## Integration con gex-agentkit skill markdown

Ogni Pine Script alimenta una specifica skill del sistema multi-agent:

| Pine Script | Skill markdown beneficiaria | File |
|---|---|---|
| 01 Hurst | macro-regime-monitor (filter ortogonale) | [skills/macro-regime-monitor.md](../skills/macro-regime-monitor.md) |
| 02 VIX TS | macro-regime-monitor (vol regime) | come sopra |
| 03 Crypto Regime | macro-regime-monitor + proactive-scout (universe selection) | [skills/proactive-scout.md](../skills/proactive-scout.md) |
| 04 Correlation Matrix | macro-regime-monitor (master regime brain) | come sopra |
| 05 SMC Confluence | scalp-execution + price-alert-trigger | [skills/scalp-execution.md](../skills/scalp-execution.md) |

## Risorse documentazione

- [Pine Script v6 Reference](https://www.tradingview.com/pine-script-reference/v6/)
- [Pine Script v6 Migration Guide](https://www.tradingview.com/pine-script-docs/migration-guides/to-pine-version-6/)
- [Webhook Alerts Configuration](https://www.tradingview.com/support/solutions/43000529348-how-to-configure-webhook-alerts/)
- [Pine Script Limitations](https://www.tradingview.com/pine-script-docs/writing/limitations/)
