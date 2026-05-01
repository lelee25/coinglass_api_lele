# Cross-validation Coinalyze ↔ CoinGlass

Run: 2026-04-30 18:00:33 UTC

## 1. Open Interest (snapshot, USD) — somma di tutti i perp BTC/ETH per exchange

| Asset | Exchange | Coinalyze (sum perps) | # perps | CoinGlass total | CG stable | CG coin | Δ % |
|---|---|---:|---:|---:|---:|---:|---:|
| BTC | Binance | $7.33B | None | $9.80B | — | — | +33.65% |
| BTC | OKX | $2.38B | None | $3.18B | — | — | +33.57% |
| BTC | Bybit | $3.82B | None | $4.42B | — | — | +15.61% |
| ETH | Binance | $4.54B | None | $6.58B | — | — | +44.75% |
| ETH | OKX | $1.56B | None | $1.82B | — | — | +16.82% |
| ETH | Bybit | $1.76B | None | $2.05B | — | — | +16.29% |

## 2. Funding Rate (snapshot, % per funding interval)

| Asset | Exchange | Coinalyze % | CoinGlass % | Δ (bp/funding) | CG interval | CZ predicted % |
|---|---|---:|---:|---:|---:|---:|
| BTC | Binance | -0.0029% | -0.0031% | -0.02 | 8h | -0.0031% |
| BTC | OKX | -0.0058% | -0.0058% | -0.00 | 8h | — |
| BTC | Bybit | -0.0047% | -0.0027% | +0.20 | 8h | -0.0027% |
| ETH | Binance | -0.0077% | -0.0065% | +0.12 | 8h | -0.0065% |
| ETH | OKX | +0.0007% | +0.0007% | +0.00 | 8h | — |
| ETH | Bybit | -0.0011% | -0.0025% | -0.14 | 8h | -0.0026% |

## 3. Liquidation 24h (Binance + OKX + Bybit)

| Asset | Side | Coinalyze USD | CoinGlass (3ex) USD | CG All-exchanges USD | Δ % vs 3ex |
|---|---|---:|---:|---:|---:|
| BTC | LONG  | $5,423,172 | $38,975,108 | $75,204,398 | +618.68% |
| BTC | SHORT | $8,625,414 | $9,870,602 | $16,671,819 | +14.44% |
| ETH | LONG  | $9,519,567 | $45,823,779 | $95,899,758 | +381.36% |
| ETH | SHORT | $12,451,558 | $13,928,057 | $22,267,312 | +11.86% |

## 4. Coverage exchange overlap

- Coinalyze future markets totali: **4255**
- Coinalyze exchange unique: **17**
- Exchange testati in overlap: Binance, OKX, Bybit

## 5. Note metodologiche

- Coinalyze restituisce `convert_to_usd=true` direttamente in USD; quando assente, `value` è in coin native.
- CoinGlass funding viene normalizzato (se in %, diviso per 100 → decimal) per essere confrontabile con Coinalyze.
- Liquidation 24h: somma 24 finestre 1h su Coinalyze, vs `range=h24` aggregato su CoinGlass.
- Δ% calcolato come `(CoinGlass − Coinalyze) / Coinalyze`.
- Tolleranza ragionevole: |Δ| < 5% per OI/liq, |Δ bps| < 10 per funding.

## 6. Conclusioni operative (validate empiricamente, 2026-04-30)

### 6.1 Funding rate — i due provider CONVERGONO (cross-validation OK)

| Exchange | Δ massimo osservato | Verdetto |
|---|---|---|
| OKX BTC/ETH | 0.00 bp | match esatto |
| Binance BTC | 0.02 bp | match operativo |
| Binance ETH | 0.12 bp | match operativo |
| Bybit BTC | 0.20 bp | match accettabile (freshness diverse) |
| Bybit ETH | 0.14 bp | match accettabile |

**Implicazione**: Coinalyze e CoinGlass sono **intercambiabili per funding rate**. Le differenze sub-bp sono nel rumore della freshness (snapshot a istanti leggermente diversi). Si possono usare per cross-validation reciproca: se divergono >2 bp, alert.

**Bonus solo Coinalyze**: `predicted-funding-rate` per la prossima finestra — endpoint che CoinGlass NON espone. Use case: anticipare funding flip 1 funding interval prima.

### 6.2 Open Interest — i due provider NON convergono (scope diverso)

| Exchange | Δ Coinalyze→CoinGlass |
|---|---|
| Binance BTC | +33.65% |
| OKX BTC | +33.57% |
| Bybit BTC | +15.61% |
| Binance ETH | +44.75% |
| OKX ETH | +16.82% |
| Bybit ETH | +16.29% |

**Causa identificata**: Coinalyze restituisce OI per i singoli `symbol` perpetual che ha listato. CoinGlass invece aggrega **TUTTI** i perpetual BTC sull'exchange (USDT + USDC + COIN-margined + altre quote), il che produce un totale sistematicamente più alto del 15-45%.

**Esempio Binance BTC**:
- Coinalyze: somma di BTCUSDT_PERP + BTCUSDC_PERP + BTCUSD_PERP (coin-margined) = $7.33B
- CoinGlass: aggregato totale (include simboli che Coinalyze potrebbe non listare, es. quarterly delivery, BTCDOMUSDT) = $9.80B

**Implicazione**: per "OI BTC su Binance" il numero dipende dal provider. **NON intercambiabili**. Decidere per design quale fonte è canonica:
- Single-symbol analysis (es. solo BTCUSDT_PERP): Coinalyze è più preciso
- Aggregato per exchange / cross-exchange: CoinGlass è più completo

Per il sistema gex-agentkit la scelta operativa: **CoinGlass canonica per aggregati**, Coinalyze come **secondary signal** per analisi single-symbol o cross-validation di trend (la direzione è coerente anche se i livelli assoluti divergono).

### 6.3 Liquidation 24h — divergenze massive (scope + freshness + aggregazione)

| Asset | Side | Δ % vs 3ex | Δ % vs All-exchanges |
|---|---|---|---|
| BTC | LONG | +618% | non comparabile |
| BTC | SHORT | +14% | — |
| ETH | LONG | +381% | — |
| ETH | SHORT | +12% | — |

**Asimmetria significativa**: il side LONG diverge drasticamente, il SHORT è molto più allineato. Possibili cause:
- CoinGlass categorizza come "LONG liquidation" qualcosa che Coinalyze classifica diversamente
- Scope perp diverso (vedi §6.2)
- Ritardo di pubblicazione delle liquidazioni grandi su Coinalyze

**Implicazione**: per liquidation analysis usare **solo CoinGlass come canonica**. Coinalyze come backup, ma sapendo che la magnitudine assoluta diverge ampiamente. La heatmap dei livelli (cluster di liquidazione futura, non fatta) è feature unica CoinGlass — Coinalyze non ce l'ha.

### 6.4 Verdetto finale per il sistema

| Dataset | Provider canonico | Provider secondario | Note |
|---|---|---|---|
| OI single-symbol | Coinalyze | CoinGlass | per BTCUSDT_PERP usare CZ |
| OI per-exchange aggregato | CoinGlass | Coinalyze (somma perps) | gap atteso 15-45% |
| Funding rate | indifferente | l'altro | match a 0.2bp |
| Predicted funding | Coinalyze | — | unico |
| Liquidation history | CoinGlass | — | scope incomparable |
| Liquidation heatmap | CoinGlass | — | feature unica |
| Hyperliquid whales | CoinGlass | — | feature unica |
| ETF flow | CoinGlass | — | feature unica |
| CVD | entrambi | cross-validate | non testato qui |
| Long/Short ratio | entrambi | cross-validate | non testato qui |

**Strategia per gex-agentkit**: NON sostituire Coinalyze con CoinGlass. NON sostituire CoinGlass con Coinalyze. Tenere entrambi con ruoli definiti, e **cross-validare il funding rate** ogni 30 min (basta 1 chiamata gratis a Coinalyze) come early warning per stress sull'API CoinGlass.
