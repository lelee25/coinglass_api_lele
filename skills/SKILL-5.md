---
name: derivatives-dashboard
description: >
  Analisi del derivatives dashboard BTC/ETH con 4 pannelli: OI+Price divergenza,
  Long/Short ratio, Liquidazioni, OI Delta + Price Change.
  Usa questa skill quando l'agent riceve screenshot o dati del derivatives_dashboard,
  o quando deve interpretare segnali derivati intraday per decisioni operative.
  Trigger: "analizza il dashboard", "cosa dicono i derivati", "leggi il dashboard",
  "OI divergenza", "liquidazioni", "L/S ratio", "derivatives_dashboard.png",
  "segnale derivati", "conferma trend", "OI delta", "sentiment retail",
  "bullish squeeze", "bearish flush", "convergenza OI prezzo".
  Attiva anche quando gex-analysis o price-alert-trigger richiedono
  una lettura approfondita dei derivati prima di una decisione.
  Output: lettura integrata dei 4 pannelli + segnale composito + implicazioni operative.
---

# Derivatives Dashboard Skill

## I 4 pannelli e cosa misurano

Il dashboard misura lo stesso mercato da 4 angolazioni complementari.
Nessun pannello da solo e sufficiente — il segnale emerge dall'incrocio.

```
PANNELLO 1 — OI + Price (convergenza/divergenza)
  COSA MISURA: se il capitale nel mercato (OI) conferma o nega il movimento di prezzo
  DOMANDA: "I soldi stanno entrando nella direzione del prezzo?"

PANNELLO 2 — Long/Short Ratio (retail sentiment)
  COSA MISURA: il posizionamento del retail (Binance futures)
  DOMANDA: "Il crowd e dalla mia parte o contro di me?"

PANNELLO 3 — Liquidazioni (long rosso, short verde)
  COSA MISURA: chi sta soffrendo — quali posizioni vengono forzatamente chiuse
  DOMANDA: "Il mercato sta pulendo long o short?"

PANNELLO 4 — OI Delta + Price Change (conferma trend)
  COSA MISURA: la combinazione OI variazione + direzione prezzo in ogni candela
  DOMANDA: "Il movimento attuale e sostenuto da nuove posizioni o da chiusure?"
```

---

## PANNELLO 1 — OI + Price: lettura convergenza/divergenza

### Le 4 combinazioni fondamentali

```
OI SALE + PREZZO SALE = TREND GENUINO (rialzista confermato)
  Nuovo capitale entra nella direzione del rialzo.
  I long si aprono con convinzione. Edge alto per long.
  Sul grafico: entrambe le linee si muovono verso l'alto insieme.

OI SALE + PREZZO SCENDE = NUOVI SHORT (pressione ribassista reale)
  Nuovo capitale entra nella direzione del ribasso.
  I short si aprono con convinzione. Edge alto per short.
  Sul grafico: OI sale mentre prezzo scende — divergenza ribassista.

OI SCENDE + PREZZO SALE = SHORT SQUEEZE o CHIUSURA SHORT
  Il rialzo e guidato da chiusura di posizioni short, non da nuovi long.
  Il rally puo essere violento ma e meno sostenibile.
  Sul grafico: OI scende mentre prezzo sale — divergenza da monitorare.

OI SCENDE + PREZZO SCENDE = CHIUSURA LONG (de-leveraging)
  Il ribasso e guidato da uscita di long, non da nuovi short.
  Movimento piu lento ma puo continuare per piu sessioni.
  Sul grafico: entrambe le linee scendono — de-leveraging in atto.
```

### Come leggere la DIVERGENZA (zona evidenziata in rosso nel dashboard)

```
DIVERGENZA = OI e prezzo si muovono in direzioni opposte per piu candele

Quando vedi la zona rossa nel pannello 1:
  1. Identifica quale delle 4 combinazioni si sta verificando
  2. Misura la durata: piu dura, piu significativa
  3. La divergenza si RISOLVE sempre — o il prezzo si adegua all'OI o viceversa

DIVERGENZA BEARISH (la piu comune sul dashboard mostrato):
  Prezzo fa nuovo massimo MA OI non conferma (o scende)
  Segnale: il rally e esausto, non ci sono nuovi compratori
  Implicazione: alta probabilita di inversione o consolidamento

DIVERGENZA BULLISH:
  Prezzo fa nuovo minimo MA OI non conferma (o scende)
  Segnale: il ribasso e guidato da chiusure, non da nuovi short
  Implicazione: possibile rimbalzo — i short non stanno buildando

FALSA DIVERGENZA (da non sovrastimare):
  Dura solo 1-2 candele -> rumore, non segnale
  Avviene su OI molto basso -> bassa partecipazione, poco significativo
  Avviene fuori orario (notte, weekend) -> liquidita ridotta distorce OI
```

### Lettura quantitativa OI

```
VALORI DI RIFERIMENTO BTC (Binance Futures, in BTC):
  OI in forte crescita: > +2% in 1h        -> partecipazione significativa
  OI stabile:          variazione < 0.5%    -> mercato in attesa
  OI in calo:          < -1% in 1h          -> de-leveraging in corso
  OI in forte calo:    < -3% in 1h          -> uscita massiccia posizioni

CONTESTO: confronta sempre il valore attuale con il range delle ultime 24-48h.
  Un OI a 48,000 BTC e alto o basso? Solo il contesto lo dice.
  Quello che conta e la DIREZIONE e la VELOCITA del cambiamento.
```

---

## PANNELLO 2 — Long/Short Ratio: lettura del sentiment retail

### Scale di interpretazione

```
RATIO > 2.0  = CROWDING LONG ESTREMO
  Il 67%+ del retail e long. Posizionamento pericolosamente sbilanciato.
  Implicazione CONTRARIAN: il mercato e in zona "flush long" — una mossa
  ribassista potrebbe liquidare ondate di stop consecutivi.
  NON significa "vai short subito" — significa "non aggiungere long qui".

RATIO 1.5-2.0 = SBILANCIAMENTO MODERATO LONG
  Sentiment rialzista ma non estremo. Monitorare.
  Se il prezzo scende -> liquidazioni long accelerano il movimento.

RATIO 1.2-1.5 = ZONA NEUTRALE CON BIAS LONG
  Distribuzione quasi equa. Meno rischio flush. Movimento piu bilanciato.

RATIO 0.8-1.2 = ZONA NEUTRALE
  Nessun segnale forte. Il movimento dipende da altri fattori.

RATIO 0.5-0.8 = SBILANCIAMENTO MODERATO SHORT
  Sentiment ribassista. Se il prezzo sale -> short squeeze accelera.

RATIO < 0.5  = CROWDING SHORT ESTREMO
  Zona di potenziale squeeze violento al rialzo.
```

### Lettura della DINAMICA (non solo il valore assoluto)

```
IL RATIO CHE CAMBIA E PIU IMPORTANTE DEL RATIO STATICO:

Ratio che SALE mentre prezzo SALE:
  -> Il retail insegue il rialzo. Aumenta il rischio flush al prossimo pull.
  -> Tipico di bull trap: tutti entrano long in cima.

Ratio che SALE mentre prezzo SCENDE:
  -> Il retail fa averaging down o compra il ribasso.
  -> Sentiment contrarian: se OI sale con questo pattern = flush long imminente.

Ratio che SCENDE mentre prezzo SALE:
  -> I long prendono profitto, i short capitolano (short squeeze).
  -> Movimento piu sano — non c'e eccesso di euforia.

Ratio che SCENDE mentre prezzo SCENDE:
  -> I long si arrendono (capitolazione). Spesso avviene vicino ai bottom.
  -> Se OI scende contemporaneamente = de-leveraging completo -> potenziale rimbalzo.

LINEA TRATTEGGIATA nel pannello (overbought/oversold):
  Sopra la linea superiore (es. > 1.3): zona overbought retail
  Sotto la linea inferiore (es. < 0.8): zona oversold retail
  Queste soglie sono relative al range storico dell'asset — non universali.
```

---

## PANNELLO 3 — Liquidazioni: chi sta soffrendo

### Lettura delle barre

```
BARRE ROSSE (verso il basso) = LONG LIQUIDAZIONI
  I compratori con leva vengono forzatamente chiusi dal mercato.
  Accelerano i ribassi: ogni long liquidato e una vendita forzata.
  Etichetta nel dashboard: "Long liq (bearish flush)"

BARRE VERDI (verso l'alto) = SHORT LIQUIDAZIONI
  I venditori con leva vengono forzatamente chiusi.
  Accelerano i rialzi: ogni short liquidato e un acquisto forzato.
  Etichetta nel dashboard: "Short liq (bullish squeeze)"
```

### Pattern operativi

```
CLUSTER DI SHORT LIQUIDAZIONI (barre verdi alte consecutive):
  Bullish squeeze in corso. Il prezzo sale forzatamente.
  Implicazione: il rally e "artificialmente" accelerato.
  ATTENZIONE: quando finiscono gli short da liquidare, il rally si esaurisce.
  Segnale di fine squeeze: le barre verdi diventano progressivamente piu piccole.

CLUSTER DI LONG LIQUIDAZIONI (barre rosse profonde consecutive):
  Bearish flush in corso. Il prezzo scende forzatamente.
  Implicazione: ogni stop che salta genera vendita -> nuovo stop -> altra vendita.
  Puo accelerare rapidamente. Non comprare "perche e sceso tanto" in questo contesto.
  Segnale di fine flush: le barre rosse diventano progressivamente piu piccole.

ALTERNANZA RAPIDA (verde e rosso si alternano):
  Mercato bidirezionale — nessuno ha il controllo netto.
  Alta volatilita ma nessuna direzione chiara.
  Scalp possibili ma swing rischioso.

LIQUIDAZIONI ASSENTI (barre molto piccole per molte candele):
  Bassa partecipazione con leva. Mercato retail in attesa.
  Spesso precede una mossa direzionale (si accumula la tensione).

RATIO LONG/SHORT NELLE LIQUIDAZIONI (24h):
  Esempio dashboard: L:269.7 / S:207.6 BTC
  Long > Short -> il mercato ha colpito piu long che short -> ribassista recente
  Short > Long -> il mercato ha colpito piu short che long -> rialzista recente
  Rapporto > 2:1 in una direzione -> flush strutturale in quella direzione
```

### Lettura della DIMENSIONE delle barre

```
BARRE MOLTO ALTE (outlier):
  Evento di liquidazione massiccia. Solitamente segna un punto di svolta.
  I grandi player hanno aperto posizioni in leva in quella zona.
  Dopo un'outlier: spesso segue consolidamento o inversione parziale.

BARRE UNIFORMI E COSTANTI:
  Liquidazioni distribuite — mercato in trend regolare con partecipazione normale.
  Non c'e evento specifico, e il comportamento normale del mercato in movimento.
```

---

## PANNELLO 4 — OI Delta + Price Change: conferma del trend

### Le 3 combinazioni colore

```
VERDE (OI sale + Prezzo sale) = TREND GENUINO
  Nuovo denaro entra nella direzione rialzista.
  E la conferma piu forte che un rally e sostenuto.
  Piu barre verdi consecutive = trend con momentum reale.

ARANCIONE (OI sale + Prezzo scende) = NUOVI SHORT
  Nuovo denaro entra nella direzione ribassista.
  I bear sono convinti e stanno costruendo posizioni.
  Segnale: il ribasso e intenzionale, non solo chiusura di long.

GRIGIO (OI scende + qualsiasi prezzo) = POSIZIONI CHIUSE
  Il mercato si de-leveraggia. Non ci sono nuovi entranti.
  Il movimento (su o giu) e guidato da chiusure, non da convinzione.
  Meno affidabile come segnale direzionale.
```

### Lettura delle sequenze

```
SEQUENZA BULLISH FORTE:
  Piu barre verdi consecutive (OI+ Price+)
  -> Trend genuino, nuovi long entrano con convinzione
  -> Edge alto per posizioni long fino al prossimo livello GEX

SEQUENZA BEARISH FORTE:
  Piu barre arancioni consecutive (OI+ Price-)
  -> Pressione short strutturale
  -> Edge alto per short, ma attenzione al L/S ratio (se gia estremo = flush risk)

SEQUENZA MISTA (verde + arancione alternati):
  Il mercato oscilla senza direzione netta nel breve termine
  -> Aspetta 3+ barre consecutive dello stesso colore prima di prendere posizione

DOMINANZA GRIGIA (molte barre grigie):
  De-leveraging generalizzato. Tutti escono.
  -> Volatilita puo aumentare improvvisamente quando finisce il de-leveraging
  -> Non e un segnale direzionale. E un segnale di "pulizia" in corso.

INVERSIONE DA GRIGIO A VERDE/ARANCIONE:
  Dopo un periodo di de-leveraging, nuove posizioni iniziano ad aprirsi.
  La PRIMA barra colorata dopo una serie grigia e spesso l'inizio di un nuovo movimento.
  Attenzione a questa transizione — e uno dei segnali piu precoci.
```

---

## Integrazione dei 4 pannelli: il segnale composito

### Framework di lettura integrata

```
STEP 1: Classifica ogni pannello con un bias (BULL / BEAR / NEUTRO)
  P1 OI+Price:   OI e prezzo convergono rialzisti? -> BULL. Divergenza? -> BEAR/NEUTRO
  P2 L/S Ratio:  Contrarian al posizionamento attuale? -> segnale opposto al crowd
  P3 Liquidazioni: Chi sta soffrendo di piu? -> la direzione opposta ha edge
  P4 OI Delta:   Colore dominante nelle ultime 3-5 barre? -> direzione del capitale

STEP 2: Conta i bias
  4 BULL -> segnale molto forte rialzista
  3 BULL + 1 NEUTRO -> segnale rialzista, procedi
  2 BULL + 2 BEAR -> segnale misto, MONITOR
  3 BEAR + 1 NEUTRO -> segnale ribassista, procedi
  4 BEAR -> segnale molto forte ribassista

STEP 3: Pesa i pannelli in base al contesto
  In trend: P1 (OI+Price) e P4 (OI Delta) pesano di piu
  In inversione: P2 (L/S contrarian) e P3 (liquidazioni) pesano di piu
  In compressione: P4 (OI Delta) e P3 (dimensione liquidazioni) pesano di piu
```

### Le 5 letture composite piu comuni

```
LETTURA 1 — TREND RIALZISTA GENUINO:
  P1: OI e prezzo salgono insieme (convergenza)
  P2: L/S ratio scende o neutro (non crowding long estremo)
  P3: Short liquidazioni dominanti (squeeze in corso)
  P4: Dominanza barre verdi
  -> Azione: long con confidence alta, tieni la posizione
  -> Rischio principale: quando finiscono gli short da liquidare (P3 si esaurisce)

LETTURA 2 — RALLY ESAUSTO (vendere la forza):
  P1: DIVERGENZA — prezzo sale ma OI non conferma o scende
  P2: L/S ratio alto (> 1.8) e crescente — retail insegue il rialzo
  P3: Long liquidazioni iniziano ad apparire
  P4: Barre grigie o arancioni dopo serie verde
  -> Azione: non aggiungere long, valutar short con stop sopra ultimo massimo
  -> Questo era il pattern nel dashboard mostrato (zona DIVERGENCE)

LETTURA 3 — FLUSH LONG IN CORSO:
  P1: OI scende, prezzo scende
  P2: L/S ratio era alto, ora inizia a scendere (long si arrendono)
  P3: Barre rosse alte (long liquidazioni dominanti)
  P4: Barre grigie o arancioni
  -> Azione: non comprare "perche e sceso tanto". Aspetta fine del flush (P3 si esaurisce).
  -> Il flush finisce quando le barre rosse diventano piu piccole per 3+ candele.

LETTURA 4 — POTENZIALE INVERSIONE RIALZISTA:
  P1: OI scende ma prezzo smette di scendere (divergenza bullish)
  P2: L/S ratio basso (< 1.0) — retail ha capitolato
  P3: Long liquidazioni si esauriscono (barre rosse sempre piu piccole)
  P4: Prime barre verdi dopo dominanza grigia
  -> Azione: setup long ad alto potenziale. Confermare con livello GEX come supporto.

LETTURA 5 — DE-LEVERAGING NEUTRO:
  P1: OI scende, prezzo laterale
  P2: L/S ratio neutro (1.0-1.3)
  P3: Liquidazioni bilanciate o assenti
  P4: Dominanza barre grigie
  -> Azione: MONITOR. Il mercato si sta pulendo. La direzione arrivera dopo.
  -> Spesso precede un movimento direzionale significativo.
```

---

## Lettura del dashboard in foto (caso reale 26/03 16:24)

Ecco come si applica il framework al dashboard mostrato:

```
P1 — OI + PRICE:
  Zona DIVERGENCE evidenziata: prezzo era salito ma OI non confermava.
  OI a 48,282 BTC dopo aver toccato circa 49,571. In calo.
  Prezzo a $68,939 in discesa.
  -> BIAS: BEAR (divergenza bearish risolta al ribasso)

P2 — LONG/SHORT RATIO:
  Ratio 1.650 (L:62.3% S:37.7%) — zona overbought segnalata.
  Il retail era posizionato long in eccesso.
  -> BIAS: CONTRARIAN BEAR (troppi long = flush potenziale)

P3 — LIQUIDAZIONI 24h:
  L:269.7 / S:207.6 BTC — long liquidazioni > short liquidazioni.
  Le barre rosse dominano nella parte destra del grafico.
  Picco di short liq a sinistra (squeeze iniziale), poi inversione con long flush.
  -> BIAS: BEAR (mercato stava colpendo i long)

P4 — OI DELTA:
  Barre arancioni (OI+ Price-) visibili = nuovi short entrano.
  Barre grigie = de-leveraging dei long.
  Mancanza di barre verdi recenti.
  -> BIAS: BEAR (nuovo capitale entra short, de-leveraging long)

SEGNALE COMPOSITO: 4/4 BEAR
  Situazione chiara: divergenza OI risolta, retail over-long in flush,
  nuovi short si costruiscono. Il calo da $71K a $68.9K era strutturale.
```

---

## Output standardizzato

```
=== DERIVATIVES DASHBOARD — [Asset] | [data ora] ===

PANNELLO 1 — OI + PRICE:
  OI attuale:      [valore BTC/unita]
  Variazione OI:   [+/-% nelle ultime Xh]
  Combinazione:    [OI+/Price+ | OI+/Price- | OI-/Price+ | OI-/Price-]
  Divergenza:      [SI (da X candele) / NO]
  Bias P1:         [BULL / BEAR / NEUTRO]

PANNELLO 2 — L/S RATIO:
  Ratio attuale:   [valore] (L:[%] S:[%])
  Zona:            [OVERBOUGHT / NEUTRO / OVERSOLD]
  Dinamica:        [crescente / decrescente / stabile]
  Bias P2:         [CONTRARIAN BULL / CONTRARIAN BEAR / NEUTRO]

PANNELLO 3 — LIQUIDAZIONI 24h:
  Long liq:        [valore BTC]
  Short liq:       [valore BTC]
  Dominante:       [LONG FLUSH / SHORT SQUEEZE / BILANCIATO]
  Pattern attuale: [cluster / outlier / esaurito / assente]
  Bias P3:         [BULL / BEAR / NEUTRO]

PANNELLO 4 — OI DELTA:
  Colore dominante ultime 3-5 barre: [VERDE / ARANCIONE / GRIGIO]
  Sequenza:        [descrizione trend colori]
  Bias P4:         [BULL / BEAR / NEUTRO]

SEGNALE COMPOSITO:
  Score:           [N/4 BULL | N/4 BEAR | MISTO]
  Lettura:         [numero lettura composita 1-5 + nome]
  Confidenza:      [ALTA (4/4) / MEDIA (3/4) / BASSA (2/4 o misto)]

IMPLICAZIONI OPERATIVE:
  Posizioni long:  [tieni / riduci / chiudi / non aprire]
  Posizioni short: [tieni / riduci / chiudi / non aprire]
  Setup da cercare: [tipo di setup scalp compatibile con questo segnale]
  Rischio principale: [cosa potrebbe invalidare questa lettura]

INTEGRAZIONE CON GEX:
  [Come questo segnale derivati si combina con la struttura GEX attuale]
  [Convergenza o divergenza con la tesi in scratchpad]
```

---

## Lettura dei chart visivi (Volume Profile, GEX Profile, Analysis Chart)

Quando ricevi screenshot dei grafici `volume_profile.png`, `gex_profile.png`,
o `Xh_analysis.png`, carica il file di riferimento:

```
-> Leggi: references/chart-reading.md
```

Contiene la guida completa per:
- **Volume Profile**: lettura POC/VAH/VAL, buy vs sell dominance, pattern operativi
- **GEX Profile** (istogramma orizzontale): gamma+/gamma-, gamma flip, zero gamma
- **Analysis Chart** (1h/4h/15m): livelli di confluenza sovrapposti, StochRSI, volume
- **Integrazione 4 fonti**: come combinare VP + GEX Profile + Chart + Derivatives
- **5 pattern visivi ricorrenti** già nominati e operativi

**Quando caricare il riferimento:**
- Screenshot di `volume_profile.png` → sempre
- Screenshot di `gex_profile.png` → sempre
- Screenshot di `Xh_analysis.png` o `Xm_analysis.png` → sempre
- Menzione di "POC", "VAH", "VAL", "gamma flip", "zero gamma" → sempre
- Richiesta di lettura integrata multi-chart → sempre

**Caso reale incluso nel riferimento:**
La lettura del 26/03 @ 68,915 (prezzo sotto VAL in gamma-) è documentata
come esempio concreto in tutte e 3 le sezioni chart.

---

## Note operative rapide

```
QUANDO I DERIVATI CONTRADDICONO IL GEX:
  GEX dice "supporto a $X" ma derivati mostrano flush long in corso
  -> I derivati hanno la precedenza nel breve termine
  -> Il supporto GEX potrebbe reggere solo DOPO che il flush si esaurisce
  -> Aspetta P3 (liquidazioni) che si esaurisce prima di comprare il supporto

RATIO L/S IN DE-LEVERAGING (OI scende):
  Il ratio L/S perde affidabilita quando OI scende rapidamente
  (le posizioni si chiudono entrambe, il ratio fluttua senza senso)
  -> In forte de-leveraging, pesare meno P2 e piu P1 e P4

LIQUIDAZIONI COME TIMING:
  Un picco isolato di liquidazioni (outlier) spesso SEGNA il punto estremo
  del movimento in quella direzione — non sempre, ma spesso.
  -> Dopo un outlier di long liq: considera scalp long di rimbalzo tecnico
  -> Dopo un outlier di short liq: considera scalp short di pull-back

DIVERGENZA OI COME EARLY WARNING:
  La divergenza nel P1 appare PRIMA che il prezzo inverta.
  Non e un segnale di entry immediato — e un segnale di attenzione.
  -> Divergenza + L/S estremo + liquidazioni che cambiano = entry signal
  -> Divergenza da sola = non ancora, aspetta conferma degli altri pannelli
```
