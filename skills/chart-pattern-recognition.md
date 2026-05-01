---
name: chart-pattern-recognition
description: >
  Riconoscimento professionale di pattern candlestick e chart pattern su grafici
  a timeframe multipli (15m, 1h, 4h, 1D). Usa questa skill ogni volta che l'agent
  riceve uno screenshot di un grafico e deve identificare pattern, oppure quando
  analizza price action per trovare setup tecnici.
  Trigger: "riconosci il pattern", "cosa vedo sul grafico", "analizza le candele",
  "c'e un pattern?", "identifica la formazione", "leggi la price action",
  "hammer", "doji", "engulfing", "testa e spalle", "flag", "wedge", "triangolo",
  "double top", "morning star", "analisi tecnica", "candlestick pattern",
  "chart pattern", "price action setup", "pattern di inversione", "pattern di continuazione".
  Attiva automaticamente quando scalp-execution richiede identificazione pattern
  per confermare un setup. Output: nome pattern + validita + implicazione + entry/stop logici.
---

# Chart Pattern Recognition Skill

## Filosofia professionale: pattern come CONTESTO, non come segnali

La regola d'oro del professionista:

```
I pattern NON predicono il futuro.
I pattern descrivono la PSICOLOGIA del momento e aumentano la probabilita
di un certo esito SOLO quando compaiono nel contesto giusto.

Un Hammer in mezzo al range non significa nulla.
Un Hammer su un supporto GEX str > 8 dopo un flush di long = setup ad alto edge.

Regola: MAI tradare un pattern isolato. SEMPRE valutare:
  1. Dove si forma? (su quale livello strutturale)
  2. In quale trend si inserisce? (timeframe superiore)
  3. Il volume conferma? (partecipazione reale)
  4. C'e confluenza con GEX / LW / VP? (struttura sottostante)
```

---

## Come leggere una candela — anatomia base

```
        |  <- Wick superiore (High)
       [=]  <- Corpo (Open-Close)
        |  <- Wick inferiore (Low)

Candela BULLISH (teal/verde): Close > Open
  Il corpo va da Open (basso) a Close (alto)
  I compratori hanno vinto la sessione

Candela BEARISH (rossa): Close < Open
  Il corpo va da Open (alto) a Close (basso)
  I venditori hanno vinto la sessione

CORPO LUNGO:  momentum forte nella direzione della chiusura
CORPO CORTO:  indecisione, equilibrio compratori/venditori
WICK LUNGO:   rifiuto del prezzo a quei livelli estremi
WICK CORTO:   poca resistenza nella direzione del movimento
```

---

## Caricamento riferimenti

Questa skill usa quattro file di riferimento. Caricali in base alla situazione:

```
CANDLESTICK PATTERNS (1-3 candele):
  -> Leggi: references/candlestick-patterns.md
  Quando: identifichi formazioni su 1, 2 o 3 candele
  Contiene: 30+ pattern con condizioni, validita, implicazioni, affidabilita

CHART PATTERNS (geometria multi-candela):
  -> Leggi: references/chart-patterns.md
  Quando: vedi struttura geometrica su piu candele (flag, triangolo, H&S...)
  Contiene: inversione, continuazione, bilaterali — ratios, target, failure modes

PATTERN ARMONICI (Gartley, Bat, Butterfly, Crab):
  -> Leggi: references/harmonic-patterns.md
  Quando: vedi struttura XABCD con 5 swing point su 1h/4h/1D
  Contiene: tutti i ratio Fibonacci esatti, PRZ, entry/stop/target, errori comuni

STOCHRSI + VOLUME (integrazione per ogni pattern):
  -> Leggi: references/stochrsi-volume-integration.md
  Quando: SEMPRE — dopo aver identificato qualsiasi pattern
  Contiene: come leggere StochRSI e volume per ogni categoria di pattern,
            score system 0-6, tabella di riferimento rapido
```

FIBONACCI (retracement, extension, S/R standalone):
  -> Leggi: references/fibonacci-analysis.md
  Quando: vedi un grafico fibonacci_analysis.png con livelli disegnati,
          oppure devi calcolare target di prezzo o PRZ di pattern armonici,
          oppure vuoi usare Fibonacci come supporti/resistenze standalone
  Contiene: come leggere ogni livello, strategie operative per ogni zona,
            come si integra con i pattern armonici, cluster Fibonacci,
            output standardizzato per fibonacci_analysis.png

RELAZIONE TRA I REFERENCE:
  fibonacci-analysis.md  →  dice DOVE sono i livelli e cosa significano
  harmonic-patterns.md   →  dice COME si chiamano le strutture XABCD su quei livelli
  stochrsi-volume        →  dice QUANDO entrare nei livelli identificati

Workflow: identifica il pattern -> carica il reference specifico ->
carica SEMPRE stochrsi-volume-integration.md -> calcola score 0-6 -> output.

Per analisi fibonacci_analysis.png: carica fibonacci-analysis.md +
stochrsi-volume-integration.md + (harmonic-patterns.md se vedi struttura XABCD).

---

## Framework di analisi in 5 passi

### PASSO 1 — Classifica il trend di sfondo (timeframe superiore)

```
Prima di identificare qualsiasi pattern, stabilisci il trend sul TF superiore:

UPTREND:
  Higher Highs + Higher Lows
  Prezzo sopra MA50 e MA21
  -> Pattern BULLISH hanno edge piu alto
  -> Pattern BEARISH richiedono conferma extra

DOWNTREND:
  Lower Highs + Lower Lows
  Prezzo sotto MA50 e MA21
  -> Pattern BEARISH hanno edge piu alto
  -> Pattern BULLISH richiedono conferma extra (potrebbero essere rimbalzi)

LATERALE (range):
  Prezzo oscilla tra supporto e resistenza senza direzionalita
  -> Pattern DI INVERSIONE ai bordi del range hanno alto edge
  -> Pattern DI CONTINUAZIONE nel mezzo del range sono rumore

REGOLA: un pattern contro-trend vale meta. Un pattern in-trend vale doppio.
```

### PASSO 2 — Identifica il livello strutturale

```
Il pattern deve formarsi SU un livello significativo per avere edge:

LIVELLI VALIDI (in ordine di importanza):
  1. Livello GEX str > 7 (da confluence_history)
  2. POC o VAH/VAL del Volume Profile
  3. Supporto/resistenza storico (minimo/massimo precedente significativo)
  4. Trendline principale (almeno 3 tocchi)
  5. Livello psicologico (numero tondo: 70,000 / 69,000 ecc.)

PATTERN SU LIVELLO FORTE: edge alto, setup tradeable
PATTERN SENZA LIVELLO:    rumore, non tradare
```

### PASSO 3 — Identifica il pattern (carica il file di riferimento)

```
Segui questo albero di decisione:

QUANTE CANDELE FORMA IL PATTERN?
  1 candela  -> Hammer, Doji, Shooting Star, Marubozu, Spinning Top
  2 candele  -> Engulfing, Harami, Tweezer, Piercing, Dark Cloud
  3 candele  -> Morning/Evening Star, Three Soldiers/Crows, Three Inside
  Molte      -> Chart Pattern (Head&Shoulders, Triangle, Flag, Wedge...)

Carica references/candlestick-patterns.md per i primi tre casi.
Carica references/chart-patterns.md per il quarto caso.
```

### PASSO 4 — Verifica la validita del pattern

```
CRITERI DI VALIDAZIONE UNIVERSALI:

[ ] Il pattern e COMPLETO? (tutte le candele si sono chiuse)
    -> Mai tradare su una candela ancora aperta
    -> Aspetta la chiusura della candela di conferma

[ ] Il volume SUPPORTA il pattern?
    -> Pattern di inversione: volume alto nella candela di inversione
    -> Pattern di continuazione: volume basso nella fase di consolidamento,
       poi spike nel breakout
    -> Volume basso su un pattern di inversione = segnale debole

[ ] Il pattern e in confluenza con la struttura?
    -> Si forma su un livello GEX / VP / strutturale? (vedi Passo 2)

[ ] Il contesto di trend e favorevole?
    -> Pattern bullish in downtrend forte = bassa probabilita
    -> Pattern bearish in uptrend forte = bassa probabilita

SCORE DI VALIDITA:
  4/4 criteri = pattern FORTE, edge alto
  3/4 criteri = pattern VALIDO, edge accettabile
  2/4 criteri = pattern DEBOLE, solo con altre confluenze
  1/4 criteri = NON tradare
```

### PASSO 5 — Calcola entry, target e stop logici

```
ENTRY:
  Candlestick pattern: entry all'apertura della candela SUCCESSIVA
                       alla candela di segnale (dopo la chiusura di conferma)
  Chart pattern:       entry alla ROTTURA del livello chiave del pattern
                       (neckline, bordo del triangolo, bordo del flag)
  Regola: MAI anticipare. Aspetta sempre la chiusura di conferma.

TARGET (metodo misurato):
  Candlestick: target = dimensione del pattern (altezza del corpo/wick)
               proiettata nella direzione del segnale
  Chart pattern: target = altezza del pattern proiettata dal punto di breakout
  Regola pratica: usa il prossimo livello GEX o strutturale come target
                  se piu vicino del target misurato

STOP LOGICO:
  Bullish pattern: stop SOTTO il minimo del pattern (o del wick inferiore)
  Bearish pattern: stop SOPRA il massimo del pattern (o del wick superiore)
  Regola: se lo stop e troppo lontano (> 2%) -> pattern non tradeable ora,
          aspetta un'entry migliore o usa size ridotta
```

---

## Regole di lettura per timeframe

```
15 MINUTI:
  Uso: scalp e entry di precisione
  Affidabilita pattern: BASSA (molto rumore)
  Regola: usare solo in confluenza con segnale su 1h o 4h
  Pattern piu affidabili: Engulfing, Hammer, Shooting Star su livelli forti
  Pattern da evitare: strutture complesse (HS, triangoli) — troppo lente

1 ORA:
  Uso: scalp esteso e swing entry
  Affidabilita pattern: MEDIA-ALTA
  Regola: timeframe primario per la maggior parte dei setup
  Pattern piu affidabili: tutti i candlestick, Flag, Wedge
  Nota: StochRSI su 1h e il piu usato per timing

4 ORE:
  Uso: swing trade e definizione struttura
  Affidabilita pattern: ALTA
  Regola: usa il 4h per capire la struttura, poi scendi a 1h per l'entry
  Pattern piu affidabili: Head & Shoulders, Double Top/Bottom, Triangoli
  Nota: i pattern su 4h richiedono piu tempo per completarsi ma sono piu affidabili

1 GIORNO:
  Uso: bias direzionale e punti di svolta strutturali
  Affidabilita pattern: MOLTO ALTA
  Regola: non tradare sul giornaliero, usarlo per capire il bias della settimana
  Pattern piu affidabili: tutti, con focus su pattern di inversione maggiori
  Nota: un Evening Star sul daily vale 10 Shooting Star sul 15m

REGOLA MULTI-TIMEFRAME:
  Daily  = trend di fondo (non si combatte)
  4h     = struttura della settimana
  1h     = trend della sessione
  15m    = entry di precisione
  
  Entry ideale: pattern su 1h allineato con bias 4h allineato con trend daily
```

---

## Tabella rapida di riconoscimento

```
PATTERN          | TF PRIMARIO | TIPO       | SEGNALE  | AFFIDABILITA
-----------------|-------------|------------|----------|-------------
Hammer           | 1h/4h       | Candlestick| Bullish  | Media-Alta
Shooting Star    | 1h/4h       | Candlestick| Bearish  | Media-Alta
Doji             | qualsiasi   | Candlestick| Neutro   | Bassa (da sola)
Engulfing Bull   | 1h/4h       | Candlestick| Bullish  | Alta
Engulfing Bear   | 1h/4h       | Candlestick| Bearish  | Alta
Morning Star     | 4h/1D       | Candlestick| Bullish  | Molto Alta
Evening Star     | 4h/1D       | Candlestick| Bearish  | Molto Alta
3 White Soldiers | 4h/1D       | Candlestick| Bullish  | Alta
3 Black Crows    | 4h/1D       | Candlestick| Bearish  | Alta
Head & Shoulders | 4h/1D       | Chart      | Bearish  | Molto Alta (76%)
Inv H&S          | 4h/1D       | Chart      | Bullish  | Molto Alta
Double Top       | 4h/1D       | Chart      | Bearish  | Alta
Double Bottom    | 4h/1D       | Chart      | Bullish  | Alta
Bull Flag        | 1h/4h       | Chart      | Bullish  | Alta (>80%)
Bear Flag        | 1h/4h       | Chart      | Bearish  | Alta
Bull Pennant     | 1h/4h       | Chart      | Bullish  | Alta (67-71%)
Asc. Triangle    | 4h/1D       | Chart      | Bullish  | Alta
Desc. Triangle   | 4h/1D       | Chart      | Bearish  | Alta
Symm. Triangle   | qualsiasi   | Chart      | Bilat.   | Media (70%)
Rising Wedge     | 1h/4h       | Chart      | Bearish  | Alta (70%)
Falling Wedge    | 1h/4h       | Chart      | Bullish  | Alta (70%)
Cup & Handle     | 4h/1D       | Chart      | Bullish  | Molto Alta (80%)
```

---

## Output standardizzato

```
=== PATTERN RECOGNITION — [Asset] @ $[prezzo] | [TF] | [ora] ===

TREND DI SFONDO ([TF superiore]):
  Bias:          [UPTREND / DOWNTREND / LATERALE]
  MA posizione:  [prezzo sopra/sotto MA21 e MA50]

LIVELLO STRUTTURALE:
  Tipo:          [GEX str X / POC / VAH-VAL / resistenza storica / trendline]
  Prezzo:        $[X]
  Rilevanza:     [alta/media/bassa]

PATTERN IDENTIFICATO:
  Nome:          [nome ufficiale]
  Tipo:          [CANDLESTICK (N candele) / CHART PATTERN]
  Categoria:     [INVERSIONE BULLISH / INVERSIONE BEARISH /
                  CONTINUAZIONE BULLISH / CONTINUAZIONE BEARISH / BILATERALE]
  Timeframe:     [TF su cui si forma]
  Stato:         [COMPLETO / IN FORMAZIONE (non tradare)]

VALIDAZIONE:
  Completezza:   [SI/NO]
  Volume:        [conferma / non conferma / non disponibile]
  Livello:       [su livello valido SI/NO]
  Trend:         [allineato / contro-trend]
  Score:         [N/4] -> [FORTE / VALIDO / DEBOLE / NON TRADARE]

PSICOLOGIA DEL PATTERN:
  [2-3 righe: cosa sta succedendo tra compratori e venditori]

SETUP OPERATIVO:
  Entry:         $[X] — condizione: [chiusura candela / breakout livello]
  Target:        $[X] — [metodo misurato / livello GEX str X]
  Stop logico:   $[X] — [sotto/sopra livello strutturale]
  R/R stimato:   [N:1]
  Timeout:       [pattern decade se non si attiva entro X candele]

SEGNALI DI INVALIDAZIONE:
  [cosa renderebbe il pattern falso prima dello stop]

INTEGRAZIONE GEX/VP:
  [come questo pattern si combina con la struttura GEX e volume profile]
```

---

## Errori comuni da evitare

```
Tradare un pattern su candela ancora aperta:
  La candela puo ancora cambiare aspetto. Aspetta la chiusura.

Tradare contro il trend del TF superiore:
  Un Hammer in downtrend forte e un rimbalzo tecnico, non un'inversione.
  Richiedere due conferme extra prima di entrare contro il trend.

Ignorare il volume:
  Un Engulfing senza volume e rumore. Con volume e segnale.

Pattern valido ma nel posto sbagliato:
  Un Morning Star nel mezzo del range non vale nulla.
  Lo stesso Morning Star su supporto GEX str 9 = setup eccellente.

Cercare pattern troppo "perfetti":
  I mercati reali producono pattern imperfetti. La psicologia conta,
  non la forma geometrica esatta. Un Hammer con corpo leggermente
  piu grande del "manuale" e ancora un Hammer se il contesto e giusto.

Pattern di inversione come segnali di timing assoluto:
  Un Evening Star non dice che il mercato crolla domani.
  Dice che la pressione rialzista si sta esaurendo in quel punto.
  Il trend puo continuare ancora 2-3 candele prima dell'inversione.
```

---

## Cross-reference con le altre skill

```
CHIAMATA DA:
  scalp-execution        (per conferma pattern visivo del setup)
  gex-analysis           (PASSO 2 lettura tecnica integrata)
  derivatives-dashboard  (interpretazione candle in zona DIVERGENCE)

CARICA REFERENCE (relative path, dentro skills/references/):
  references/candlestick-patterns.md       (1-3 candele)
  references/chart-patterns.md             (geometria multi-candela)
  references/harmonic-patterns.md          (XABCD Fibonacci ratios)
  references/fibonacci-analysis.md         (livelli, extension, S/R)
  references/stochrsi-volume-integration.md (SEMPRE — filtro qualità)

LETTA DA QUESTA SKILL (modifier contestuale):
  context.macro_regime          <- pattern bullish in EUPHORIA = edge ridotto
  calibration.asset_thresholds  <- references/calibration-thresholds.md
                                    (StochRSI 75/25 -> p85/p15 calibrati)

NOTA: i pattern hanno affidabilità storica documentata nella tabella.
      Quei valori (es. H&S 76%, Bull Flag >80%) sono medi storici da
      letteratura, NON calibrati per asset specifico — usali come ordine
      di grandezza, non come probabilità esatta del trade.
```
