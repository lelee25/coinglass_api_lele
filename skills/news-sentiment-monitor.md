---
name: news-sentiment-monitor
description: >
  Monitor continuo di news + sentiment crypto via CryptoPanic free + heuristics
  di severity. Categorizza eventi (CRITICAL: hack/halt/depeg/exploit/enforcement,
  HIGH: launch/partnership/listing/breakdown, MEDIUM: announcement/upgrade,
  LOW: opinion/analysis). Produce sentiment score per asset (-1 a +1) e flag
  CRITICAL events che il composite-risk-gate usa per kill switch immediato.
  Trigger: "news check", "ultime news", "sentiment BTC", "cryptopanic",
  "exploit alert", "hack notify", "regulatory news", "ETF announcement",
  "exchange halt", "depeg", "news driven move", "catalyst", "narrative shift",
  "what's happening now". Cron 5min + event-driven webhook se disponibile.
---

# News & Sentiment Monitor — il cervello informativo

## Filosofia: la tecnica si azzera quando entra una news

Il technical analysis è razionale dopo l'evento. **Durante** un evento news,
i livelli GEX, i pattern, i derivatives signal vengono ignorati dal market
per minuti o ore. Il comportamento è dominato da:

```
1. PANICO/EUFORIA (sentiment shift istantaneo)
2. POSITION UNWIND (close veloci indipendenti dai livelli)
3. ALGO NEWS-DRIVEN (HFT che leggono Reuters/Bloomberg first)
```

Senza una skill di news monitoring, l'agent può:
- Aprire long su un supporto GEX 30s prima di un exchange halt
- Mantenere swing in regime "STABLE" mentre uno stablecoin sta de-peggando
- Ignorare un catalyst major (ETF approval) che invalida bias short

L'edge non è "tradare le news" (HFT vince sempre lì). L'edge è
**non essere ciechi** quando le news cambiano il regime informativo.

---

## Data sources

```
★ AGGIORNAMENTO 2026-05-01: CryptoPanic ha RIMOSSO il free tier API.
  Vecchia URL https://cryptopanic.com/api/free/v1/posts/ ritorna HTTP 403.
  Strategia abbandonata. Sostituita con aggregazione RSS multi-source.

PRIMARY — RSS feeds aggregati (verificati empiricamente 2026-05-01):
  
  ✅ FUNZIONANTI (6 feed, parsing feedparser):
    CoinTelegraph:           https://cointelegraph.com/rss              (30 entries)
    CoinTelegraph Markets:   https://cointelegraph.com/rss/category/markets  (30 entries, subset markets)
    The Block:               https://www.theblock.co/rss.xml             (20 entries)
    Decrypt:                 https://decrypt.co/feed                     (55 entries)
    Bitcoin Magazine:        https://bitcoinmagazine.com/.rss/full/      (10 entries)
    CryptoSlate:             https://cryptoslate.com/feed/               (10 entries)
  
  ❌ NON FUNZIONANTE (verificato 2026-05-01):
    CoinDesk:    https://www.coindesk.com/arc/outboundfeeds/rss/  -> HTTP 308 redirect, 0 entries
                 (URL cambiato o bot detection — investigare con browser headers)
  
  DEDUP CROSS-SOURCE:
    Lo stesso evento può comparire in multiple source. Hash su title canonicalizzato
    (lowercase, no punctuation, prime 50 char) + check 24h history.
  
  PARSING (verificato funzionante):
    pip install feedparser (battle-tested, gestisce RSS + Atom + redirect)
    Per ogni entry: {title, summary, link, published, source}
  
  REFRESH:
    Cron 5min, fetch 6 feed in parallelo (HTTP timeout 5s, retry 1)
    Aggregato totale: ~150 entries / 5min, dopo dedup ~30-50 unique.

VEDI tests/test_calendar_news.py per smoke test riproducibile.

OPTIONAL — Aggregator open-source per CLI (raccomandato):
  Esistono repo GitHub che aggregano news crypto già con dedup + sentiment:
    https://github.com/khoadeptry/crypto-news-aggregator
    https://github.com/web3technologies/crypto-news-aggregator
  Possono essere usati come CLI o wrappati in Python.
  
  Alternativa minimale (no dipendenze esterne):
    Implementazione ~100 righe Python usando solo feedparser + heuristics
    keyword-based per severity (definite sotto in "Categorizzazione eventi").

EXCHANGE STATUS (per CRITICAL detection rapida):
  Endpoint pubblici di status (gratis, no auth):
    Binance:  https://www.binance.com/bapi/composite/v1/public/marketing/notice/queryAdLimitedNotice
    Coinbase: https://status.coinbase.com/api/v2/incidents.json
    Bitget:   https://www.bitget.com/api/v2/public/spot/announcements (filtro tag "system maintenance")
  Refresh: cron 5min, parsing per detection halt/maintenance.

FALLBACK SOFT — community sentiment via CoinGecko Demo:
  /coins/{id} ritorna campi sentiment_votes_up_percentage / community_score
  Refresh lento (24h), proxy debole ma free.

SECONDARY — Heuristic sentiment scoring:
  Keyword-based su title (no NLP avanzato necessario per CRITICAL detection):
    CRITICAL_KEYWORDS = ["hack", "exploit", "halt", "suspend", "depeg",
                         "freeze", "rug", "drain", "vulnerability", "crash"]
    BULLISH_KEYWORDS  = ["approval", "etf", "launch", "adopt", "partnership",
                         "buyback", "burn", "upgrade", "spot etf"]
    BEARISH_KEYWORDS  = ["lawsuit", "investigation", "fine", "ban", "delist",
                         "outflow", "selloff", "warning"]

OPTIONAL — Twitter/X via paid API (skip per ora):
  Sentiment crypto-twitter è prezioso ma richiede API paid e processing NLP.
  V2 della skill se l'utente upgrade.

CONTEXT INTERNO:
  scratchpad.active_positions   -> per filtrare news rilevanti per posizioni aperte
  context.macro_regime          -> sentiment magnifies regime
```

---

## Categorizzazione eventi

### CRITICAL — kill switch trigger
```
CONDIZIONI:
  Title contiene CRITICAL_KEYWORDS
  AND asset target è in active_positions OR è BTC/ETH
  AND source è "trusted" (CoinDesk, Bloomberg, Reuters, The Block, exchange official)

ESEMPI:
  "Binance pauses BTC withdrawals due to maintenance"  -> CRITICAL
  "USDT loses peg, trading at $0.97"                    -> CRITICAL
  "Curve Finance hacked, $50M drained"                  -> CRITICAL (exposure check)
  "SEC sues Coinbase"                                    -> CRITICAL

AZIONE:
  Push a composite-risk-gate -> kill switch immediato
  Push notify utente entro 60s
  Log dettagliato in scratchpad.news_alerts
```

### HIGH — bias modifier strong
```
CONDIZIONI:
  BULLISH_KEYWORDS o BEARISH_KEYWORDS major
  Source trusted o aggregato (≥ 3 source riportano)

ESEMPI:
  "BlackRock files for SOL ETF"                         -> HIGH bullish SOL
  "China announces crypto ban (rumored)"                -> HIGH bearish all
  "Strategy buys $500M BTC"                             -> HIGH bullish BTC

AZIONE:
  Update sentiment score per asset
  Modifier per scalp-execution e gex-analysis
  Notify utente
```

### MEDIUM — watch
```
CONDIZIONI:
  Announcement/upgrade/partnership tier 2
  Solo singola source o aggregato debole

AZIONE:
  Aggiorna sentiment score (peso minore)
  No notify, solo log
```

### LOW — noise
```
CONDIZIONI:
  Opinion pieces, technical analysis, predictions personali
  Aggregato debole (1 source)

AZIONE:
  Skip, eventualmente log per audit
```

---

## Algoritmo di processing (cron 5min)

```
STEP 1 — Fetch
  Call CryptoPanic /posts/?filter=hot&public=true&currencies=BTC,ETH,SOL
  Limit: top 50 ultimi 30min (filtra per published_at)

STEP 2 — Dedup + classify
  Per ogni post:
    if hash(title) in already_processed: skip
    
    severity = classify_by_keywords(title)
    sentiment = score_by_keywords(title)  # -1 a +1
    affected_assets = parse_currencies(post)
    
    if severity == "CRITICAL":
      trigger_critical(post)
    elif severity == "HIGH":
      update_high_alert(post)
    
    add_to_log(post, severity, sentiment, ts=now)

STEP 3 — Aggregate sentiment per asset (rolling 1h, 4h, 24h)
  per ogni asset:
    sentiment_1h = weighted_avg(post.sentiment for post in posts_1h
                                weighted by post.severity_weight)
    sentiment_score[asset] = sentiment_1h * 0.6 + sentiment_4h * 0.3 + sentiment_24h * 0.1

STEP 4 — Detect cluster events
  Se ≥ 3 BEARISH HIGH news per stesso asset in 1h:
    -> NEWS_CLUSTER_BEARISH alert
  Se sentiment_4h < -0.5 sostenuto:
    -> SUSTAINED_BEARISH_SENTIMENT alert

STEP 5 — Persist + notify
  Write context.news_signal
  Push notify per CRITICAL e HIGH
```

---

## Output: scrittura context + scratchpad

### context.news_signal (refresh 5min)
```json
{
  "news_signal": {
    "ts": "2026-05-01T15:00:00Z",
    "ttl_minutes": 30,
    "sentiment_by_asset": {
      "BTC": {
        "score_1h": 0.15,
        "score_4h": 0.42,
        "score_24h": 0.38,
        "trending_direction": "bullish",
        "top_news": [
          {"title": "BlackRock IBIT crosses $50B AUM", "severity": "HIGH",
           "sentiment": +0.8, "source": "Bloomberg", "ts": "..."}
        ]
      },
      "ETH": {
        "score_1h": -0.05,
        "score_4h": 0.10,
        "score_24h": 0.18,
        "trending_direction": "neutral"
      }
    },
    "active_alerts": [
      {
        "level": "HIGH",
        "asset": "BTC",
        "category": "INSTITUTIONAL_FLOW",
        "narrative": "BlackRock IBIT $50B AUM, multiple sources confirm",
        "ts": "..."
      }
    ]
  }
}
```

### scratchpad.news_alerts (CRITICAL events, append-only rolling 7gg)
```json
{
  "news_alerts": [
    {
      "ts": "2026-05-01T13:42:00Z",
      "severity": "CRITICAL",
      "category": "EXCHANGE_HALT",
      "asset": "BTC",
      "title": "Binance pauses BTC withdrawals due to maintenance",
      "source": "Binance Official",
      "url": "https://...",
      "action_taken": "kill_switch_triggered",
      "kill_switch_id": "uuid-...",
      "resumed_at": "2026-05-01T14:30:00Z",
      "duration_minutes": 48
    }
  ]
}
```

---

## Cross-reference con altre skill

```
LETTA DA QUESTA SKILL:
  scratchpad.active_positions    (per filtrare news rilevanti)
  context.macro_regime           (sentiment magnifies regime)
  External: CryptoPanic API

PUSH A:
  composite-risk-gate            (CRITICAL events -> immediate kill switch)
  jarvis-main agent              (notify + display in UI)

LETTO DA:
  composite-risk-gate            (CRITICAL category -> trigger #4)
  gex-analysis                   (sentiment modifier in PASSO 3)
  scalp-execution                (filter 9: news cluster contrarian -> downgrade)
  proactive-scout                (news positivo aumenta score)
  macro-regime-monitor           (sentiment cluster contribuisce a regime change)
  narrative-rotation-monitor     (news per identificare narrative emergent)

SCRIVE:
  context.news_signal            (rolling 30min refresh)
  scratchpad.news_alerts         (CRITICAL events log, 7gg)
  retrospettive.md               (post-mortem CRITICAL events: cosa successo, latenza alert, false positive?)
```

---

## Errori da evitare

```
Trattare ogni news come tradabile:
  HFT vince sempre la news race. Non è "trade the news", è "don't be blind".

Sentiment score senza source weighting:
  Tweet random vs Bloomberg headline non vanno pesati uguali.
  Source whitelist + weighting essential.

Keyword matching naive:
  "Binance hack" potrebbe essere CTF, satira, vecchio articolo.
  Sempre verificare published_at recente + multiple source.

False positive su title clickbait:
  "BTC will CRASH 90%!" è LOW (opinion), non CRITICAL.
  CRITICAL richiede source trusted + asset impact reale.

Skip dedup:
  CryptoPanic spesso aggrega multiple posting dello stesso evento.
  Hash title (lowercase, no punctuation) + check 24h history.

Auto-resume kill switch da news:
  Una volta che CRITICAL news triggers kill, l'auto-resume richiede
  cooldown 2h MINIMO + verifica che situazione "contained".
  No auto-resume aggressivo.

NLP sofisticato senza necessità:
  Per CRITICAL detection, keyword-based è sufficient e affidabile.
  NLP per LLM-grade sentiment può aspettare upgrade futuro.
```

---

## Threshold operativi

```
CRYPTOPANIC FETCH:
  rate_limit_per_min: 5 (free tier safe)
  cron_interval_min: 5
  posts_per_fetch: 50

SEVERITY THRESHOLDS:
  critical_keywords_match: 1+ critical word + trusted source
  high_keywords_match: 1+ bull/bear word + source trusted
  source_trusted_list: ["CoinDesk", "Bloomberg", "Reuters", "The Block",
                        "Binance", "Coinbase", "Fidelity", "BlackRock", ...]

SENTIMENT SCORING:
  weight_1h: 0.6
  weight_4h: 0.3
  weight_24h: 0.1
  cluster_threshold: 3 same-direction HIGH news in 1h
  sustained_threshold: sentiment_4h abs > 0.5 for 4h+
```
