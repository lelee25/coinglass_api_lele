# Candlestick Patterns Reference

## PATTERN SINGOLI (1 candela)

### Hammer (Martello) — BULLISH REVERSAL
```
FORMA:
  Corpo piccolo nella parte ALTA della candela
  Wick inferiore lungo (almeno 2x il corpo)
  Wick superiore assente o minimo
  Colore del corpo: indifferente (meglio se bullish/teal)

CONTESTO RICHIESTO:
  Deve formarsi in DOWNTREND o su supporto
  Se forma in uptrend = Hanging Man (bearish, vedi sotto)

PSICOLOGIA:
  I venditori spingono il prezzo in basso durante la sessione
  ma i compratori reagiscono con forza e riportano il prezzo vicino all'apertura.
  Il wick lungo = zona di rifiuto dei prezzi bassi. I buyer hanno difeso quel livello.

VALIDAZIONE:
  Candela successiva bullish (chiude sopra il corpo dell'Hammer) = conferma forte
  Volume alto sull'Hammer = segnale piu affidabile

ENTRY: apertura candela successiva (dopo chiusura conferma bullish)
TARGET: prossimo livello strutturale sopra
STOP: sotto il minimo dell'wick inferiore
AFFIDABILITA: Media-Alta (meglio su 1h/4h/1D)
```

### Hanging Man (Uomo Impiccato) — BEARISH REVERSAL
```
FORMA: identica all'Hammer ma in UPTREND
  Corpo piccolo nella parte ALTA
  Wick inferiore lungo (2x il corpo)

PSICOLOGIA:
  Identica all'Hammer ma il contesto e opposto.
  In uptrend, i venditori tentano un'inversione durante la sessione.
  Non ci riescono completamente ma il segnale e di esaurimento bullish.

VALIDAZIONE: candela successiva bearish (chiude sotto il corpo del Hanging Man)
AFFIDABILITA: Media (richiede sempre conferma)
```

### Shooting Star (Stella Cadente) — BEARISH REVERSAL
```
FORMA:
  Corpo piccolo nella parte BASSA della candela
  Wick superiore lungo (almeno 2x il corpo)
  Wick inferiore assente o minimo
  Colore del corpo: indifferente

CONTESTO: deve formarsi in UPTREND o su resistenza

PSICOLOGIA:
  I compratori spingono il prezzo in alto ma i venditori reagiscono con forza
  e riportano il prezzo vicino all'apertura. Il wick lungo in alto = rifiuto della resistenza.

VALIDAZIONE: candela successiva bearish
ENTRY: apertura candela successiva bearish
STOP: sopra il massimo dello wick superiore
AFFIDABILITA: Media-Alta
NOTA: e lo speculare bearish dell'Hammer. Stesse regole di validazione.
```

### Inverted Hammer (Martello Invertito) — BULLISH REVERSAL
```
FORMA: identica alla Shooting Star ma in DOWNTREND
  Corpo piccolo nella parte BASSA
  Wick superiore lungo

PSICOLOGIA: i compratori tentano un'inversione in downtrend. Richiede conferma forte.
AFFIDABILITA: Bassa-Media (meno affidabile della Shooting Star speculare)
```

### Doji — INDECISION / POTENTIAL REVERSAL
```
FORMA:
  Open ≈ Close (corpo quasi assente o inesistente)
  Wick superiore e inferiore presenti (lunghezza variabile)
  Sembra una croce o un segno +

VARIANTI:
  Doji classico: wick simmetrici sopra e sotto
  Dragonfly Doji: wick solo verso il basso, corpo in cima (simile a Hammer)
                  -> Bullish se su supporto
  Gravestone Doji: wick solo verso l'alto, corpo in basso (simile a Shooting Star)
                   -> Bearish se su resistenza
  Long-legged Doji: wick molto lunghi in entrambe le direzioni
                    -> Massima indecisione, mossa esplosiva probabile

PSICOLOGIA:
  Compratori e venditori si annullano perfettamente.
  Ne nessuno ha il controllo. Il mercato e in pausa.
  Da solo vale poco — ha valore solo in contesto (fine trend + livello strutturale)

REGOLA: un Doji NON e un segnale da solo.
        Doji + livello strutturale + candela di conferma successiva = setup
AFFIDABILITA: Bassa (da sola), Alta (in combinazione con contesto)
```

### Marubozu — STRONG MOMENTUM
```
FORMA:
  Corpo lungo senza wick (o wick trascurabili)
  Bullish Marubozu: apertura = minimo, chiusura = massimo (teal lungo)
  Bearish Marubozu: apertura = massimo, chiusura = minimo (rosso lungo)

PSICOLOGIA:
  Controllo totale da parte di una fazione.
  Nessun rifiuto durante tutta la sessione.
  Segnale di momentum puro — NON di inversione.

USO: conferma di breakout, inizio di trend, non entry di inversione
AFFIDABILITA: Alta come conferma momentum, non come pattern di inversione
```

### Spinning Top — INDECISION
```
FORMA:
  Corpo piccolo al centro
  Wick simmetrici sopra e sotto (non lunghi come il Doji)

PSICOLOGIA: simile al Doji ma meno estremo. Equilibrio temporaneo.
USO: segnale di esitazione, non di inversione. Simile al Doji ma meno rilevante.
```

---

## PATTERN DOPPI (2 candele)

### Bullish Engulfing (Inghiottimento Rialzista) — BULLISH REVERSAL
```
FORMA:
  Candela 1: bearish (rossa), corpo di qualsiasi dimensione
  Candela 2: bullish (teal), corpo che INGLOBIRA COMPLETAMENTE il corpo della candela 1
             La candela 2 apre sotto il close della candela 1
             e chiude sopra l'open della candela 1

CONTESTO: deve formarsi in downtrend o su supporto

PSICOLOGIA:
  Il primo giorno i venditori controllano. Il secondo giorno i compratori
  rovesciano completamente la sessione, assorbendo tutta la pressione di vendita
  e aggiungendo nuovi acquisti. Segnale di capitolazione dei venditori.

VALIDAZIONE:
  Corpo della candela 2 piu grande = segnale piu forte
  Volume alto sulla candela 2 = conferma forte
  Formazione su supporto GEX/VP = massima affidabilita

ENTRY: apertura della candela successiva all'Engulfing
STOP: sotto il minimo della candela 1 (bearish)
AFFIDABILITA: Alta — uno dei pattern piu affidabili su 1h/4h
```

### Bearish Engulfing (Inghiottimento Ribassista) — BEARISH REVERSAL
```
FORMA:
  Candela 1: bullish (teal)
  Candela 2: bearish (rossa) che inglobisce completamente il corpo della candela 1

CONTESTO: deve formarsi in uptrend o su resistenza
PSICOLOGIA: speculare al Bullish Engulfing. I compratori vengono sopraffatti.
ENTRY: apertura candela successiva alla bearish engulfing
STOP: sopra il massimo della candela 1 (bullish)
AFFIDABILITA: Alta
```

### Bullish Harami (Harami Rialzista) — BULLISH REVERSAL (debole)
```
FORMA:
  Candela 1: bearish grande (rossa lunga)
  Candela 2: bullish piccola (corpo contenuto DENTRO il corpo della candela 1)
  E l'opposto dell'Engulfing — la seconda candela e "contenuta" dalla prima.

PSICOLOGIA:
  Il movimento ribassista rallenta. I venditori perdono momentum.
  La seconda candela piccola mostra incertezza dopo un forte ribasso.
  Segnale di possibile pausa/inversione ma debole da solo.

VALIDAZIONE: richiede sempre candela di conferma bullish successiva
AFFIDABILITA: Media (meno affidabile dell'Engulfing)
```

### Bearish Harami — BEARISH REVERSAL (debole)
```
Speculare al Bullish Harami ma in uptrend.
Candela 1 bullish grande, candela 2 bearish piccola contenuta.
Stessa logica e affidabilita.
```

### Tweezer Top (Pinzette in Cima) — BEARISH REVERSAL
```
FORMA:
  Due candele con lo STESSO MASSIMO
  Candela 1: bullish (teal)
  Candela 2: bearish (rossa)
  I massimi coincidono o quasi

PSICOLOGIA:
  Il prezzo testa due volte la stessa resistenza e viene respinto entrambe le volte.
  La seconda resistenza fallisce = i compratori non riescono a superare quel livello.

CONTESTO: deve formarsi in uptrend o su resistenza
AFFIDABILITA: Media-Alta se il massimo coincide con livello GEX/strutturale
```

### Tweezer Bottom (Pinzette in Basso) — BULLISH REVERSAL
```
Speculare al Tweezer Top. Due candele con lo stesso minimo.
Candela 1 bearish, candela 2 bullish. Supporto difeso due volte.
AFFIDABILITA: Media-Alta
```

### Piercing Line (Linea di Perforazione) — BULLISH REVERSAL
```
FORMA:
  Candela 1: bearish lunga (rossa)
  Candela 2: bullish che apre SOTTO il minimo della candela 1
             e chiude SOPRA la meta del corpo della candela 1

PSICOLOGIA:
  Simile all'Engulfing ma meno forte (non inglobisce completamente).
  I compratori recuperano almeno meta della perdita del giorno precedente.
  Segnale di possibile inversione ma richiede conferma.

AFFIDABILITA: Media
```

### Dark Cloud Cover (Copertura Nuvolosa) — BEARISH REVERSAL
```
Speculare al Piercing Line in uptrend.
Candela 1 bullish lunga, candela 2 bearish che apre sopra il massimo
e chiude sotto la meta del corpo della candela 1.
AFFIDABILITA: Media
```

---

## PATTERN TRIPLI (3 candele)

### Morning Star (Stella del Mattino) — BULLISH REVERSAL FORTE
```
FORMA:
  Candela 1: bearish lunga (rossa) — conferma il downtrend
  Candela 2: corpo piccolo (qualsiasi colore, anche Doji) — gap down rispetto alla 1
             Corpo piccolo = indecisione, il ribasso perde momentum
  Candela 3: bullish lunga (teal) — chiude sopra la meta del corpo della candela 1

CONTESTO: deve formarsi in downtrend o su supporto importante

PSICOLOGIA:
  La prima candela mostra dominanza dei venditori.
  La seconda mostra esitazione — il ribasso si esaurisce.
  La terza mostra che i compratori hanno preso il controllo con forza.
  E' la narrazione completa di un'inversione bullish in 3 atti.

VALIDAZIONE:
  Gap tra candela 1 e candela 2 (non sempre presente in crypto/forex)
  Volume alto sulla terza candela = conferma forte
  Formazione su supporto GEX o POC = massima affidabilita

ENTRY: apertura candela 4 (o durante la chiusura della candela 3 se molto forte)
STOP: sotto il minimo della candela 1
AFFIDABILITA: MOLTO ALTA — pattern piu affidabile tra i tripli
```

### Evening Star (Stella della Sera) — BEARISH REVERSAL FORTE
```
FORMA: speculare al Morning Star in uptrend
  Candela 1: bullish lunga (teal)
  Candela 2: corpo piccolo (indecisione) — gap up
  Candela 3: bearish lunga (rossa) — chiude sotto la meta del corpo della candela 1

PSICOLOGIA: narrzione completa di un'inversione bearish in 3 atti
AFFIDABILITA: MOLTO ALTA
NOTA: e uno dei segnali piu forti che esistono su 4h e 1D
```

### Morning Doji Star — BULLISH REVERSAL MOLTO FORTE
```
Variante del Morning Star dove la candela 2 e specificatamente un DOJI.
L'indecisione e massima -> l'inversione e piu netta.
AFFIDABILITA: piu alta del Morning Star standard
```

### Evening Doji Star — BEARISH REVERSAL MOLTO FORTE
```
Speculare. Candela 2 = Doji in cima a un uptrend.
AFFIDABILITA: piu alta dell'Evening Star standard
```

### Three White Soldiers (Tre Soldati Bianchi) — BULLISH CONTINUATION/REVERSAL
```
FORMA:
  3 candele bullish (teal) consecutive
  Ognuna apre dentro il corpo della precedente
  Ognuna chiude progressivamente piu in alto
  Corpi lunghi, wick minimi

PSICOLOGIA:
  Tre sessioni consecutive di controllo bullish progressivo.
  I compratori guadagnano terreno sistematicamente senza cedimenti.
  Segnale di momentum forte o di inizio trend.

CONTESTO: piu significativo dopo un consolidamento o su un supporto importante
ATTENZIONE: se i corpi diventano progressivamente piu piccoli = momentum si esaurisce
AFFIDABILITA: Alta come segnale di momentum, richiede contesto per inversione
```

### Three Black Crows (Tre Corvi Neri) — BEARISH CONTINUATION/REVERSAL
```
Speculare ai Three White Soldiers.
3 candele bearish consecutive con corpo progressivamente in basso.
Segnale di forte momentum ribassista.
AFFIDABILITA: Alta
```

### Three Inside Up — BULLISH REVERSAL
```
FORMA:
  Candela 1: bearish lunga
  Candela 2: bullish contenuta dentro il corpo della 1 (Harami bullish)
  Candela 3: bullish che chiude SOPRA il massimo della candela 1

E' un Harami + candela di conferma. Molto piu affidabile dell'Harami da solo.
AFFIDABILITA: Alta (perche la terza candela conferma il pattern)
```

### Three Inside Down — BEARISH REVERSAL
```
Speculare al Three Inside Up in uptrend.
Harami bearish + terza candela bearish che chiude sotto il minimo della prima.
AFFIDABILITA: Alta
```

### Three Outside Up — BULLISH REVERSAL FORTE
```
FORMA:
  Candela 1: bearish (qualsiasi)
  Candela 2: bullish che inglobisce la 1 (Engulfing bullish)
  Candela 3: bullish che chiude ancora piu in alto

E' un Engulfing + conferma. Piu forte dell'Engulfing da solo.
AFFIDABILITA: Alta
```

### Three Outside Down — BEARISH REVERSAL FORTE
```
Speculare. Engulfing bearish + terza candela bearish che conferma.
AFFIDABILITA: Alta
```

---

## Pattern di indecisione avanzati

### Inside Bar (Bar Interna)
```
FORMA:
  Candela 2 contenuta completamente (High e Low) dentro la candela 1
  Sia corpi che wick devono essere dentro la candela precedente

PSICOLOGIA: compressione totale. Il mercato esita.
USO: segnale di breakout imminente. Tradare la rottura del High o Low della candela 1.
AFFIDABILITA: Media come segnale di direzione, Alta come segnale di volatilita imminente
```

### Outside Bar (Bar Esterna / Engulfing completo)
```
FORMA:
  Candela 2 inglobisce completamente (High e Low) la candela 1

PSICOLOGIA: volatilita esplosiva in entrambe le direzioni poi una fazione vince.
USO: la direzione della chiusura della candela 2 indica il winner.
AFFIDABILITA: Alta — spesso segna punti di svolta
```

---

## Tabella di priorita pattern

```
AFFIDABILITA DECRESCENTE:
1. Evening/Morning Doji Star (4h/1D su livello)    — molto alta
2. Evening/Morning Star (4h/1D su livello)         — molto alta
3. Bullish/Bearish Engulfing (1h/4h su livello)    — alta
4. Three White/Black Soldiers (4h su livello)      — alta
5. Three Inside/Outside Up/Down (1h/4h)            — alta
6. Tweezer Top/Bottom (1h/4h su livello)           — media-alta
7. Hammer/Shooting Star (1h/4h su livello)         — media-alta
8. Piercing/Dark Cloud (1h/4h)                     — media
9. Harami (1h/4h + conferma)                       — media
10. Doji (solo con contesto forte)                 — bassa da solo

REGOLA FINALE:
  Qualsiasi pattern di livello 1-4 su livello GEX str > 8 + volume = setup premium
  Qualsiasi pattern di livello 7-10 senza livello strutturale = ignorare
```
