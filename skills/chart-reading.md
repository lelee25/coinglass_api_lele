# Chart Reading Reference — Volume Profile + GEX Profile + Analysis Chart

## CHART 1 — Volume Profile

### Cosa mostra
Il Volume Profile distribuisce il volume scambiato per livello di prezzo
in un periodo dato. Non è una distribuzione temporale — è una distribuzione
**spaziale**: dove il mercato ha fatto più transazioni.

```
LEGENDA:
  Barre teal (sinistra)  = Buy Volume  — acquisti aggressivi (taker buy)
  Barre rosse (destra)   = Sell Volume — vendite aggressive (taker sell)
  Linea gialla tratteggiata = POC (Point of Control) — prezzo con più volume
  Linea blu VAH          = Value Area High — bordo superiore area di valore
  Linea blu VAL          = Value Area Low  — bordo inferiore area di valore
  Linea bianca tratteggiata = prezzo corrente
```

### I 3 livelli chiave

```
POC — Point of Control:
  Il livello con il volume totale più alto del periodo.
  È il "prezzo di equilibrio percepito" dal mercato.
  Proprietà:
  - Il prezzo tende a tornare al POC dopo deviazioni (mean reversion)
  - Se il prezzo è sopra il POC: zona di supporto quando il prezzo scende
  - Se il prezzo è sotto il POC: zona di resistenza quando il prezzo sale
  - Breakout confermato = quando il prezzo chiude dall'altro lato del POC
    e non torna dentro entro 2-3 candele

VAH — Value Area High:
  Il 70% del volume totale è stato scambiato tra VAL e VAH.
  Il VAH è il bordo superiore di questa zona.
  Proprietà:
  - Resistenza forte quando il prezzo arriva dal basso
  - Una volta superato con forza: il VAH diventa supporto (flip)
  - Se il prezzo torna sotto il VAH = il breakout era falso

VAL — Value Area Low:
  Il bordo inferiore della Value Area (70% del volume).
  Proprietà:
  - Supporto forte quando il prezzo arriva dall'alto
  - Una volta rotto: il VAL diventa resistenza
  - Prezzo sotto il VAL = il mercato ha rifiutato il "fair value" verso il basso
```

### Lettura del rapporto Buy/Sell su ogni livello

```
BUY VOLUME >> SELL VOLUME su un livello:
  A quel prezzo i compratori erano aggressivi (assorbivano offerta).
  Il livello ha "attrazione" rialzista — supporto potenziale.

SELL VOLUME >> BUY VOLUME su un livello:
  A quel prezzo i venditori erano aggressivi.
  Il livello ha "attrazione" ribassista — resistenza potenziale.

BUY ≈ SELL (barre simili):
  Zona di equilibrio — nessuno aveva il controllo.
  Spesso zona di transizione, non di reazione forte.

VOLUME TOTALE MOLTO ALTO (barra lunga):
  "Nodo di volume alto" — zona dove il mercato ha trascorso più tempo.
  Alta probabilità di reazione (da entrambe le direzioni).
  Il POC è sempre il nodo di volume più alto.

VOLUME TOTALE MOLTO BASSO (barra cortissima):
  "Vacuum zone" o "low volume node" — il mercato è passato velocemente.
  Il prezzo tende ad attraversare queste zone rapidamente.
  Identifica le zone dove il movimento sarà rapido.
```

### Pattern operativi del Volume Profile

```
PATTERN 1 — Prezzo torna al POC (mean reversion):
  Se il prezzo si è allontanato dal POC, tende a tornare.
  La forza dell'attrazione dipende da quanto tempo è passato
  e se il mercato ha creato un nuovo POC nel frattempo.
  Setup: long/short verso il POC quando il prezzo è ai bordi della value area.

PATTERN 2 — Prezzo sotto VAL (bearish):
  Il mercato ha rifiutato la value area verso il basso.
  Il VAL diventa resistenza. Il POC è target ribassista secondario.
  Comportamento tipico: rimbalzo fino al VAL (ora resistenza), poi ripartenza short.

PATTERN 3 — Prezzo sopra VAH (bullish):
  Il mercato ha accettato prezzi più alti come "fair value".
  Il VAH diventa supporto. Il POC è target rialzista secondario.
  Comportamento tipico: pullback al VAH (ora supporto), poi ripartenza long.

PATTERN 4 — Migrazione del POC:
  Se in sessioni successive il POC si sposta verso l'alto/basso,
  il "prezzo di equilibrio" del mercato si sta spostando.
  POC che migra verso l'alto = accettazione di prezzi più alti = bullish.
  POC che migra verso il basso = distribuzione = bearish.
```

### Lettura del Volume Profile in foto (caso reale 26/03)

```
POC:   70,800 (linea gialla)
VAH:   71,600
VAL:   69,500
Prezzo attuale: ~68,915 — SOTTO il VAL

LETTURA:
  Il prezzo è uscito dalla value area verso il basso.
  Il mercato ha rifiutato il "fair value" (69,500-71,600).
  Il VAL a 69,500 è ora resistenza.
  Zona 69,300-69,500 = sell wall (sell volume dominante visibile).
  Zona 70,800 = POC, resistenza più forte se il prezzo rimbalza.

  Comportamento atteso:
  - Rimbalzo: testa 69,400-69,500 (VAL come resistenza)
  - Se respinto lì: nuovo leg ribassista probabile
  - Per invalidare il bias ribassista: chiusura sopra 69,500 + riconquista VAL
```

---

## CHART 2 — GEX Profile (barre orizzontali)

### Cosa mostra

Il GEX Profile è una visualizzazione a istogramma orizzontale del Gamma Exposure
distribuito per strike. È la versione "visiva" degli array prices/values del Pine Script.

```
LEGENDA:
  Barre teal (destra del centro)  = Gamma+ (Call Wall — Resistenza)
  Barre rosse (sinistra del centro) = Gamma- (Put Wall — Supporto)
  Linea tratteggiata nera          = Prezzo corrente
  Linea tratteggiata gialla        = Zero Gamma (punto di transizione)
  Asse X                           = Valore GEX in milioni
```

### Come leggere l'istogramma

```
BARRA TEAL LUNGA (verso destra):
  Gamma+ elevato a quello strike.
  I MM devono vendere quando il prezzo si avvicina da sotto.
  → Resistenza meccanica: il prezzo rallenta e può rimbalzare.
  Più lunga la barra = più forte la resistenza.

BARRA ROSSA LUNGA (verso sinistra):
  Gamma- elevato a quello strike.
  I MM amplificano il movimento in quella zona.
  → NON è supporto classico — è zona di accelerazione.
  Se il prezzo entra nella zona rossa, il movimento si accelera.

ZERO GAMMA LINE (linea gialla):
  Il punto dove il GEX netto cambia segno (da + a -).
  Sotto questa linea: i MM destabilizzano il mercato.
  Sopra: i MM stabilizzano.
  Se il prezzo scende sotto zero gamma = regime di alta volatilità.
```

### Lettura della struttura globale

```
STRUTTURA BILANCIATA:
  Barre teal e rosse di dimensione simile sopra e sotto il prezzo.
  I MM hanno pressione in entrambe le direzioni → range trading.

STRUTTURA ASIMMETRICA BULLISH:
  Gamma+ dominante sopra, gamma- limitato sotto.
  I MM fungono da "soffitto" ma non da "acceleratori" verso il basso.
  → Movimento rialzista più lento (freni sopra) ma più sicuro.

STRUTTURA ASIMMETRICA BEARISH:
  Gamma- dominante sotto il prezzo, gamma+ lontano sopra.
  I MM amplificano ogni discesa ma non frenano i rialzi vicini.
  → Setup pericoloso per i long: ogni discesa accelera.

VACUUM ZONE nel GEX Profile:
  Zona senza barre significative (né teal né rosse).
  Il prezzo qui non ha attrito meccanico → si muove velocemente.
  Identifica le zone di movimento rapido tra un livello e l'altro.
```

### Lettura del GEX Profile in foto (caso reale 26/03)

```
Prezzo corrente: 68,915 (linea nera tratteggiata)
Zero gamma:      51,000 (linea gialla — molto lontano, non pericoloso ora)

GAMMA+ (teal) sopra il prezzo:
  Presenza significativa da ~69,500 in su, con picco intorno a 72,500-75,000.
  → Cluster di resistenze meccaniche che il prezzo deve superare per salire.
  → La densità del teal da 69,500 a 75,000 spiega perché il pump era "a gradini".

GAMMA- (rosso) sotto e intorno al prezzo:
  Barre rosse dominanti da ~55,000 a ~69,500.
  Il prezzo a 68,915 è DENTRO la zona gamma-.
  → Il prezzo è in zona di accelerazione, non di supporto.
  → I MM amplificano i movimenti qui — attenzione alle discese.

ZONA CRITICA (intorno al prezzo):
  ~69,500 = transizione da gamma- a gamma+.
  È il "gamma flip" — il punto dove la struttura cambia regime.
  Sopra 69,500: i MM frenano i movimenti (zona più stabile).
  Sotto 69,500 (dove siamo): i MM amplificano — zona instabile.

IMPLICAZIONE OPERATIVA:
  Il bias è ribassista fin quando il prezzo è sotto 69,500.
  Il primo obiettivo rialzista per uscire dalla zona gamma- è 69,500.
  Sotto il prezzo: gamma- fino a ~65,000 (barre rosse lunghe).
  Se il prezzo scende sotto 68,500 senza supporto → accelerazione verso 65-66K.
```

---

## CHART 3 — Analysis Chart (1h/4h/15m con livelli di confluenza)

### Elementi del grafico

```
CANDELE:
  Teal = candela rialzista (chiude sopra apertura)
  Rossa = candela ribassista (chiude sotto apertura)

LINEE ORIZZONTALI DI CONFLUENZA:
  Rosse con triangolo ▼ e score = RESISTENZA (vendere verso questi livelli)
  Teal con triangolo ▲ e score  = SUPPORTO (comprare da questi livelli)
  Il numero accanto = strength score (0-10) dalla confluence_history
  Tag [VAH]/[POC]/[VAL] = coincidenza con volume profile

INDICATORE CENTRALE (StochRSI):
  Due linee (solitamente blu e arancione, K e D)
  Scala 0-100
  > 80 = zona ipercomprata → possibile inversione short
  < 20 = zona ipervenduta → possibile inversione long
  Incrocio linee in zona estrema = segnale di ingresso potenziale

VOLUME (barre in basso):
  Teal = candela rialzista con quel volume
  Rosso = candela ribassista
  Barra molto alta = evento significativo (liquidazione, news, breakout)
  Volume decrescente = esaurimento del movimento

MEDIE MOBILI (linee curve sul grafico principale):
  Tipicamente MA21 e MA50 o simili
  Pendenza e incrocio indicano il bias di trend
  Prezzo sopra entrambe: uptrend. Sotto entrambe: downtrend.
```

### Come leggere i livelli di confluenza sovrapposti

```
STRENGTH SCORE SUL GRAFICO:
  Il numero accanto alla linea è lo stesso str della confluence_history.
  str 7.9 > str 7.5 > str 7.3 — il livello con score più alto è quello
  dove la reazione sarà più forte e affidabile.

TAG [VAH]/[POC]/[VAL]:
  La confluenza con il Volume Profile è il segnale più potente.
  Un livello GEX che coincide con POC o VAH/VAL ha doppia forza:
  - Il GEX porta la pressione meccanica dei MM
  - Il Volume Profile porta l'attrazione del "fair value"
  Questi livelli reggono più a lungo e generano reazioni più nette.

COME IDENTIFICARE IL SETUP SUL GRAFICO:
  1. Trova il livello più vicino al prezzo con str > 7
  2. Verifica se è resistenza (▼ rosso) o supporto (▲ teal)
  3. Guarda le ultime 2-3 candele: il prezzo si sta avvicinando o allontanando?
  4. Guarda lo StochRSI: è in zona estrema nella direzione del setup?
  5. Guarda il volume: è coerente con un'imminente reazione?
```

### Lettura del chart 1h in foto (caso reale 26/03)

```
STRUTTURA LIVELLI VISIBILI:
  70,800 str 7.3 [VAH] — resistenza (rosso ▼) — coincide con POC volume profile
  70,500 str 7.5 [POC] — resistenza (rosso ▼) — punto di controllo GEX
  70,000 str 7.9       — resistenza (rosso ▼) — livello più forte del gruppo
  69,400 str 7.2 [VAL] — resistenza (rosso ▼) — ex supporto ora resistenza
  68,850 str 4.8       — supporto (teal ▲)    — unico livello supporto visibile

PREZZO: ~68,933 (sotto tutti i livelli rossi, appena sopra il supporto 68,850)

STOCHRSI: ~20-21 (zona ipervenduto, in risalita dal minimo)
  → Segnale tecnico di potenziale rimbalzo nel breve termine

VOLUME: barra verde alta nell'ultima candela
  → Partecipazione in aumento, possibile fine della discesa

CANDELE RECENTI:
  Lunga candela rossa con picco verso 68,500 → wick inferiore
  Poi rimbalzo con candela verde
  Pattern classico: capitolazione + rimbalzo tecnico

LETTURA INTEGRATA 1h:
  Il prezzo è in zona ipervenduta (StochRSI) con un wick di capitolazione.
  Il supporto più vicino è 68,850 (str 4.8 — debole).
  Tutti i livelli sopra sono resistenze (rosso).
  
  SCENARIO RIMBALZO TECNICO:
    Target primo: 69,400 [VAL] — ex supporto, ora prima resistenza
    Target secondo: 70,000 str 7.9 — resistenza più forte
    Invalidazione: chiusura 1h sotto 68,500

  SCENARIO CONTINUAZIONE RIBASSISTA:
    Rottura di 68,850 senza rimbalzo
    Prossimo supporto significativo: livelli GEX a ~67,500 (da gex_profile)
    In zona gamma- → movimento potrebbe essere rapido
```

---

## Integrazione completa dei 3 chart + derivatives dashboard

### Framework unificato a 4 fonti

```
FONTE              | RISPONDE A                        | PESO
-------------------|-----------------------------------|------------------
Volume Profile     | "Dov'è il fair value?"            | Medio-Alto
GEX Profile        | "Dove sono i MM posizionati?"     | Alto
Analysis Chart     | "Qual è il segnale tecnico ora?"  | Medio (timing)
Derivatives Dash   | "Chi ha leva e chi sta soffrendo?"| Alto (conferma)
```

### Come combinare i 4 segnali

```
STEP 1 — Volume Profile → determina il regime
  Prezzo sopra VAL:  accettazione, fair value, setup da range
  Prezzo sotto VAL:  rifiuto, bias ribassista, i rimbalzi sono vendite
  Prezzo sopra VAH:  rottura rialzista, nuova value area si forma

STEP 2 — GEX Profile → determina l'ambiente
  Prezzo in zona gamma+: movimenti frenati, rimbalzi affidabili
  Prezzo in zona gamma-: movimenti amplificati, non mean reversion
  Prezzo vicino al gamma flip: zona di transizione, alta attenzione

STEP 3 — Derivatives Dashboard → conferma la partecipazione
  OI convergente: il movimento è sostenuto
  L/S estremo: rischio flush nella direzione del crowd
  Liquidazioni: identifica chi sta cedendo

STEP 4 — Analysis Chart → timing di entrata
  StochRSI in zona estrema + wick + livello confluence str > 7 = entry
  Volume spike sul livello = conferma
  Le medie mobili indicano il bias di trend
```

### Tabella di confluenza livelli (come incrociare le 3 fonti visive)

```
LIVELLO MASSIMA CONFLUENZA (tutte e 3 confermano):
  GEX Profile:      barra teal/rossa significativa a quel prezzo
  Volume Profile:   POC, VAH o VAL coincidono con quel prezzo
  Analysis Chart:   livello marcato con str > 8 + tag [POC]/[VAH]/[VAL]
  → Reazione quasi certa. Setup ad altissimo edge.
  Esempio: 70,800 = POC volume + forte GEX + str 7.3 [VAH] sul chart

LIVELLO BUONA CONFLUENZA (2 su 3):
  GEX + Volume Profile (senza marcatura sul chart): valido ma meno preciso
  GEX + Analysis Chart (senza volume profile): affidabile se str > 7
  Volume + Analysis (senza GEX significativo): usare con cautela
  → Edge buono ma non ottimale. Setup accettabile.

LIVELLO SINGOLA FONTE:
  Solo GEX, solo Volume, solo tecnico:
  → Edge limitato. Usare solo in confluenza con segnale derivati forte.
```

### Output integrato standard

```
=== ANALISI CHART COMPLETA — [Asset] @ $[prezzo] | [ora] ===

VOLUME PROFILE:
  POC:    $[X] | Posizione relativa: [sopra/sotto/al prezzo]
  VAH:    $[X] | Prezzo vs VAH: [dentro/sopra/sotto value area]
  VAL:    $[X] | Regime: [ACCETTAZIONE / RIFIUTO RIALZISTA / RIFIUTO RIBASSISTA]
  Nodo VP più vicino: $[X] ([buy-dominated/sell-dominated])
  Bias VP: [BULL/BEAR/NEUTRO + motivo]

GEX PROFILE:
  Zona prezzo attuale: [GAMMA+ / GAMMA- / TRANSIZIONE]
  Gamma flip:   $[X] (distanza [Y%])
  Zero gamma:   $[X] (distanza [Y%], [pericoloso/lontano])
  Prima resistenza GEX sopra: $[X] (barra teal, dimensione stimata)
  Primo supporto GEX sotto:   $[X] (o "zona gamma-, nessun supporto")
  Bias GEX: [BULL/BEAR/NEUTRO + motivo]

ANALYSIS CHART [timeframe]:
  Trend MA: [uptrend/downtrend/laterale]
  StochRSI: [valore K/D] — [OVERBOUGHT/OVERSOLD/NEUTRO]
  Volume ultima candela: [alto/medio/basso rispetto alla media]
  Livello più vicino sopra: $[X] str [Y] [▼ tag]
  Livello più vicino sotto: $[X] str [Y] [▲ tag]
  Setup tecnico visibile: [tipo setup / NESSUNO]
  Bias Chart: [BULL/BEAR/NEUTRO]

DERIVATIVES:
  [Sintesi da derivatives-dashboard: P1/P2/P3/P4 bias]
  Segnale composito: [N/4 direzione]

SEGNALE UNIFICATO:
  Fonti allineate:    [N/4 nella stessa direzione]
  Livello chiave ora: $[X] (confluenza [VP+GEX+Chart])
  Bias dominante:     [BULL/BEAR/NEUTRO]
  
SETUP OPERATIVO:
  Tipo:    [rimbalzo/breakdown/breakout/no setup]
  Entry:   $[X] — condizione: [cosa deve succedere]
  Target:  $[X] — motivazione: [livello confluence]
  Stop:    $[X] — motivazione: [livello strutturale]
  Timeout: [entro X candele, altrimenti il setup decade]
```

---

## Pattern visivi ricorrenti da riconoscere

```
PATTERN A — "Prezzo sotto VAL in gamma-" (il più ribassista):
  Volume Profile: prezzo sotto VAL
  GEX Profile:    prezzo in zona gamma-
  Analysis Chart: livelli rossi sopra, nessun supporto significativo sotto
  → Configurazione di massima pressione ribassista
  → Rimbalzi sono tecnicamente vendibili fino al VAL
  → Questo era esattamente il caso in foto (68,915 sotto VAL 69,500 in gamma-)

PATTERN B — "Rimbalzo al VAL in gamma-" (setup short classico):
  Il prezzo risale fino al VAL (ora resistenza)
  GEX: testa il gamma flip ma rimane sotto
  StochRSI: risale da oversold verso neutro
  Volume: si riduce nell'avvicinamento al VAL
  → Setup short al VAL con stop sopra il gamma flip

PATTERN C — "Rottura del gamma flip con volume" (inversione bullish):
  Il prezzo supera il livello gamma flip con chiusura confermata
  GEX: entra in zona gamma+ (teal nel profile)
  Volume Profile: supera il VAL e si avvicina al POC
  StochRSI: incrocio rialzista da zona neutro/oversold
  → Inversione strutturale — il regime cambia da gamma- a gamma+
  → Setup long con target POC poi VAH

PATTERN D — "Compressione tra POC e gamma flip" (pre-breakout):
  Volume Profile: prezzo intorno al POC
  GEX: prezzo vicino al gamma flip (transizione)
  StochRSI: neutro (40-60), nessun segnale direzionale
  Volume: basse e decrescenti
  → Il mercato decide. Aspettare la rottura con volume.
  → Sul GEX Profile: se il gamma flip è vicino al POC, la struttura è instabile

PATTERN E — "Rifiuto del POC con derivati bearish" (continuazione short):
  Volume Profile: prezzo tenta di tornare al POC ma viene respinto
  Analysis Chart: POC visibile come resistenza (str alta, tag [POC])
  Derivatives: OI+Price- (nuovi short), flush long in corso
  GEX: prezzo rimane in gamma-
  → Conferma che il ribasso è strutturale, non solo tecnico
  → Short al POC/VAL con target nodi di basso volume sotto
```
