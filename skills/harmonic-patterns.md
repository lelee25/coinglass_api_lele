# Harmonic Patterns Reference
## Fonte: H.M. Gartley (1935), Scott Carney (1999-2010), Larry Pesavento

---

## Fondamenta: cosa sono i pattern armonici

I pattern armonici sono strutture geometriche di prezzo basate su rapporti di
Fibonacci **precisi e misurabili**. Non sono pattern "a occhio" — richiedono
la verifica matematica di ogni gamba tramite il tool Fibonacci di TradingView.

```
DIFFERENZA FONDAMENTALE DAI PATTERN CLASSICI:
  Pattern classici (H&S, Flag...): riconoscimento visivo, soglie flessibili
  Pattern armonici:                 matematica Fibonacci obbligatoria,
                                    tolleranza ±3-5% sui ratio, non di più

PERCHE FUNZIONANO (tre motivi):
  1. I mercati si muovono in rapporti Fibonacci — comportamento ricorrente
  2. Molti trader li seguono — effetto self-fulfilling prophecy
  3. Convergenza di multiple proiezioni Fib nello stesso punto (PRZ)
     = alta concentrazione di ordini in quella zona

PRZ = Potential Reversal Zone:
  La zona dove tutte le misurazioni Fibonacci del pattern convergono.
  Non è un punto esatto — è una zona (solitamente 0.5-1.5% di ampiezza).
  Il prezzo entra nel PRZ, mostra segnali di inversione, poi si inverte.
  NON entrare anticipando il PRZ — aspettare il segnale di inversione dentro il PRZ.
```

---

## Struttura base: XABCD

Tutti i pattern armonici a 5 punti seguono la stessa struttura:

```
X ──── A  (XA: impulso iniziale — gamba di partenza)
         \
          B  (AB: ritracciamento di XA)
         /
        C   (BC: rimbalzo di AB)
         \
          D  (CD: gamba finale che completa il pattern — zona di ingresso PRZ)

REGOLE UNIVERSALI:
  - X è il punto di origine
  - A è il primo swing significativo
  - B è un ritracciamento di XA (percentuale specifica per ogni pattern)
  - C è un ritracciamento di AB (percentuale specifica)
  - D è il completamento del pattern (PRZ) — zona di INGRESSO

FORMA VISIVA:
  Bullish pattern (inversione rialzista): forma a "W" o "M" con D in basso
  Bearish pattern (inversione ribassista): forma a "M" con D in alto

ENTRY: sempre a D (dopo conferma nel PRZ)
STOP: oltre X (con tolleranza del 3-5%)
TARGET 1: punto C
TARGET 2: punto A
TARGET 3: 161.8% / 261.8% di XA (estensioni Fibonacci)
```

---

## AB=CD — Il pattern base (fondamento di tutti gli altri)

```
STRUTTURA (4 punti: A, B, C, D):
  AB = CD in lunghezza (idealmente)
  BC: ritracciamento di AB tra 0.618 e 0.786
  CD: estensione di BC tra 1.272 e 1.618

FIBONACCI RATIOS:
  BC = 0.618 retracement di AB → CD = 1.618 di BC (classico)
  BC = 0.786 retracement di AB → CD = 1.272 di BC (alternativo)

FORMA VISIVA:
  Due gambe quasi identiche separate da un ritracciamento.
  Sembra una "N" (bearish) o "N invertita" (bullish).

PSICOLOGIA:
  Il mercato fa un impulso, si corregge proporzionalmente,
  poi fa un secondo impulso della stessa ampiezza del primo.
  La simmetria indica un punto di esaurimento probabile.

PRZ: punto D (dove AB = CD)
ENTRY: D con segnale di inversione candlestick
STOP: oltre D di un importo pari al 13-20% di CD
TARGET 1: 61.8% di CD
TARGET 2: inizio di CD (punto C)
AFFIDABILITA: Media-Alta (pattern base — fondamento degli altri)
NOTA: è embedato in tutti i pattern XABCD come gamba CD
```

---

## Gartley "222" — Il Pattern Originale

**Fonte: H.M. Gartley, "Profits in the Stock Market" (1935), pag. 222**

```
STRUTTURA (5 punti: X, A, B, C, D):
  XA: impulso iniziale (rialzista per bullish, ribassista per bearish)
  AB: B ritraccia XA del 61.8% (ratio critico, tolleranza ±3%)
  BC: C ritraccia AB tra 38.2% e 88.6%
  CD: D è al 78.6% retracement di XA (ratio chiave del Gartley)
  CD deve essere 1.272 o 1.618 di BC (dipende da BC)

FIBONACCI RATIOS ESATTI:
  AB  = 0.618 di XA                    ← OBBLIGATORIO (±3%)
  BC  = 0.382 a 0.886 di AB
  CD  = 1.272 di BC (se BC = 0.382)
       o 1.618 di BC (se BC = 0.886)
  D   = 0.786 retracement di XA        ← RATIO CHIAVE

FORMA VISIVA:
  Bullish Gartley: sembra una "W" con D sopra il minimo di X
  Bearish Gartley: sembra una "M" con D sotto il massimo di X
  D NON supera X (questo distingue il Gartley dal Butterfly)

PSICOLOGIA:
  È il pattern di correzione perfetta di un trend.
  Il mercato ritraccia in maniera ordinata e si riposiziona per continuare.
  Il punto D (78.6% di XA) è una zona di supporto/resistenza molto rispettata
  perché rappresenta una correzione profonda ma non inversione.

PRZ: intorno al punto D (0.786 di XA ± 1%)
ENTRY: D + segnale candlestick di inversione (Hammer, Engulfing, Doji)
STOP: appena sotto X (bullish) / appena sopra X (bearish)
TARGET 1: punto B (61.8% del pattern)
TARGET 2: punto A
TARGET 3: 161.8% di XA proiettato da D
CONTESTO: tipicamente in trend esistente (correzione ordinata)
AFFIDABILITA: Alta — uno dei pattern armonici più affidabili
TIMEFRAME: funziona su tutti i TF, migliore su 1h/4h/1D
```

---

## Bat Pattern — Alta Precisione, Tight Stop

**Fonte: Scott Carney, "The Harmonic Trader" (1999)**

```
STRUTTURA (5 punti: X, A, B, C, D):
  XA: impulso iniziale
  AB: B ritraccia XA tra 38.2% e 50.0% (NON deve superare 61.8%)
  BC: C ritraccia AB tra 38.2% e 88.6%
  CD: D è all'88.6% retracement di XA (ratio chiave del Bat)

FIBONACCI RATIOS ESATTI:
  AB  = 0.382 a 0.500 di XA             ← CHIAVE: B non supera 0.618 di XA
  BC  = 0.382 a 0.886 di AB
  CD  = 1.618 a 2.618 di BC
  D   = 0.886 retracement di XA         ← RATIO CHIAVE (più profondo del Gartley)

DIFFERENZA DAL GARTLEY:
  Bat: D è all'88.6% di XA (più profondo)
  Gartley: D è al 78.6% di XA (meno profondo)
  Bat: AB è max 50% di XA (più corto)
  Gartley: AB è esattamente 61.8% di XA

FORMA VISIVA:
  Simile al Gartley ma con D più vicino a X.
  Il ritracciamento di AB è più corto (B meno profondo).

PSICOLOGIA:
  Ritracciamento molto profondo (88.6%) = zona di massimo stress del trend.
  I compratori/venditori difendono questo livello con forza.
  Il vantaggio principale: stop molto stretto (appena oltre X), R/R ottimo.

PRZ: intorno al punto D (0.886 di XA ± 1%)
ENTRY: D + segnale candlestick
STOP: appena oltre X (il Bat ha lo stop più stretto tra i 4 pattern principali)
TARGET 1: punto C
TARGET 2: punto A
TARGET 3: 161.8% di XA da D
VANTAGGIO: R/R teorico molto favorevole grazie allo stop stretto
AFFIDABILITA: Alta — Carney lo descrive come molto affidabile
```

---

## Butterfly Pattern — Estensione Oltre X

**Fonte: Bryce Gilmore, perfezionato da Scott Carney**

```
STRUTTURA (5 punti: X, A, B, C, D):
  XA: impulso iniziale
  AB: B ritraccia XA del 78.6%
  BC: C ritraccia AB tra 38.2% e 88.6%
  CD: D è al 127.2% o 161.8% ESTENSIONE di XA
      → D VA OLTRE X (questo è il tratto distintivo del Butterfly)

FIBONACCI RATIOS ESATTI:
  AB  = 0.786 di XA                     ← RATIO CHIAVE (profondo)
  BC  = 0.382 a 0.886 di AB
  CD  = 1.618 a 2.618 di BC
  D   = 1.272 o 1.618 estensione di XA  ← CHIAVE: D OLTRE X

DIFFERENZA FONDAMENTALE DAL GARTLEY E BAT:
  Gartley e Bat: D è DENTRO il range XA (D non supera X)
  Butterfly:     D è OLTRE X (estensione, non ritracciamento)

FORMA VISIVA:
  Bullish Butterfly: D è sotto il minimo di X (nuovo minimo)
  Bearish Butterfly: D è sopra il massimo di X (nuovo massimo)
  Ha la forma di una "W" allargata (bullish) o "M" allargata (bearish)

PSICOLOGIA:
  Il prezzo fa un nuovo estremo oltre il punto di partenza.
  Questo "overshoot" cattura tutti i trader che seguono il trend
  (breakout falso), poi inverte violentemente.
  È un pattern di exhaustion — il mercato si è spinto troppo in là.

PRZ: intorno al punto D (1.272 o 1.618 di XA ± 1.5%)
ENTRY: D + segnale forte di inversione (il rimbalzo sarà violento)
STOP: 15-20% oltre D nella direzione del pattern
TARGET 1: 61.8% del CD leg
TARGET 2: punto B
TARGET 3: punto A
NOTA: il rimbalzo dal PRZ del Butterfly è spesso molto rapido e ampio
      — può dare R/R eccellenti ma richiede timing preciso
AFFIDABILITA: Alta — soprattutto su 4h/1D
```

---

## Crab Pattern — Il Più Estremo, Massima Precisione

**Fonte: Scott Carney (2000) — "il pattern armonico più preciso"**

```
STRUTTURA (5 punti: X, A, B, C, D):
  XA: impulso iniziale
  AB: B ritraccia XA tra 38.2% e 61.8%
  BC: C ritraccia AB tra 38.2% e 88.6%
  CD: D è al 161.8% ESTENSIONE di XA (la CD è lunga — molto oltre X)

FIBONACCI RATIOS ESATTI:
  AB  = 0.382 a 0.618 di XA
  BC  = 0.382 a 0.886 di AB
  CD  = 2.618 a 3.618 di BC (CD molto lunga)
  D   = 1.618 estensione di XA           ← RATIO CHIAVE (più estremo di tutti)

DIFFERENZA DAL BUTTERFLY:
  Butterfly: D a 1.272 o 1.618 di XA
  Crab:      D a 1.618 di XA (più estremo — CD è più lunga)
  Entrambi hanno D oltre X, ma il Crab va più lontano

FORMA VISIVA:
  La gamba CD è molto lunga rispetto al resto del pattern.
  Visivamente sembra "squilibrato" — la coda (CD) è sproporzionata.

PSICOLOGIA:
  Il prezzo si spinge all'estremo assoluto di un movimento.
  La zona D al 161.8% di XA è un punto di massimo squilibrio.
  Carney afferma che questo è il punto di inversione più preciso
  tra tutti i pattern armonici — quando il PRZ viene raggiunto
  con i ratio corretti, la inversione è quasi meccanica.

PRZ: punto D (1.618 di XA ± 0.5% — tolleranza molto bassa)
ENTRY: D + qualsiasi segnale di inversione candlestick
STOP: 5-10% oltre D (lo stop è più ampio perché la zona è estrema)
TARGET 1: 38.2% di CD
TARGET 2: 61.8% di CD
TARGET 3: punto C
NOTA CRITICA: la precisione Fibonacci deve essere massima.
              Un Crab con ratios "approssimativi" non è un Crab valido.
AFFIDABILITA: Molto Alta quando i ratio sono rispettati (Carney: "il più preciso")
```

---

## Shark Pattern — Il Più Recente

**Fonte: Scott Carney, "Harmonic Trading Vol. 3" (2010)**

```
STRUTTURA: usa punti O, X, A, B, C (nomenclatura diversa)
  OX: impulso iniziale
  XA: B ritraccia tra 113% e 161.8% di OX
  AB: C ritraccia tra 113% e 161.8% di XA
  BC: D è al 88.6% di OX

FIBONACCI RATIOS:
  XA: 113% a 161.8% di OX
  AB: B deve essere tra 113% e 161.8% di XA (BC inverso)
  D  = 88.6% di OX (simile al Bat nel ritracciamento)

FORMA VISIVA: più irregolare degli altri — "dente di squalo"
AFFIDABILITA: Media-Alta (più recente, meno dati storici)
```

---

## Cypher Pattern — Pattern Alternativo

**Fonte: Darren Oglesbee**

```
FIBONACCI RATIOS:
  AB  = 0.382 a 0.618 di XA
  BC  = 1.130 a 1.414 di XA (BC supera A — estensione)
  CD  = 78.6% del range XC (non XA — differenza importante)
  D   = 0.786 retracement di XC

FORMA VISIVA: simile al Butterfly ma con BC che supera il punto A
AFFIDABILITA: Alta quando identificato correttamente
```

---

## Come identificare e validare un pattern armonico

### Step 1 — Identifica i 5 swing point (X, A, B, C, D)

```
COSA CERCARE:
  Cerca strutture a "M" o "W" su grafici 1h, 4h o 1D
  Ogni punto deve essere un swing significativo (almeno 2-3 candele di reazione)
  
SUL GRAFICO TRADINGVIEW:
  Usa il Fibonacci Retracement tool su XA per trovare i livelli chiave
  Misura AB come % di XA → confronta con i ratio del pattern
  Misura BC come % di AB
  Calcola dove D dovrebbe essere (PRZ)
```

### Step 2 — Verifica i ratio Fibonacci

```
TOLLERANZE AMMESSE:
  Gartley:   ±3% sui ratio chiave
  Bat:       ±3%
  Butterfly: ±3-5% (D può avere tolleranza leggermente maggiore)
  Crab:      ±1-2% (il più preciso — quasi zero tolleranza)

COME VERIFICARE SU TRADINGVIEW:
  1. Fibonacci Retracement da X ad A → guarda dove cade B (deve essere al 61.8% per Gartley)
  2. Fibonacci Retracement da A a B → guarda dove cade C (38.2% - 88.6%)
  3. Proietta CD: Extension tool da X ad A → guarda dove proietta D

SE I RATIO NON CORRISPONDONO: il pattern NON è valido, non tradare
```

### Step 3 — Aspetta il PRZ e il segnale di inversione

```
REGOLA CRITICA: non entrare prima che il prezzo raggiunga il PRZ

NEL PRZ CERCA:
  Candlestick di inversione (Hammer, Engulfing, Morning Star, Doji)
  Divergenza RSI/StochRSI (vedi references/stochrsi-volume-integration.md)
  Volume che aumenta nel PRZ (interesse in quella zona)
  Livello GEX o VP che coincide con il PRZ (massima confluenza)

SE IL PREZZO ATTRAVERSA IL PRZ SENZA RIMBALZARE:
  Il pattern è invalidato se D supera X (per Gartley e Bat)
  Per Butterfly e Crab: rivedere i ratio — potrebbe essere un pattern diverso
```

---

## Integrazione con la struttura GEX/VP

```
MASSIMA CONFLUENZA (setup premium):
  PRZ del pattern armonico coincide con:
  - Livello GEX str > 8 (da confluence_history)
  - POC o VAH/VAL del Volume Profile
  - Supporto/resistenza storico significativo
  
  In questo caso: tre sistemi diversi segnalano lo stesso prezzo
  → probabilità di inversione molto alta

MEDIA CONFLUENZA (setup valido):
  PRZ coincide con uno dei livelli sopra

BASSA CONFLUENZA (evitare):
  PRZ in zona vuota senza livelli strutturali
  → anche con ratio Fibonacci perfetti, l'edge è inferiore
```

---

## Tabella riassuntiva ratios

```
PATTERN   | AB di XA      | D di XA           | D vs X
----------|---------------|-------------------|------------------
Gartley   | 0.618         | 0.786 retrac.     | D dentro XA
Bat       | 0.382-0.500   | 0.886 retrac.     | D dentro XA (vicino X)
Butterfly | 0.786         | 1.272-1.618 ext.  | D OLTRE X
Crab      | 0.382-0.618   | 1.618 extension   | D MOLTO OLTRE X
Cypher    | 0.382-0.618   | 0.786 di XC       | variabile

STOP LOSS posizionamento:
  Gartley/Bat:       appena oltre X
  Butterfly/Crab:    13-20% oltre D

TARGET sequenza:
  T1: punto C (o 38.2% di CD)
  T2: punto A
  T3: 161.8% di XA proiettato da D
```

---

## Errori più comuni con i pattern armonici

```
FORZARE I RATIO:
  "Quasi 61.8%" non è 61.8%. Se AB è al 55% di XA non è un Gartley.
  I ratio devono essere rispettati. Senza precisione non c'è pattern.

ANTICIPARE IL PRZ:
  Entrare prima che D sia raggiunto. Il prezzo può estendersi ancora.
  Regola: aspettare che il PRZ sia toccato + segnale candlestick.

IGNORARE L'INVALIDAZIONE:
  Se il prezzo supera X in un Gartley o Bat, il pattern è invalidato.
  Uscire immediatamente. Non "sperare" in un ritorno.

NON VERIFICARE I RATIO DI AB:
  Il Bat ha AB max al 50%, il Gartley esattamente al 61.8%.
  Un pattern con AB al 70% non è ne Bat ne Gartley.

USARE SU TIMEFRAME TROPPO BASSI:
  Su 5m e 15m i pattern armonici hanno alta percentuale di falsi segnali.
  Timeframe ideale: 1h minimo, meglio 4h e 1D.
```

---

## Affidabilità statistica documentata

```
Gartley:    ~65-70% win rate quando ratio corretti + conferma candlestick
Bat:        ~70-75% (Carney: il più affidabile per R/R)
Butterfly:  ~65% (rimbalzi violenti ma meno frequenti)
Crab:       ~70-75% (quando ratio rispettati al massimo)
AB=CD:      ~60-65% (il più comune, meno preciso)

NOTA: queste statistiche assumono:
  1. Ratio Fibonacci rispettati (tolleranza ≤ 3-5%)
  2. Segnale di inversione candlestick nel PRZ
  3. Volume che aumenta nel PRZ
  4. Assenza di trend molto forte opposto (non combattere trend daily forte)
```
