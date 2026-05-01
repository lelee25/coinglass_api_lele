---
name: whale-onchain-monitor
description: >
  Identifica movimenti dei grandi player (whale) tramite Hyperliquid native API
  + flussi onchain dei pool stablecoin (USDT/USDC/WBTC) di Ethereum + indice
  HHI di concentrazione wallet. I whale muovono il prezzo 4-12h prima dei
  segnali tecnici classici. Skill REAL-TIME (cron 15min su BTC/ETH).
  Trigger: "whale activity?", "movimenti grandi player", "HHI concentration",
  "Hyperliquid whales", "vault tracking", "accumulation detect", "distribution",
  "rotation BTC ETH", "smart money flow", "stablecoin inflow", "whale alert",
  "pool USDT BTC", "tx grandi", "wallet concentration".
  Output: alert level + top 5 movements + bias signal letto dalle altre skill.
  NON sostituisce gex-analysis — è un EARLY WARNING che le skill tecniche
  consultano per anticipare cambi di regime intraday.
---

# Whale & Onchain Monitor — early warning capitale grosso

## Filosofia: i whale fanno i prezzi, gli analisti li spiegano dopo

I segnali tecnici (StochRSI, candlestick, livelli GEX) descrivono il
**risultato** del posizionamento dei grandi player. Quando un whale ha già
caricato $50M di BTC long su Hyperliquid, il segnale tecnico si forma 4-12h
**dopo**. Questa skill cattura il segnale prima della sua manifestazione tecnica.

```
Pipeline classica:           whale agisce -> prezzo si muove -> tecnico segnala
Pipeline con whale-monitor:  whale agisce (rilevato) -> alert -> tecnico conferma
```

L'edge non è "tradare quello che fa il whale" (slippage, ritardo, conflitto).
L'edge è **prepararsi**: aumentare attenzione nel direzione del whale flow,
ridurre size in posizioni contrarian.

---

## Data sources

```
HYPERLIQUID NATIVE API (gratis, no auth — verificato 2026-05-01 con tests/test_hyperliquid.py):
  POST https://api.hyperliquid.xyz/info
  
  ENDPOINT TYPE VERIFICATI AVAILABLE:
    {"type":"meta"}                 -> universe 230 asset (BTC, ETH, ATOM, ...)
    {"type":"allMids"}              -> prezzi current per ogni asset
    {"type":"metaAndAssetCtxs"}     -> ★ OI, funding, premium, oracle, mark per ogni asset
    {"type":"fundingHistory","coin":"BTC","startTime":...} -> 24 sample/24h
    {"type":"clearinghouseState","user":"0x..."}  -> account state per wallet
    {"type":"openOrders","user":"0x..."}          -> open orders per wallet
    {"type":"userFills","user":"0x..."}           -> fill history per wallet
    {"type":"candleSnapshot","req":{...}}         -> OHLC per asset
    {"type":"l2Book","coin":"BTC"}                -> orderbook L2

  ★ CAVEAT IMPORTANTE — leaderboard NON è API public:
    "type":"leaderboard" NON è esposto come tipo /info pubblico.
    La pagina https://app.hyperliquid.xyz/leaderboard è UI client-side
    che fa chiamate non documentate.
    
    WORKAROUND PRATICO:
      1. Whitelist top 20 wallet manuale (curato dall'utente, refresh mensile)
         Source: scraping della dashboard via Playwright/Puppeteer una volta
                 al mese, salva lista in config/hyperliquid_whales.json
      2. Tracking automatico: per ogni wallet whitelisted chiama
         clearinghouseState + userFills ogni 15min, calcola delta.
      3. Alternative: monitor metaAndAssetCtxs.openInterest aggregato per
         asset = leading indicator senza per-wallet detail (meno specifico
         ma sempre utile).

ONCHAIN DEX FLOW (CoinGecko Demo, verificato §22.6):
  /onchain/networks/eth/pools/multi/{addrs} -> batch state pool USDT-WBTC, USDC-ETH
  /onchain/networks/eth/pools/{addr}/trades -> ultimi 300 swap del pool
  /onchain/networks/eth/tokens/{addr}/pools  -> top pool per ogni token
  /onchain/tokens/info_recently_updated     -> token in attention spike
  /coins/{id}/contract/{address}            -> metadata smart contract

  Pool da monitorare (Ethereum):
    WBTC/USDC Uniswap v3 0.3%: 0x99ac8ca7087fa4a2a1fb6357269965a2014abc35
    USDT/USDC Uniswap v3 0.01%: 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640
    WBTC/USDT Uniswap v3 0.3%: 0x9db9e0e53058c89e5b94e29621a205198648425b
    WETH/USDC Uniswap v3 0.05%: 0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640
    WETH/USDT Uniswap v3 0.3%: 0x4e68ccd3e89f51c3074ca5072bbac773960dfa36

CALCOLI CLIENT-SIDE:
  HHI (Herfindahl-Hirschman Index) sui tx_from_address dei 300 trade:
    HHI = sum((volume_wallet_i / total_volume) ^ 2) * 10000
    Range: 0 (perfetta dispersione) a 10000 (monopolio totale)
    Soglie statiche (calibrabili — vedi references/calibration-thresholds.md):
      HHI < 1000  -> retail spread normale
      HHI 1000-2500 -> alcuni medi player attivi
      HHI > 2500 -> alta concentrazione, whale dominance
      HHI > 5000 -> singolo whale dominante

  HHI VELOCITY (ΔHHI/h) — il vero alpha:
    velocity = HHI_now - HHI_1h_ago
    Statico HHI ti dice STATO. Velocity ti dice MOVIMENTO.
    Token con HHI stabile a 5000 da settimane = "concentrato e dormiente".
    Token con HHI da 2500 -> 4500 in 4h = ACCUMULAZIONE ATTIVA in corso.
    Soglia alert: ΔHHI > +500/h sostenuto per 2+ cicli = pre-move signal forte
    (validato §15.2 INTEGRATION-NOTES).

  GINI coefficient (alternativa robust):
    gini = (n+1-2*Σcumsum)/n applicato ai trade volumes
    Soglia alert: Gini > 0.85 con HHI velocity > +500/h

CROSS-VALIDAZIONE OBBLIGATORIA:
  HHI alto su pool con TVL < $1M = rumore (poche tx).
  HHI alto + TVL > $5M + volume 24h > $1M = segnale.
  Sempre filtrare per liquidity prima di alertare.
```

---

## Asset coverage — dove la skill funziona davvero

```
✅ FUNZIONA BENE:
  - Pool stablecoin <-> WBTC/WETH (flusso stablecoin -> BTC/ETH)
    Esempio: USDT/WBTC pool 0.3% Uniswap v3 — cattura whale che switchano
    da fiat-stable a BTC/ETH (accumulazione cross-asset)
  - Altcoin DEX con liquidity concentrata in 1-2 pool (Uniswap, Raydium):
    pre-pump detection via ΔHHI/h positivo + holder_delta_7d positivo
  - Hyperliquid wallet pubblici per perp positioning
  
⚠️ FUNZIONA LIMITATO:
  - Token cross-chain o multi-pool (Solana, BSC, Polygon mix):
    serve aggregare HHI cross-pool, complessità computazionale
  - Token con liquidity in CEX > 80% (es. memecoin maturati):
    DEX pool perde rappresentatività
  
❌ NON FUNZIONA:
  - Distribuzione HOLDER di BTC/ETH stessi:
    troppi wallet (>50M BTC, >250M ETH), distribution stabile,
    HHI ricalibrato non cambia. Per BTC/ETH usa il PROXY:
    pool stablecoin/WBTC come misura del FLUSSO, non della distribuzione.
  - Wallet CEX retail:
    nessun identifier pubblico, by design dei CEX. Hyperliquid è eccezione
    perché è perp DEX onchain.
```

---

## I 4 pattern operativi rilevabili

### Pattern 1 — ACCUMULATION SILENT
```
SEGNALI CONTEMPORANEI:
  Inflow netto su pool stablecoin -> WBTC/WETH > 24h media
  HHI > 0.25 (concentrazione alta)
  Stessi 3-5 wallet ripetuti nei buy
  Hyperliquid: wallet del leaderboard aumenta long size senza spike notional

INTERPRETAZIONE:
  Whale sta accumulando senza causare movimento di prezzo
  -> BIAS bullish 24-72h, ma non intraday

ALERT LEVEL: MEDIUM
DURATA: il segnale resta valido finché HHI > 0.25 e flow netto positivo
```

### Pattern 2 — DISTRIBUTION COVERT
```
SEGNALI:
  Outflow netto WBTC/WETH -> stablecoin
  HHI > 0.25 nei sell
  Hyperliquid: top wallet riducono long, alcuni invertono short
  Spesso accompagnato da prezzo che fa nuovi massimi (rally guidato dal retail
  che assorbe il sell del whale)

INTERPRETAZIONE:
  Whale distribuisce sul rally retail. Top imminente.
  -> BIAS bearish 6-24h

ALERT LEVEL: HIGH (uno dei pattern più predittivi)
INTEGRAZIONE: combinare con derivatives-dashboard P1 (divergenza OI/Price)
```

### Pattern 3 — ROTATION BTC -> ETH (o viceversa)
```
SEGNALI:
  Pool WBTC/USDC: outflow WBTC + inflow USDC dello stesso wallet
  Pool WETH/USDC: inflow WETH dallo stesso wallet poco dopo
  HHI alto su entrambi i pool nello stesso timeframe (15min)

INTERPRETAZIONE:
  Capitale ruota da BTC a ETH (o inverso)
  -> Possibile preludio altseason o flight to safety

ALERT LEVEL: HIGH (direzionalmente specifico)
NOTA: rotation BTC -> ETH storicamente precede di 2-7 giorni outperformance ETH
```

### Pattern 4 — CONCENTRATION VELOCITY SPIKE (★ pre-move signal)
```
SEGNALI CONTEMPORANEI:
  ΔHHI/h > +500 sostenuto per ≥ 2 cicli consecutivi (i.e. 30min)
  HHI assoluto attualmente > 2500 (concentrato)
  TVL pool > $1M (segnale non rumore)
  Volume 24h del pool > 2x media 7gg (attivazione recente)

INTERPRETAZIONE:
  Concentrazione che CRESCE rapidamente. Non è "whale presente" — è
  "whale STA accumulando ADESSO". Lead time storico: 4-12h prima del move.

OPERATIVO:
  Per altcoin DEX: setup pre-pump ad alto edge — long size piena se segnale
  tecnico aggiuntivo (volume crescente + breakout di micro-resistenza).
  Per BTC/ETH (via pool stable/WBTC): aumentare size_factor swing long
  per le prossime 8h, ma non triggerare trade autonomamente.

ALERT LEVEL: HIGH (uno dei pochi pattern leading veri)
HISTORICAL: validato §15.2 INTEGRATION-NOTES, "qualcosa sta per succedere"
```

### Pattern 5 — HYPERLIQUID VAULT SPIKE
```
SEGNALI:
  Top vault (per AUM) cambia notional > 5% in 15min
  Apertura/chiusura posizione di > $1M su singolo asset
  Vault con track record (Sharpe > 2 storico) di solito leading

INTERPRETAZIONE:
  Smart money sta ruotando posizioni
  -> BIAS coerente con la direzione del vault, lead 30-90min

ALERT LEVEL: HIGH (alta affidabilità, bassa frequenza)
LIMITAZIONE: solo wallet pubblici Hyperliquid. Bitget/Bybit/Binance non esposti.
```

---

## Algoritmo di scoring & alerting

```
STEP 1 — Calcola metriche del ciclo (15min)
  per ogni pool monitorato:
    netflow_pool[15min] = inflow - outflow (in USD equivalente)
    hhi_pool[15min] = HHI dei 300 trade del pool
    top_wallets[15min] = top 5 wallet per volume

  per Hyperliquid:
    delta_top20 = somma cambi posizioni top 20 wallet (notional USD)
    new_positions_above_1m = numero posizioni nuove > $1M

STEP 2 — Detection pattern
  pattern_active = []
  if netflow_btc_pools < -1M AND hhi > 0.25 AND price_at_local_high:
    pattern_active.append("DISTRIBUTION_COVERT")
  if netflow_btc_pools > 5M AND hhi > 0.25 AND price_flat_or_down:
    pattern_active.append("ACCUMULATION_SILENT")
  ... etc

STEP 3 — Aggregazione alert level
  level = max(pattern.alert_level for pattern in pattern_active) or "LOW"

STEP 4 — Smoothing
  Pattern singolo che appare per la prima volta -> NOTICE (no escalation)
  Pattern confermato per 2 cicli consecutivi -> ALERT (escalation)
  Pattern confermato per 4+ cicli -> STRUCTURAL (alta confidence)
```

---

## Output: scrittura scratchpad.json + alert push

### scratchpad.whale_alerts (rolling 24h, max 50 entries)

```json
{
  "whale_alerts": [
    {
      "ts": "2026-05-01T12:15:00Z",
      "level": "ALERT",
      "pattern": "DISTRIBUTION_COVERT",
      "asset": "BTC",
      "direction": "BEARISH",
      "magnitude": "high",
      "evidence": {
        "pool_netflow_usd": -8.4e6,
        "hhi": 0.34,
        "top_wallets_count": 3,
        "btc_price_change_pct": +0.4,
        "hyperliquid_delta_top20": -12.5e6
      },
      "narrative": "3 wallets venduti $8.4M WBTC mentre BTC saliva +0.4%.
                    Hyperliquid top 20 ridotto long $12.5M. Distribuzione covert
                    su rally retail."
    },
    ...
  ],
  "current_bias": {
    "BTC": "BEARISH_WHALE",
    "ETH": "NEUTRAL",
    "rotation_active": null
  }
}
```

### Alert push immediato (level HIGH/STRUCTURAL)
```
[WHALE ALERT] {asset} {direction} — {pattern}
Evidence: {1 line evidence}
Suggested action: {bias-aware suggestion}
TTL: 60min (poi rivaluta)
```

---

## Threshold operativi (calibrabili — vedi references/calibration-thresholds.md)

```
HHI (scala 0-10000, standard Glassnode/CCN):
  Soglia attivazione pattern: 2500 (default)
  Soglia "highly concentrated": 5000
  Calibrazione: percentile 90° rolling 30gg sul pool specifico

HHI VELOCITY (ΔHHI/h):
  Soglia alert: > +500/h sostenuto per ≥ 2 cicli (30min)
  Soglia critical: > +1000/h sostenuto per ≥ 3 cicli (45min)

NETFLOW POOL:
  ACCUMULATION threshold: > 1.5σ sopra rolling 7gg netflow
  DISTRIBUTION threshold: < -1.5σ sotto rolling 7gg netflow

HYPERLIQUID DELTA:
  Vault spike: > 5% notional vault, oppure > $1M assoluto
  Top 20 aggregato: > $10M shift in 15min

WHALE TRANSACTION:
  Single tx > $500k -> log come "potential whale"
  Single tx > $2M -> sempre alert NOTICE
```

---

## Cross-reference con altre skill

```
LETTA DA:
  price-alert-trigger     -> aggiunge "whale activity" come 6° check checklist
                             (se ALERT HIGH bearish e segnale long -> downgrade)
  gex-analysis            -> usa current_bias per pesare la cascata decisionale
  derivatives-dashboard   -> integra come early-warning in lettura composita
  macro-regime-monitor    -> aggregato whale flow in modifier ETF/institutional

SCRIVE:
  scratchpad.whale_alerts (rolling 24h)
  context.whale_bias = {BTC, ETH, rotation_active}
  retrospettive.md (solo level STRUCTURAL — pattern persistenti)

NON SCRIVE:
  retrospettive per ogni alert (sarebbero centinaia)
  decisioni di trade (delegato a skill veloci)
```

---

## Errori da evitare

```
Tradare il whale alert da solo:
  Il whale può essere wrong. L'edge è "filtro di qualità", non "trigger".
  Sempre confermare con gex-analysis o scalp-execution prima di entrare.

Confondere flow legittimo con whale:
  Market maker exchange, treasury aziendali, cold wallet movement = grossi
  ma non smart money. Filtrare wallet noti (binance hot wallet, coinbase, etc.)
  via blacklist da aggiornare manualmente.

Sovrapesare HHI singolo ciclo:
  HHI variabile sessione per sessione. Significativo solo se persiste > 2 cicli.

Ignorare i pool con liquidity bassa:
  Pool < $10M TVL hanno HHI artificialmente alto (poche tx). Filtrare
  TVL minimo prima di calcolare HHI.

Tradare contro un Hyperliquid vault top:
  I vault top hanno track record. Combatterli senza segnale tecnico forte
  è statisticamente perdente. Quando un vault apre $5M long -> NON shortare.
```

---

## Caveat su privacy & legalità

```
TUTTI I DATI SONO PUBBLICI:
  Hyperliquid wallets sono pubblici by design (perp DEX onchain).
  Pool Ethereum sono pubblici (lettura mempool/blocks).
  Nessuna deanonimizzazione attiva.

FILTRI ETICI:
  Non pubblicare alert su singoli wallet identificabili pubblicamente.
  Nei log/scratchpad usa hash troncato (es. "0x9af...3c2").
  L'alert si riferisce al PATTERN, non al wallet.
```
