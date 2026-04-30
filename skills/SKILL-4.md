---
name: scalp-execution
description: >
  Identificazione di opportunita di scalping e logica di esecuzione rapida.
  Usa questa skill quando l'agent deve valutare se esiste un setup di scalp
  valido in questo momento, indipendentemente dall'analisi GEX completa.
  Trigger: "c'e uno scalp?", "setup scalp", "entry ora?", "opportunita intraday",
  "vedo un setup", "posso entrare?", "scalp long/short", "setup tecnico",
  "identificami un'opportunita", "vale la pena entrare?", "c'e edge ora?".
  Attiva anche quando price-alert-trigger o gex-analysis concludono con
  SCALP CONDIZIONALE e delegano la valutazione tecnica dettagliata.
  NON gestisce size, leva, o posizioni aperte — solo logica e identificazione.
---

# Scalp Execution Skill — Logica e Identificazione

## Filosofia dello scalping in contesto GEX

Lo scalp non e una versione piccola dello swing. E un gioco diverso:

```
SWING:  segue il trend strutturale, regge contro i MM, dura ore/giorni
SCALP:  cattura il movimento MECCANICO dei MM su un livello specifico,
        dura minuti/candele, non si oppone alla struttura — la sfrutta

La differenza chiave:
  Nello scalp non ti chiedi "dove va il mercato?"
  Ti chiedi "cosa DEVONO fare i MM nei prossimi 5-15 minuti?"
```

Ogni scalp valido ha un **trigger meccanico** — un evento osservabile
che forza i MM (o i trader algoritmici) a muoversi in una direzione
prevedibile per un periodo di tempo breve ma definito.

---

## I 6 setup di scalp validi

### Setup 1 — Rimbalzo su gamma wall (il piu affidabile)

```
CONTESTO:
  Prezzo tocca un livello gamma+ con str > 7.0
  I MM sono obbligati a vendere su quel livello (short gamma hedging)
  Se la domanda reale e insufficiente, il prezzo rimbalza meccanicamente

SEGNALI DI CONFERMA (servono almeno 2 su 3):
  [ ] Wick di rigetto: la candela penetra il livello ma chiude lontana
  [ ] StochRSI > 75 sul timeframe di esecuzione (ipercomprato)
  [ ] Volume calante nell'avvicinamento al livello (domanda si esaurisce)

SEGNALI DI INVALIDAZIONE (uno solo basta per abbandonare):
  [ ] Chiusura di candela SOPRA il livello (non e rimbalzo, e breakout)
  [ ] Volume spike nell'avvicinamento (grandi player assorbono i MM)
  [ ] LW diff recente mostra ask spariti su quel livello (struttura ceduta)

ENTRY:   Prima candela che chiude SOTTO il livello dopo il wick
TARGET:  Livello gamma+ o supporto str > 6 immediatamente sotto
         (tipicamente 0.5% - 1.5% di distanza)
DURATA:  2-8 candele sul timeframe di esecuzione
EDGE:    I MM vendono meccanicamente qui. Non serve indovinare.
```

### Setup 2 — Bounce su supporto gamma+ (speculare al Setup 1)

```
CONTESTO:
  Prezzo tocca un livello gamma+ come supporto (dopo gamma flip o da sotto)
  I MM sono obbligati a comprare su quel livello
  Se la pressione di vendita e insufficiente, il prezzo rimbalza

SEGNALI DI CONFERMA (almeno 2 su 3):
  [ ] Wick inferiore: penetra il livello ma chiude sopra
  [ ] StochRSI < 25 sul timeframe di esecuzione (ipervenduto)
  [ ] Volume calante nell'avvicinamento (vendita si esaurisce)

SEGNALI DI INVALIDAZIONE:
  [ ] Chiusura SOTTO il livello (breakdown, non rimbalzo)
  [ ] LW diff: bid spariti di recente su quel livello
  [ ] Regime gamma- sotto il livello (se cede, accelera — niente pavimento)

ENTRY:   Prima candela che chiude SOPRA il livello dopo il wick
TARGET:  Prossimo livello gamma+ o resistenza str > 6 sopra
DURATA:  2-8 candele
EDGE:    Speculare al Setup 1. MM comprano meccanicamente.
```

### Setup 3 — Breakdown con momentum (trend continuation)

```
CONTESTO:
  Prezzo rompe un supporto gamma+ o POC con chiusura confermata
  Il livello non ha retto — i MM ora vendono con il prezzo (gamma flip negativo)
  Il momentum e direzionale, non cercare rimbalzi

SEGNALI DI CONFERMA (servono tutti e 3):
  [ ] Chiusura candela 15m/1h SOTTO il livello (non solo wick)
  [ ] Volume nella candela di breakdown > media ultimi 10 periodi
  [ ] StochRSI non in zona ipervenduto estrema (< 10) — se e gia a 5, il move e quasi finito

SEGNALE OPZIONALE (aumenta confidence):
  [ ] LW diff: bid spariti dal livello nelle ultime sessioni (struttura gia indebolita)

ENTRY:   Retest del livello rotto dall'altro lato (ora resistenza)
         Se non c'e retest entro 2-3 candele, l'entry perde edge
TARGET:  Prossimo livello gamma- o supporto str > 6 sotto
         ATTENZIONE: in zona gamma- il target puo essere piu lontano del solito
DURATA:  3-12 candele (i breakdown in gamma- viaggiano piu a lungo)
EDGE:    Il livello rotto ora "respinge" il prezzo verso il basso — entry meccanica
```

### Setup 4 — Breakout con momentum (trend continuation rialzista)

```
CONTESTO:
  Speculare al Setup 3 ma al rialzo.
  Prezzo rompe resistenza gamma+ con chiusura confermata.
  I MM ora comprano con il prezzo (hedging del breakout).

SEGNALI DI CONFERMA (tutti e 3):
  [ ] Chiusura candela 15m/1h SOPRA il livello
  [ ] Volume > media (partecipazione reale)
  [ ] StochRSI non in zona ipercomprata estrema (> 90)

SEGNALE OPZIONALE:
  [ ] LW diff: bid nuovi sopra il livello (buyer si riposizionano sopra)

ENTRY:   Retest del livello rotto dall'altro lato (ora supporto)
         Se non c'e retest, considera entry con size ridotta sul momentum
TARGET:  Prossimo gamma wall nella vacuum zone sopra
EDGE:    Gamma flip — il vecchio muro diventa pavimento meccanico
```

### Setup 5 — Compressione + breakout direzionale (squeeze setup)

```
CONTESTO:
  Il prezzo e compresso tra due livelli vicini per piu candele
  Bollinger Bands si restringono visibilmente
  LW COMPRESSO (entrambi i lati si rafforzano)
  L'energia si accumula — il breakout sara direzionale e veloce

SEGNALI DI CONFERMA:
  [ ] Bollinger squeeze: bande < 0.5% di distanza sul timeframe di esecuzione
  [ ] Minimo 3 candele di consolidamento nel range stretto
  [ ] Volume decrescente nel consolidamento (nessuno si muove)

COME TRADARE:
  NON anticipare la direzione — aspetta la rottura.
  Imposta due ordini pending (OCO se disponibile):
  -> BUY STOP sopra il range + 0.15%
  -> SELL STOP sotto il range - 0.15%
  Cancella quello non triggerto dopo 2 candele dal breakout.

TARGET:  50-80% dell'altezza del range proiettata nella direzione del breakout
EDGE:    Il breakout da compressione tende a essere sostenuto (accumulo precede il move)
RISCHIO: Se il breakout fallisce e rientra nel range entro 1 candela = falso segnale,
         uscita immediata
```

### Setup 6 — Divergenza StochRSI / prezzo su livello GEX (setup avanzato)

```
CONTESTO:
  Il prezzo fa un nuovo massimo/minimo ma StochRSI NON conferma
  (massimo di prezzo piu alto, ma StochRSI con massimo piu basso = divergenza bearish)
  Questo setup e piu affidabile quando avviene ESATTAMENTE su un livello GEX

SEGNALI DI CONFERMA:
  [ ] Divergenza visibile su almeno 2 massimi/minimi consecutivi
  [ ] La divergenza avviene su un livello gamma+ str > 6.5
  [ ] StochRSI forma il secondo massimo/minimo in zona estrema (> 70 o < 30)

ENTRY:   Quando StochRSI inverte dalla zona estrema (primo hook)
TARGET:  Livello GEX immediatamente opposto
EDGE:    Il momentum si sta esaurendo esattamente dove i MM hanno piu pressione
         meccanica nella direzione opposta — doppia conferma
NOTA:    Richiede piu osservazione degli altri setup. Non usare in fretta.
```

---

## Timeframe di esecuzione

```
SCALP VELOCE (micro-scalp):
  Timeframe di lettura: 5m
  Timeframe di esecuzione: 1m-3m
  Durata media: 3-15 minuti
  Adatto a: Setup 1, 2, 5
  Condizione: mercato attivo (volume > media), no eventi macro imminenti

SCALP STANDARD:
  Timeframe di lettura: 15m
  Timeframe di esecuzione: 5m
  Durata media: 15-60 minuti
  Adatto a: tutti i setup
  Condizione: qualsiasi

SCALP ESTESO:
  Timeframe di lettura: 1h
  Timeframe di esecuzione: 15m
  Durata media: 1-4 ore
  Adatto a: Setup 3, 4, 6
  Condizione: movimento strutturale in atto, non solo tecnico
  ATTENZIONE: a questo punto e quasi uno swing — valuta gex-analysis completa
```

---

## Filtri di qualita — quando NON fare scalp

```
FILTRO 1 — ORARIO (bassa liquidita):
  BTC/ETH: evitare 02:00-06:00 UTC (spread alto, slippage)
  Futures equity: evitare fuori RTH (09:30-16:00 ET) salvo eventi specifici
  Motivo: i livelli GEX perdono efficacia senza partecipazione

FILTRO 2 — EVENTO MACRO IMMINENTE:
  Leggi hrs_to_next_event da context.json
  < 30 minuti: NON aprire nuovi scalp
  30-120 minuti: solo Setup 1/2 (rimbalzo meccanico breve), target ridotto
  Motivo: un dato macro azzera qualsiasi analisi tecnica in secondi

FILTRO 3 — PREZZO NEL MEZZO DEL RANGE:
  Se il prezzo e a > 0.8% dal livello piu vicino con str > 7
  non c'e un trigger meccanico chiaro
  -> Aspetta che il prezzo si avvicini al livello, non inseguire

FILTRO 4 — VOLUME ANOMALO PERSISTENTE:
  Se il volume e 3x+ la media per piu di 5 candele consecutive
  c'e un evento straordinario in corso (notizia, liquidazione massiccia)
  -> Non scalp contro il flusso anomalo. Aspetta che si normalizzi.

FILTRO 5 — CORRELAZIONE ROTTA:
  BTC e ETH si muovono in direzioni opposte con forza
  Segnale di stress di mercato o di evento asset-specifico
  -> Operare solo sull'asset con segnale piu pulito, size ridotta

FILTRO 6 — DOPO 2 STOP LOSS CONSECUTIVI:
  Non aprire un terzo scalp nella stessa sessione
  sul medesimo asset nella stessa direzione
  Motivo: probabilmente c'e una struttura che non stai leggendo
  -> Passa a MONITOR. Lascia che il cron gex-analysis resettti il quadro.
```

---

## Confluenza: come aumentare l'edge di ogni setup

Ogni setup ha un edge base. La confluenza lo moltiplica:

```
CONFLUENZE CHE AUMENTANO L'EDGE:

+1 livello: il setup avviene su un livello POC (Point of Control del volume profile)
+1 livello: il setup avviene su VAH o VAL del volume profile
+1 derivati: L/S ratio contrarian (es. scalp long con L/S > 1.8 = squeeze potenziale)
+1 tecnico: setup confermato su due timeframe simultaneamente (es. 5m E 15m)
+1 strutturale: il livello ha LW bid/ask attivi (non spariti) nell'ultima sessione
+1 GEX: il livello e nei top 3 della confluence_history (str > 8.5)

SCORING CONFLUENZA:
  0-1 confluenze: setup base, edge minimo
  2-3 confluenze: setup buono, edge accettabile
  4+ confluenze: setup ottimo, massima fiducia nel segnale

REGOLA PRATICA:
  Se hai un setup con solo 0-1 confluenze e il filtro anti-tilt e attivo (loss recente)
  -> Salta. Aspetta un setup con almeno 2-3 confluenze.
```

---

## Riconoscimento rapido del contesto di mercato

Prima di identificare qualsiasi setup, classifica il contesto attuale:

```
CONTESTO A — TREND CHIARO (il migliore per scalp):
  Caratteristiche: candele direzionali, volume crescente, pochi wick
  Setup migliori: 3 e 4 (trend continuation)
  Errore da evitare: Setup 1/2 (rimbalzo contro trend — bassa probabilita)

CONTESTO B — RANGE (il piu comune):
  Caratteristiche: prezzo rimbalza tra due livelli, volume calante nel range
  Setup migliori: 1 e 2 (rimbalzo ai bordi del range)
  Errore da evitare: 3 e 4 (i breakdown falliscono spesso in range)

CONTESTO C — COMPRESSIONE (pre-esplosione):
  Caratteristiche: range che si restringe, Bollinger squeeze, volume minimo
  Setup migliore: 5 (attendere breakout direzionale)
  Errore da evitare: qualsiasi setup direzionale prima della rottura

CONTESTO D — VOLATILITA ANOMALA (post-news, liquidazioni):
  Caratteristiche: candele enormi, volume 3x+, spread ampio
  Setup migliori: NESSUNO nelle prime 5-10 candele
  Dopo la normalizzazione: Setup 1/2 sui rimbalzi tecnici
  Errore da evitare: inseguire il movimento nel pieno della volatilita
```

---

## Output standardizzato

```
=== SCALP SCAN — [Asset] @ $[prezzo] | [ora CET] ===

CONTESTO:      [A-TREND / B-RANGE / C-COMPRESSIONE / D-VOLATILITA]
FILTRI ATTIVI: [lista filtri che potrebbero invalidare — o "nessuno"]

SETUP IDENTIFICATO: [numero e nome] / [NESSUN SETUP VALIDO]

SE SETUP IDENTIFICATO:
  Tipo:          [1-6 + nome]
  Livello chiave: $[X] | str [Y] | GEX [+-ZM]
  Conferme:      [lista segnali presenti — quanti su quanti]
  Confluenze:    [N]/6  ([lista confluenze attive])
  Edge stimato:  [BASSO / MEDIO / ALTO] (basato su conferme + confluenze)

  ENTRY:
    Condizione:  [cosa deve succedere prima di entrare]
    Prezzo:      $[X] (market dopo conferma / limit a $Y)
    Invalidazione entry: [condizione che cancella il setup prima dell'entry]

  TARGET:
    T1:          $[X] ([motivo — livello GEX / POC / VAH])
    T2:          $[X] (solo se vacuum zone ampia, opzionale)

  STOP LOGICO:
    Prezzo:      $[X]
    Motivo:      [perche li — livello strutturale / sopra-sotto il wick]
    NOTA: il calcolo della size basato su questo stop e fuori scope di questa skill

  TIMING:
    Timeframe:   [5m / 15m / 1h]
    Durata attesa: [X-Y candele / minuti]
    Scade se:    [condizione di timeout — es. "se non entra entro 3 candele"]

  SEGNALE DI USCITA ANTICIPATA:
    [cosa ti dice che il setup sta fallendo prima dello stop]

SE NESSUN SETUP:
  Motivo:        [filtro attivo / prezzo nel mezzo range / contesto D]
  Prossimo livello da monitorare: $[X] (in [direzione], distanza [Y%])
  Condizione per rivalutare: [quando ricercare un setup]
```

---

## Tabella riassuntiva dei 6 setup

```
SETUP  | CONTESTO  | DIREZIONE        | SEGNALE CHIAVE          | DURATA
-------|-----------|------------------|-------------------------|----------
  1    | Range/    | Contro il touch  | Wick + StochRSI alto    | 2-8 c.
       | Resistenza| (short al muro)  | + volume calo           |
-------|-----------|------------------|-------------------------|----------
  2    | Range/    | Con il touch     | Wick inf + StochRSI     | 2-8 c.
       | Supporto  | (long al rimb.)  | basso + volume calo     |
-------|-----------|------------------|-------------------------|----------
  3    | Trend down| Con il trend     | Chiusura sotto livello  | 3-12 c.
       |           | (short breakdown)| + volume up + retest    |
-------|-----------|------------------|-------------------------|----------
  4    | Trend up  | Con il trend     | Chiusura sopra livello  | 3-12 c.
       |           | (long breakout)  | + volume up + retest    |
-------|-----------|------------------|-------------------------|----------
  5    | Compress. | In entrambe      | Bollinger squeeze       | 2-6 c.
       |           | (OCO pending)    | + 3+ candele range      | post-break
-------|-----------|------------------|-------------------------|----------
  6    | Qualsiasi | Contro divergenza| Div. StochRSI su livello| 3-10 c.
       |           |                  | GEX str > 6.5           |
```
