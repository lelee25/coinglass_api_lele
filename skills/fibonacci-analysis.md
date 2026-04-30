# Fibonacci Reference
## Retracement · Extension · Supporti/Resistenze standalone

---

## Fondamenta: perché Fibonacci funziona nei mercati

```
LA SEQUENZA: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144...
  Ogni numero = somma dei due precedenti.
  
  Il Golden Ratio (φ = 1.618): ogni numero / il precedente ≈ 1.618
  Il suo reciproco (0.618): ogni numero / il successivo ≈ 0.618

I RATIO DERIVATI (usati nel trading):
  0.236  (23.6%)  — ritracciamento debole, mercati forti
  0.382  (38.2%)  — primo ritracciamento significativo (38.2% = 1 - 0.618)
  0.500  (50.0%)  — non Fibonacci puro, ma molto rispettato (regola di Dow)
  0.618  (61.8%)  — Golden Ratio reciproco, ritracciamento "perfetto"
  0.786  (78.6%)  — radice quadrata di 0.618, ritracciamento profondo
  0.886  (88.6%)  — radice quadrata di 0.786, ritracciamento estremo
  1.000  (100%)   — ritorno al punto di partenza
  1.272  (127.2%) — radice quadrata di 1.618, prima estensione
  1.414  (141.4%) — radice quadrata di 2.0
  1.618  (161.8%) — Golden Ratio, estensione principale
  2.000  (200%)   — estensione doppia
  2.618  (261.8%) — 1.618², estensione espansa
  3.618  (361.8%) — 2.618 + 1.000, estensione massima

PERCHÉ IL MERCATO RISPETTA QUESTI LIVELLI:
  1. Comportamento ciclico della psicologia umana (stessi rapporti di paura/avidità)
  2. Molti algoritmi e trader istituzionali usano gli stessi tool Fibonacci
  3. Self-fulfilling prophecy: se tutti si aspettano supporto a 61.8%, lo creano
  4. I pattern armonici codificano questi rapporti in strutture geometriche
```

---

## PARTE 1 — Fibonacci Retracement

### Cos'è e quando usarlo

```
IL RETRACEMENT misura quanto il prezzo "ritorna indietro" dopo un movimento.

QUANDO TRACCIARLO:
  Dopo un impulso chiaro (rialzista o ribassista) su qualsiasi TF
  L'impulso deve essere netto: partenza da uno swing significativo,
  arrivo a uno swing significativo. Non tracciare su movimenti laterali.

COME TRACCIARLO SU TRADINGVIEW:
  Tool: "Fibonacci Retracement"
  Movimento RIALZISTA: trascina dal minimo (X) al massimo (A) — dal basso verso l'alto
  Movimento RIBASSISTA: trascina dal massimo (X) al minimo (A) — dall'alto verso il basso
  I livelli si disegnano automaticamente tra i due estremi.
```

### Come leggere i livelli nel grafico (già disegnati)

```
STRUTTURA VISIVA DEL GRAFICO fibonacci_analysis.png:
  Linee orizzontali colorate tra due swing
  Etichette con le percentuali: 0.0%, 23.6%, 38.2%, 50%, 61.8%, 78.6%, 100%
  La linea 0.0% = punto di fine del movimento (swing high o swing low)
  La linea 100% = punto di inizio del movimento (swing low o swing high)

COME LEGGERE OGNI LIVELLO:
  In un retracement su movimento RIALZISTA (tracciato da basso ad alto):
    0.0%   = il massimo (A) — top dell'impulso
    23.6%  = primo supporto debole
    38.2%  = primo supporto significativo
    50.0%  = supporto medio, zona di equilibrio
    61.8%  = supporto forte (Golden Ratio) — il livello più rispettato
    78.6%  = supporto molto profondo
    88.6%  = supporto estremo (zona di inversione o breakout)
    100%   = il minimo (X) — se rompe qui l'impulso è completamente negato

  In un retracement su movimento RIBASSISTA (tracciato da alto in basso):
    Gli stessi livelli diventano RESISTENZE invece di supporti
    61.8% = resistenza forte
    78.6% = resistenza molto profonda
```

### I livelli chiave e il loro significato operativo

```
23.6% — RITRACCIAMENTO SUPERFICIALE:
  Il mercato è in trend forte. Non vuole correggere profondo.
  Rimbalzo rapido, continuazione quasi immediata.
  Setup: entry long sul rimbalzo dal 23.6% in uptrend forte
  Attenzione: se il prezzo rompe il 23.6% con forza, il prossimo target è 38.2%

38.2% — PRIMO LIVELLO SIGNIFICATIVO:
  Il ritracciamento "minimo normale" di un trend sano.
  I trader trend-following comprano/vendono qui la prima volta.
  Se tiene: trend molto forte, entry di qualità
  Se rompe: il trend non è così forte come sembrava → prossimo target 50%

50.0% — ZONA DI EQUILIBRIO (regola di Dow):
  Non è Fibonacci puro ma è estremamente rispettato.
  Il mercato è indeciso — equilibrio tra compratori e venditori.
  Zona di alta indecisione: aspettare una candela direzionale per decidere.
  Se il mercato rimbalza dal 50% con forza: trend riprende
  Se il mercato consolida al 50%: aspettare conferma

61.8% — GOLDEN RATIO — IL LIVELLO PIÙ IMPORTANTE:
  Il ritracciamento "perfetto" secondo la teoria armonica.
  I grandi player si aspettano supporto/resistenza qui.
  Setup di qualità: entry long sul rimbalzo dal 61.8% in uptrend
  Se rompe il 61.8% verso il basso: alta probabilità di test del 78.6% o 100%
  NOTA: nei pattern armonici, il punto B del Gartley è esattamente al 61.8%

78.6% — RITRACCIAMENTO PROFONDO:
  Il trend ha subito una correzione significativa.
  Il mercato testa la "zona di massimo stress" del trend.
  Se tiene: forte segnale che il trend riprenderà (buyers/sellers difendono)
  Se rompe: il trend è probabilmente finito → test del 100% o oltre
  NOTA: nel pattern Bat, il punto D è all'88.6% — molto vicino a questa zona

88.6% — RITRACCIAMENTO ESTREMO:
  Correzione quasi completa. Ultima linea di difesa del trend.
  Se tiene: inversione con movimento potenzialmente esplosivo (spring)
  Se rompe: il trend originale è terminato, preparati per inversione maggiore
  NOTA: nel pattern Bat, D è esattamente all'88.6% di XA

100% — FINE DELL'IMPULSO:
  Il prezzo è tornato al punto di partenza.
  Se tiene come supporto: double bottom o area di accumulazione
  Se rompe: il movimento originale è completamente negato
```

### Confluenza tra livelli Fibonacci e struttura GEX/VP

```
REGOLA FONDAMENTALE:
  Un livello Fibonacci da solo è un'indicazione.
  Un livello Fibonacci che coincide con GEX str > 7 o POC/VAH/VAL
  è un segnale strutturale di alta qualità.

COME LEGGERE LA CONFLUENZA NEL GRAFICO:
  Se vedi una linea Fibonacci che coincide con:
  - Una linea GEX dal chart_analysis (livelli rossi/teal)
  - Il POC o VAH/VAL del volume_profile
  - Un supporto/resistenza storico evidente
  → Quella zona ha TRIPLICE confluenza → alta probabilità di reazione

ESEMPIO PRATICO:
  Il 61.8% di Fibonacci cade a $70,000
  Il livello GEX ha str 7.9 a $70,000
  Il POC del volume profile è a $70,800 (vicino)
  → Zona $70,000-70,800 = cluster di confluenza massima
  → Entry long nel cluster con stop sotto $69,500
```

---

## PARTE 2 — Fibonacci Extension

### Cos'è e quando usarlo

```
L'EXTENSION calcola DOVE il prezzo andrà DOPO aver completato la correzione.
Si usa per identificare i TARGET di prezzo dopo un breakout o un rimbalzo.

DIFFERENZA DA RETRACEMENT:
  Retracement: misura quanto si "ritira" (< 100% del movimento)
  Extension:   proietta dove arriverà (> 100% del movimento)

QUANDO USARLA:
  Dopo aver identificato un rimbalzo dal livello di retracement
  Per calcolare il target del prossimo impulso nella direzione del trend
  Per calcolare il PRZ finale nei pattern armonici (dove si trova D)
```

### Come tracciare l'Extension su TradingView

```
METODO 1 — Fibonacci Extension (3 punti):
  Tool: "Fibonacci Extension" o "Fib Extension"
  Punto 1: inizio dell'impulso (X o A)
  Punto 2: fine dell'impulso (A)
  Punto 3: fine della correzione (B o il rimbalzo)
  → I livelli proiettano automaticamente dove andrà il prezzo

METODO 2 — Retracement con livelli > 100%:
  Traccia il Fibonacci Retracement normalmente
  Abilita i livelli 127.2%, 161.8%, 200%, 261.8% nelle impostazioni
  Questi livelli oltre il 100% SONO le extensions

LETTURA NEL GRAFICO (livelli già disegnati da te):
  Se nel grafico fibonacci_analysis.png vedi linee oltre il massimo/minimo:
  127.2% = prima extension (target conservativo)
  161.8% = extension principale (target primario)
  200.0% = extension doppia (target aggressivo)
  261.8% = extension espansa (target massimo del movimento)
```

### I livelli di Extension e il loro uso

```
127.2% (1.272) — PRIMA EXTENSION:
  Target "minimo" dopo un breakout.
  Se il movimento è debole, spesso si ferma qui.
  Nei pattern armonici: CD può terminare a 1.272 di BC (Butterfly alternativo)
  Setup: take profit parziale (50%) quando il prezzo tocca questo livello

161.8% (1.618) — GOLDEN RATIO EXTENSION — TARGET PRINCIPALE:
  Il target di estensione più rispettato.
  La maggior parte dei movimenti sani raggiunge il 161.8%.
  Nei pattern armonici: target standard di molti CD legs
  Setup: take profit principale (restante 50%) a questo livello

200.0% (2.000) — ESTENSIONE DOPPIA:
  Target aggressivo per trend molto forti.
  Il prezzo ha "raddoppiato" il movimento originale.
  Setup: trailing stop o hold solo se il trend è strutturalmente forte

261.8% (2.618) — ESTENSIONE ESPANSA:
  Movimenti eccezionali o pattern Crab (D a 1.618 di XA)
  Nei pattern armonici: CD del Crab raggiunge 2.618 di BC
  Setup: molto raro nel breve termine, più comune su TF daily/settimanale

REGOLA PRATICA PER I TARGET:
  Extension 127.2% = Take Profit 1 (scalp)
  Extension 161.8% = Take Profit 2 (swing)
  Extension 200.0% = Take Profit 3 (solo con trend forte confermato)
```

### Come usare le Extension insieme ai pattern armonici

```
NEI PATTERN ARMONICI, le Extension calcolano dove si trova D (il PRZ):

GARTLEY bullish:
  Traccia Fibonacci da X ad A
  Il retracement: B deve essere al 61.8% di XA
  L'extension da B: D deve essere al 78.6% di XA (retracement, non extension)
  → Usa il retracement su XA per trovare D

BAT bullish:
  Traccia Fibonacci da X ad A
  B al 38.2%-50% di XA (retracement)
  D all'88.6% di XA (retracement profondo)
  → Usa il retracement su XA, guarda dove cade l'88.6%

BUTTERFLY bullish:
  Traccia Fibonacci da X ad A
  D si trova al 127.2% o 161.8% OLTRE X (extension, non retracement)
  → Abilita i livelli di extension nel tool, guarda 127.2% e 161.8%

CRAB bullish:
  Traccia Fibonacci da X ad A
  D si trova al 161.8% OLTRE X
  → Extension 161.8% di XA = D del Crab

SEQUENZA OPERATIVA:
  1. Identifica XA (impulso iniziale)
  2. Traccia Fibonacci Retracement da X ad A
  3. Trova B (deve rispettare il ratio del pattern)
  4. Traccia Fibonacci Extension o Retracement per trovare D
  5. Confronta con harmonic-patterns.md per confermare il pattern
  6. D = PRZ = zona di ingresso
```

---

## PARTE 3 — Fibonacci come Supporti/Resistenze Standalone

### Filosofia: Fibonacci senza pattern armonico

```
Non hai bisogno di identificare un pattern XABCD per usare Fibonacci.
Puoi tracciarlo su qualsiasi impulso significativo e usare i livelli
come supporti/resistenze "intelligenti" — più precisi dei livelli statici.

LA DIFFERENZA dai livelli GEX/VP:
  GEX/VP: dove i MM e i grandi player hanno posizioni
  Fibonacci: dove la matematica del mercato crea attrazione/repulsione

Quando i due si sovrappongono: massima confluenza.
```

### Fibonacci su movimento rialzista (supporti)

```
CONTESTO: il mercato è in uptrend, fa un impulso, poi si corregge

COME USARLO:
  Traccia Fibonacci dall'ultimo swing low (X) all'ultimo swing high (A)
  I livelli tra 0% e 100% diventano i SUPPORTI della correzione

COMPORTAMENTO ATTESO a ogni livello:
  23.6%: rimbalzo rapido se raggiunto — trend molto forte
  38.2%: primo test importante, spesso il primo rimbalzo significativo
  50.0%: zona di decisione, aspettare segnale candlestick
  61.8%: supporto forte, zona di acquisto per trader trend-following
  78.6%: ultimo baluardo prima della negazione del trend
  100%:  test del minimo precedente — double bottom o fine trend

STRATEGIE OPERATIVE:

STRATEGIA 1 — Rimbalzo dal Golden Ratio (61.8%):
  Condizione: prezzo ritraccia al 61.8% in uptrend
  StochRSI: in zona ipervenduta (< 30)
  Volume: si riduce nell'avvicinamento al 61.8%
  Candela: Hammer, Engulfing bullish, o Morning Star sul 61.8%
  Entry: chiusura della candela di conferma
  Stop: sotto il 78.6% (o sotto il 61.8% con tolleranza 1%)
  Target: estensione 127.2% poi 161.8% del movimento correttivo
  R/R tipico: 1:2 a 1:4

STRATEGIA 2 — Test del 38.2% in trend molto forte:
  Condizione: prezzo fa piccola correzione al 38.2% in trend forte (MA forte)
  StochRSI: tocca brevemente 30-40 poi rimbalza
  Volume: molto basso nella correzione (no capitolazione)
  Entry: candela bullish dopo il tocco del 38.2%
  Stop: sotto il 50.0%
  Target: nuovo massimo oltre il precedente
  R/R tipico: 1:3 a 1:5 (alta probability entry)

STRATEGIA 3 — Difesa del 78.6% (inversione potenziale):
  Condizione: prezzo in correzione profonda raggiunge 78.6%
  StochRSI: ipervenduto profondo (< 20), divergenza bullish
  Volume: spike sulla candela che tocca il 78.6% (capitolazione o accumulo)
  Entry: solo con candela di inversione forte (Engulfing, Morning Star)
  Stop: sotto il 100% (minimo precedente)
  Target: 38.2% poi 50% del range come primo recupero
  R/R tipico: 1:2 (stop ampio ma target realistico)
```

### Fibonacci su movimento ribassista (resistenze)

```
CONTESTO: il mercato è in downtrend, fa un impulso ribassista, poi rimbalza

COME USARLO:
  Traccia Fibonacci dall'ultimo swing high (X) all'ultimo swing low (A)
  I livelli tra 0% e 100% diventano le RESISTENZE del rimbalzo

COMPORTAMENTO ATTESO:
  23.6%: rimbalzo debole respinto subito — trend ribassista molto forte
  38.2%: prima resistenza significativa del rimbalzo
  50.0%: zona di decisione — spesso venduta dai trader short
  61.8%: resistenza forte (Golden Ratio) — zona di vendita privilegiata
  78.6%: resistenza molto profonda, quasi inversione
  100%:  test del massimo precedente (double top potenziale)

STRATEGIA — Short al 61.8% in downtrend:
  Condizione: prezzo rimbalza al 61.8% in downtrend
  StochRSI: arriva in zona ipercomprata (> 70) nel rimbalzo
  Volume: si riduce nell'avvicinamento al 61.8%
  Candela: Shooting Star, Bearish Engulfing, Evening Star
  Entry: chiusura della candela bearish di conferma
  Stop: sopra il 78.6%
  Target: estensione ribassista (127.2%, 161.8% del movimento correttivo)
  R/R tipico: 1:2 a 1:3
```

### Fibonacci Multi-Swing (livelli cluster)

```
TECNICA AVANZATA: traccia Fibonacci su più swing diversi.
Se più livelli Fibonacci di swing diversi cadono nella stessa zona → CLUSTER.

ESEMPIO:
  Swing 1 (XA grande): il 61.8% cade a $70,000
  Swing 2 (AB piccolo): il 38.2% cade a $70,200
  Swing 3 (BC): l'estensione 161.8% cade a $69,900
  → Cluster $69,900-$70,200 = zona di alta confluenza Fibonacci

  Se in questa zona c'è anche:
  - Livello GEX str > 7
  - POC o VAL del volume profile
  → MASSIMA CONFLUENZA POSSIBILE — setup ad altissimo edge

COME IDENTIFICARLO NEL GRAFICO:
  Cerca zone dove più linee Fibonacci si "affollano" vicine
  Una zona con 3+ linee Fibonacci in un range del 1-2% = cluster significativo
  Il prezzo tipicamente rallenta o inverte in queste zone
```

---

## PARTE 4 — Come leggere il grafico fibonacci_analysis.png

### Struttura visiva del grafico

```
ELEMENTI CHE VEDRAI:
  Candele (prezzo)
  Linee orizzontali colorate con etichette percentuali
    → Queste sono le linee Fibonacci già tracciate da te
  Eventuale ombreggiatura tra livelli (Value Area di Fibonacci)
  Linea tratteggiata orizzontale = prezzo corrente

COME L'AGENT LEGGE IL GRAFICO:

STEP 1 — Identifica il movimento di riferimento:
  Quale swing ha generato le linee Fibonacci visibili?
  (Cerca il punto 0% = estremo recente e il punto 100% = altro estremo)
  Esempio: "Fibonacci tracciato da $67,000 (100%) a $72,000 (0%)"
  → Movimento rialzista di $5,000 di riferimento

STEP 2 — Identifica dove si trova il prezzo rispetto ai livelli:
  Il prezzo è sopra o sotto il 61.8%?
  Il prezzo è in avvicinamento o allontanamento da un livello chiave?
  Il prezzo ha rotto un livello importante (ora resistenza/supporto)?

STEP 3 — Identifica la zona di massima rilevanza:
  Qual è il livello Fibonacci più vicino al prezzo corrente?
  C'è un cluster (più linee vicine)?
  C'è confluenza con altri strumenti (GEX/VP)?

STEP 4 — Leggi il contesto del pattern (se presente):
  Se nel grafico sono visibili strutture XABCD:
  → Carica references/harmonic-patterns.md e verifica i ratio
  Se i livelli Fibonacci servono come S/R standalone:
  → Applica le strategie della Parte 3 sopra
```

### Output standard dopo lettura del fibonacci_analysis.png

```
=== FIBONACCI ANALYSIS — [Asset] @ $[prezzo] | [ora] ===

MOVIMENTO DI RIFERIMENTO:
  Da:   $[X] ([data swing])  ← punto 100%
  A:    $[A] ([data swing])  ← punto 0%
  Tipo: [RIALZISTA / RIBASSISTA]
  Ampiezza: $[N] ([N%])

POSIZIONE ATTUALE:
  Prezzo:   $[X]
  Livello:  tra [N%] e [N%] di Fibonacci
  Zona:     [sopra/sotto il Golden Ratio 61.8%]

LIVELLI CHIAVE VISIBILI:
  [Livello]%  = $[X]  — [tipo: S/R forte/debole] — [distanza% dal prezzo]
  [Livello]%  = $[X]  — ...
  (lista dei livelli rilevanti ordinati per distanza dal prezzo)

CLUSTER IDENTIFICATI:
  [Zona $X-$Y]: [N] livelli Fibonacci convergenti → [alta/media/bassa confluenza]
  Confluenza con GEX/VP: [SÌ a $X str Y / NO]

LETTURA PATTERN ARMONICO (se applicabile):
  Pattern in formazione: [nome / NESSUNO]
  Punti identificati: X=$X A=$X B=$X C=$X D=PRZ $X
  Validazione ratio: [confermati / non confermati / da verificare]
  → Caricato harmonic-patterns.md: [SI/NO]

SETUP OPERATIVO:
  Livello più rilevante ora: $[X] ([N%] Fibonacci [+ confluenze])
  Tipo setup:   [rimbalzo / short / attesa PRZ / standalone S/R]
  Entry:        $[X] — condizione: [candela + StochRSI + volume]
  Target 1:     $[X] (ext. [N%] o livello Fibonacci successivo)
  Target 2:     $[X] (ext. [N%])
  Stop:         $[X] (sotto/sopra [N%] con tolleranza 1%)

INTEGRAZIONE CON ALTRI STRUMENTI:
  GEX:  [il livello Fibonacci coincide con / è distante da un livello GEX]
  VP:   [coincidenza con POC/VAH/VAL o area a basso volume]
  StochRSI: [zona corrente, segnale atteso al livello chiave]
  Volume: [comportamento atteso al livello]
```

---

## Tabella dei ratio Fibonacci — Riferimento rapido

```
RATIO   | NOME            | USO PRIMARIO                    | AFFIDABILITA
--------|-----------------|--------------------------------|-------------
0.236   | Superficie      | Trend molto forti, entry veloce | Bassa
0.382   | Primo target    | Primo S/R significativo         | Media
0.500   | Equilibrio      | Zona di decisione (regola Dow)  | Media-Alta
0.618   | Golden Ratio    | S/R principale, pattern armonici| Molto Alta
0.786   | Profondo        | Ritracciamento profondo         | Alta
0.886   | Estremo         | Bat pattern, ultimo baluardo    | Alta
1.000   | Origine         | Test del punto di partenza      | Alta
1.272   | Prima ext.      | Target conservativo, Butterfly  | Alta
1.414   | Intermedia      | Target intermedio               | Media
1.618   | Golden Ext.     | Target principale, Crab/Butt.   | Molto Alta
2.000   | Doppia          | Target aggressivo               | Media
2.618   | Espansa         | Crab (CD leg), trend molto forti| Media
3.618   | Massima         | Rare estensioni eccezionali     | Bassa

PRIORITA OPERATIVA (da usare sempre):
  0.382 — 0.618 — 0.786 — 1.272 — 1.618
  Gli altri sono complementari, non primari.
```

---

## Errori comuni con Fibonacci

```
TRACCIARE DA SWING SBAGLIATI:
  Usare picchi/valli intraday non significativi.
  Regola: usa solo swing visibili su almeno il TF di esecuzione (1h minimum).
  Su 1h: usa swing che abbiano almeno 3-5 candele di reazione intorno.

IGNORARE IL CONTESTO DI TREND:
  Il 61.8% in uptrend = SUPPORTO (comprare)
  Il 61.8% in downtrend come resistenza al rimbalzo = VENDERE
  Lo stesso livello ha significato opposto in trend diversi.

ASPETTARSI UN RIMBALZO PRECISO AL LIVELLO:
  Il prezzo può toccare il livello con un wick e rimbalzare,
  oppure consolidare 5-10 candele intorno al livello prima di muoversi.
  Regola: aspetta sempre il segnale candlestick, non entrare sul touch.

NON AGGIORNARE I LIVELLI:
  Dopo un nuovo swing significativo, il Fibonacci va ritraccato.
  Livelli su swing di 3+ settimane fa perdono rilevanza progressivamente.
  Aggiornare ad ogni nuova sessione giornaliera (cron).

USARE FIBONACCI SU MOVIMENTI TROPPO PICCOLI:
  Su movimenti < 2-3% i livelli Fibonacci sono troppo ravvicinati.
  Il rumore del mercato li rende inefficaci.
  Minimo consigliato: movimento di almeno 3-5% per tracciare livelli utili.

CONFONDERE EXTENSION E RETRACEMENT:
  Retracement: sempre tra 0% e 100% del movimento originale
  Extension: va oltre il 100% (verso nuovi massimi/minimi)
  Se vedi livelli oltre il 100%: sono extensions, non retracements.
```
