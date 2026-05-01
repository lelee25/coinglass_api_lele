---
name: gex-analysis
description: >
  Analisi completa del Gamma Exposure (GEX) per asset finanziari (BTC, ETH, NQ, ES, GC).
  Usa questa skill ogni volta che l'utente fornisce dati GEX, livelli di opzioni, gamma wall,
  o chiede una lettura del mercato basata su posizioni in opzioni e market maker hedging.
  Trigger: "analizza il GEX", "leggi i livelli", "cosa faranno i market maker", "dove va il prezzo",
  "interpreto questi livelli", "gamma wall", "gamma exposure", "supporti e resistenze opzioni",
  "prossimo movimento", "analisi strutturale", confronto tra sessioni GEX diverse.
  Attiva anche quando ricevi dati da confluence_history, lw_diff_history, scratchpad, context.json
  o retrospettive. Questa skill produce analisi ragionate multi-sorgente, previsioni con logica
  meccanica spiegata, confronti storici tra sessioni e outcome osservati.
---

# GEX Analysis Skill — Full Pipeline

## PASSO 0 — Lettura contesto completo

**Prima di qualsiasi analisi, leggi in quest'ordine:**

```
1. retrospettive.md        → osservazioni passate, pattern emersi, outcome reali
2. scratchpad.json         → tesi attiva, ultima decisione, posizioni aperte
3. context.json            → macro, derivati, LW trend, portfolio, livelli confluence
4. lw_diff_history.md      → cambiamenti recenti nelle liquidity walls
5. confluence_history.md   → livelli GEX x LW con strength score
```

Le retrospettive sono **dati storici pesati**, non regole. Pattern con 4+ casi simili:
pesali fortemente. Con 1-2 casi: usali come indizio, non come legge.

---

## Architettura dati: cosa fa ogni fonte

### GEX (Pine Script / array prices+values)
La struttura gamma delle opzioni. Dice **dove** i MM sono obbligati a hedgiarsi.
- Gamma+ (verde): MM vende quando sale, compra quando scende -> freno, magnete
- Gamma- (arancione): MM amplifica il movimento -> acceleratore
- Ordine array: sorted per importanza decrescente (indice 0 = piu rilevante)

### Confluence History (confluence_history.md)
GEX incrociato con Liquidity Walls. Ogni livello ha:
```
prezzo | tipo | str (0-10) | GEX value | LW side | LW width
```
La `strength` e il numero piu importante: combina GEX + LW in un unico score.
- str > 9.0 -> livello strutturale della settimana, raramente perforato
- str 7-9   -> livello significativo, alta probabilita di reazione
- str < 6   -> livello secondario, usare solo in confluenza con altri segnali

### LW Diff History (lw_diff_history.md)
Cambiamenti nelle liquidity walls tra sessioni. Radar in tempo reale del
riposizionamento dei grandi player.

```
BID SPARITI   -> compratori si ritirano (debolezza)
BID NUOVI     -> compratori si posizionano (supporto in costruzione)
ASK SPARITI   -> venditori si ritirano (resistenza si alleggerisce)
ASK NUOVI     -> venditori si posizionano (resistenza in costruzione)
```

Pattern chiave:
- Bid spariti + ask nuovi = pressione ribassista
- Ask spariti + bid nuovi = pressione rialzista
- Entrambi i lati si rafforzano = COMPRESSIONE -> breakout imminente
- Entrambi i lati si alleggeriscono = LIQUIDITA IN USCITA -> volatilita imminente

### LW Trend (context.json)
Sintesi delle ultime N sessioni:
```json
{
  "bias": "BEARISH|BULLISH|COMPRESSO|NEUTRO",
  "net_bid": -6,   // positivo = buyer si rafforzano
  "net_ask": +5,   // positivo = seller si rafforzano
  "price_direction": "FALLING|RISING|STABLE"
}
```
Quando price_direction e bias si confermano = trend coerente, edge alto.
Quando divergono (prezzo sale ma LW bearish) = fake move probabile.

### Derivati (context.json -> derivatives_coinalyze)
```
L/S ratio:
  > 2.0  = CROWDING LONG ESTREMO -> rischio flush long, contrarian bearish
  1.5-2.0 = sbilanciamento moderato
  0.7-1.5 = zona neutrale
  < 0.7  = crowding short -> rischio squeeze

OI trend 24h:
  crescente = partecipazione in aumento -> conferma movimento
  calante   = de-leveraging -> fake breakout risk elevato

Liquidazioni 7 giorni:
  liq_long >> liq_short per piu giorni = sell-off strutturale long
  liq_short >> liq_long per piu giorni = squeeze strutturale
```

### Macro (context.json -> macro_values + hidden_links)
```
DXY forte + liquidita in contrazione = headwinds su BTC/risk assets
  -> I bounce tecnici sono piu deboli
  -> I breakdown sono piu veloci
  -> Stop < 1% vengono falciati prima del move (osservato 2+ volte)

DXY debole + liquidita in espansione = tailwinds
  -> I gamma wall rialzisti si rompono piu facilmente
  -> Il magnete settimanale GEX e piu affidabile
```

### Scratchpad (scratchpad.json)
Bridge tra sessioni. Contiene:
- active_thesis.btc/eth -> tesi operativa con confidence e key_levels
- last_decision         -> ultima azione (TRADE/MONITOR/NO_TRADE) e reason
- active_positions      -> posizioni aperte (cambiano il ragionamento)
- last_trade_outcome    -> risultato ultimo trade (considera per anti-tilt)
- notes                 -> ragionamenti recenti degli agent

### Retrospettive (retrospettive.md)
Osservazioni empiriche da sessioni reali. Ogni entry:
- Contesto in cui e stata fatta
- Outcome reale
- Counterfactual (cosa sarebbe successo con scelte diverse)
- Osservazione distillata

---

## PASSO 1 — Costruzione mappa strutturale

```
=== MAPPA STRUTTURALE [asset] @ $[prezzo] ===

RESISTENZE (sopra, ordine crescente):
  $[prezzo]  str [X.X]  GEX [+-XM]  LW-ask [W]  tipo [...]  +[X%]

--- PREZZO: $[X] --- [posizione vs struttura] ---

SUPPORTI (sotto, ordine decrescente):
  $[prezzo]  str [X.X]  GEX [+-XM]  LW-bid [W]  tipo [...]  -[X%]

AMBIENTE:  [GAMMA+ / GAMMA- / MISTO / VACUUM ZONE]
LW TREND:  [BEARISH/BULLISH/COMPRESSO] net_bid:[N] net_ask:[N]
DERIVATI:  OI [trend] | L/S [ratio] | [regime]
MACRO:     [headwind/tailwind/neutro]
```

---

## PASSO 2 — Lettura integrata a cascata

```
DOMANDA 1: Ambiente GEX?
  Gamma+ sopra = scala di freni
  Gamma- sotto = scala di acceleratori
  Vacuum zone = velocita libera

DOMANDA 2: LW trend conferma o contraddice il GEX?
  GEX rialzista + LW BULLISH = massima convergenza, edge alto
  GEX rialzista + LW BEARISH = i grandi player si spostano contro
  LW COMPRESSO = breakout imminente, attendere conferma direzione

DOMANDA 3: Derivati supportano il movimento?
  OI crescente + movimento = partecipazione reale, edge alto
  OI calante + movimento = de-leveraging, movimento fragile
  L/S > 2.0 = flush risk imminente nella direzione del crowd

DOMANDA 4: Macro headwind o tailwind?
  DXY forte + liquidita down = ogni long richiede conferma derivati
  Questo regime aumenta il tasso di fake breakout

DOMANDA 5: Tesi attiva (scratchpad) ancora valida?
  Confronta livelli di invalidazione con struttura attuale
  Se il prezzo ha superato l'invalidazione, la tesi e obsoleta

DOMANDA 6: Retrospettive segnalano pattern simile?
  Cerca contesti analoghi: stesso regime macro + struttura GEX + derivati
  3+ casi simili con outcome coerente = peso primario nell'analisi
```

---

## PASSO 3 — Strength score composito

```
GEX_weight:
  > 20M assoluto -> 4/4 (muro principale)
  10-20M         -> 3/4 (significativo)
  5-10M          -> 2/4 (valido)
  < 5M           -> 1/4 (secondario)

LW_weight (da confluence_history):
  str > 9.0 -> strutturale della settimana
  str 7-9   -> significativo
  str < 6   -> secondario

macro_modifier:
  DXY forte + liquidita down:
    -> livelli gamma+ RIALZISTI pesano -20% (meno efficaci)
    -> livelli gamma- RIBASSISTI pesano +20% (piu pericolosi)

deriv_modifier:
  OI calante -> tutti i livelli pesano -15% (de-leveraging ignora struttura)
  L/S crowding estremo -> aggiunge rischio flush nella direzione del crowd
```

---

## PASSO 4 — Cascata decisionale obbligatoria

```
STEP A — SWING CHECK (tutte le condizioni devono essere vere):
  [ ] Struttura GEX favorevole alla direzione
  [ ] LW trend allineato
  [ ] OI crescente (partecipazione confermata)
  [ ] Macro non contrarian
  [ ] L/S non in crowding estremo nella direzione del trade
  -> Se tutte vere: SWING. Se anche 1 falsa: NO SWING -> STEP B

STEP B — SCALP CHECK:
  [ ] Livello confluente (str > 7.0) vicino al prezzo (< 0.5%)
  [ ] Segnale tecnico: StochRSI estremo + wick rejection O Bollinger squeeze
  [ ] Volume relativo confermato
  [ ] Prezzo NON nel mezzo del range
  -> Se vere: SCALP size ridotta. Se anche 1 falsa: NO SCALP -> STEP C

STEP C — MONITOR:
  Definisci trigger specifici e binari:
  -> LONG trigger: [prezzo] + [segnale tecnico] + [condizione derivati]
  -> SHORT trigger: [prezzo] + [segnale tecnico] + [condizione derivati]
  -> Invalidazione esplicita per entrambi
```

---

## PASSO 5 — I 5 scenari operativi

### A — Long guidato da gamma+ (piu affidabile)
```
CONDIZIONI OTTIMALI:
  Prezzo sotto cluster gamma+ denso (str > 7 cumulativo)
  Vacuum zone tra prezzo e target
  LW BULLISH (net_bid positivo)
  OI crescente
  L/S neutro o contrarian bearish (squeeze potenziale)

ENTRY:  Rimbalzo su livello gamma+ str > 7 con wick + StochRSI < 20
TARGET: Gamma wall principale (verificare su confluence_history)
STOP:   Sotto il livello di supporto con STR piu alta
SIZE:   Piena se macro tailwind + OI up. Ridotta se macro headwind.
```

### B — Short al gamma wall (rimbalzo)
```
CONDIZIONI:
  Prezzo attacca grande gamma wall (GEX > 15M o str > 8)
  Volume DECRESCENTE nell'avvicinamento
  LW: ask wall ancora in posizione (non spariti in sessione recente)
  OI piatto o in calo

ENTRY:  Wick al livello + candela di rifiuto (doji, shooting star)
TARGET: Livello gamma+ precedente
STOP:   Chiusura oraria sopra il livello + 0.3%
NOTA:   Se LW mostra ask SPARITI recentemente -> rischio breakout, non shortare
```

### C — Breakout reale del gamma wall
```
CONDIZIONI:
  Prezzo rompe gamma wall con chiusura oraria sopra senza wick rientro
  Volume SPIKE 2-3x media
  LW: bid nuovi sopra il livello appena rotto (buyer si riposizionano sopra)
  OI in aumento

ENTRY:  Chiusura confermata sopra (NON anticipare)
TARGET: Prossimo gamma wall nella vacuum zone
STOP:   Rientro sotto il livello rotto
NOTA:   In vacuum zone ampia (> 3%), il 50-80% del range si percorre
        nelle prime 2-4 candele. Non aspettare pullback.
```

### D — Accelerazione in gamma- (pericoloso)
```
REGOLE ASSOLUTE:
  Non comprare "perche ha rimbalzato qui ieri" (gamma- trap)
  Non usare stop < 1.5% (vedi retrospettiva 24/03)
  Non inseguire il movimento con entry ritardata

  Se short: ride il movimento, stop ampi
  Se vuoi long: aspetta uscita confermata dalla zona gamma-
```

### E — Monitor in compressione
```
QUANDO:
  Prezzo nel mezzo tra livelli
  LW COMPRESSO
  Derivati non danno segnale direzionale
  Macro headwinds presenti

OSSERVAZIONE DOCUMENTATA (4+ casi):
  In compressione + headwinds, il MONITOR con trigger binari
  ha battuto sistematicamente l'anticipazione.
  Non e passivita, e gestione dell'incertezza.

TRIGGER DA DEFINIRE (specifici e binari):
  LONG: [prezzo] + [segnale tecnico] + [condizione derivati]
  SHORT: [prezzo] + [segnale tecnico] + [condizione derivati]
```

---

## PASSO 6 — Lettura del cambiamento tra sessioni

### LW diff (pattern operativi)
```
BULLISH ROTATION:
  + Bid nuovi su livelli sopra il prezzo (buyer si posizionano in anticipo)
  + Ask spariti in resistenza (seller abbandonano la difesa)
  + Pattern confermato per 2+ sessioni = strutturale

BEARISH ROTATION:
  + Bid spariti su supporti (buyer si ritirano)
  + Ask nuovi appena sopra (seller anticipano ribasso)
  + Pattern per 2+ sessioni = strutturale

COMPRESSIONE:
  + Entrambi i lati si rafforzano simultaneamente
  + Tipico pre-catalizzatore
  + Attendere conferma prima di posizionarsi

LIQUIDITA IN USCITA:
  + Sia bid sia ask spariscono
  + Volatilita imminente, slippage elevato
  + Non operare fino a struttura ricostruita
```

### GEX session-to-session
```
STRUTTURA CONFERMATA -> continuazione strutturalmente supportata

GAMMA WALL SPARITO:
  Meno attrito in quella zona
  Se era il muro principale -> rivedere target e struttura

GAMMA WALL NUOVO:
  Gamma+ sopra = nuovo tetto
  Gamma- sopra = copertura al ribasso, segnale bearish
  Gamma+ sotto = nuovo pavimento (acquisto istituzionale)

SPOSTAMENTO GAMMA WALL (es. 75K -> 77K):
  Magnete si e spostato in alto -> target aumentato -> bullish

INVERSIONE COMPLETA:
  Riposizionamento massiccio -> alta volatilita -> ridurre size
```

---

## PASSO 7 — Anti-tilt e size management

```
DOPO LOSS CONSECUTIVI:
  Ridurre size al 80% (anti-tilt)
  Fino a 1 trade profittevole prima di tornare a size piena
  [Documentato nelle retrospettive]

STOP IN REGIME DI DE-LEVERAGING (OI down + macro bearish):
  Osservazione documentata (2+ casi): wick superano stop < 1% sistematicamente
  -> Stop minimo 1.5%, o ridurre size per compensare

SCALP COUNTER-TREND CON MACRO HEADWIND:
  "Close 15m" non e sufficiente come unico segnale
  Richiedere OI up O L/S squeeze come filtro obbligatorio
  [Retrospettiva 24/03 14:46]
```

---

## PASSO 8 — Counterfactual (obbligatorio)

Ogni decisione deve includere il counterfactual:

```
FORMAT:
  "Se avessi [azione alternativa] con entry [prezzo], SL [prezzo], TP [prezzo]:
   -> Il prezzo ha poi fatto [X]
   -> Sarebbe stato: TP_HIT / SL_HIT / OPEN
   -> Classificazione: OPPORTUNITA COLTA / MANCATA / NEUTRO / CORRETTA ASTENSIONE"

PERCHE E OBBLIGATORIO:
  Permette di distinguere "MONITOR corretto" (mercato non ha fatto niente)
  da "MONITOR errato" (c'era un movimento chiaro che non ho sfruttato).
  Senza counterfactual, il MONITOR diventa alibi per inattivita.
```

---

## PASSO 9 — Formato output standardizzato

```
### ANALISI GEX — [Asset] @ $[prezzo] | [data ora CET]

=== MAPPA STRUTTURALE ===
[livelli sopra: prezzo | str | GEX | LW | distanza%]
--- PREZZO: $[X] | [posizione] ---
[livelli sotto: prezzo | str | GEX | LW | distanza%]

=== AMBIENTE ===
GEX:      [tipo ambiente]
LW:       [bias] (net_bid:[N] net_ask:[N])
DERIVATI: OI [trend] | L/S [ratio] | [regime]
MACRO:    [sintesi headwind/tailwind]

=== CAMBIAMENTO DA SESSIONE PRECEDENTE ===
[LW diff rilevante - cosa e sparito/apparso]
[GEX struttura - livelli nuovi/spariti]
[Interpretazione riposizionamento]

=== CASCATA DECISIONALE ===
SWING:  [SI/NO - motivo specifico]
SCALP:  [SI/NO/CONDIZIONALE - motivo]
-> DECISIONE: [TRADE long/short | MONITOR | NO_TRADE]

=== SCENARI ===
PRINCIPALE ([X]% prob stimata):
  Trigger:       [cosa deve succedere - specifico]
  Meccanica:     [perche MM + LW + derivati si comportano cosi]
  Entry zone:    [$X - $Y]
  Target:        [$Z - livello confluence str>X]
  Stop:          [$W - sotto/sopra livello str>X]
  Invalidazione: [condizione specifica]

ALTERNATIVO ([Y]% prob stimata):
  [struttura per direzione opposta]

=== RETROSPETTIVE APPLICABILI ===
[Pattern storico rilevante - data + contesto + applicazione]
[Se nessuno: "Nessun pattern storico direttamente comparabile"]

=== COUNTERFACTUAL ===
[Verifica tesi precedente se presente in scratchpad]

=== LIVELLI DA MONITORARE ===
CRITICO SOPRA: $[X] (str [Y], tipo, motivo)
CRITICO SOTTO: $[X] (str [Y], tipo, motivo)

=== SINTESI ===
[3 frasi: struttura attuale, scenario piu probabile, cosa fare/non fare ora]
```

---

## PASSO 10 — Scrittura retrospettiva

**Dopo ogni analisi con decisione operativa, scrivi entry in retrospettive.md:**

```markdown
### [DATA] [ORA] — sessione gex-analysis ([tipo])
- **Tesi precedente**: [da scratchpad o MONITOR precedente]
- **Contesto chiave**: [prezzo, macro, derivati, LW bias]
- **GEX aggiornato**: [net GEX, livello chiave attorno al prezzo]
- **Cascata decisione**: [SWING NO/SI -> SCALP NO/SI -> decisione]
- **Counterfactual**: [azione alternativa -> outcome -> classificazione]
- **Osservazione**: [pattern distillato, applicabile a sessioni future]
```

Scrivere retrospettiva ANCHE per MONITOR. I casi di astensione corretta
sono importanti quanto i trade per calibrare i criteri nel tempo.

---

## Errori documentati dalle retrospettive

```
Stop < 1% in OI down + macro bearish:
  I wick sono 1.5-2x la norma. Stop minimo 1.5% o size ridotta.
  [Retrospettiva 24/03 13:24]

"Reclaim con close 15m" senza OI up:
  Non sufficiente per long counter-trend. OI up = filtro obbligatorio.
  [Retrospettiva 24/03 14:46]

Long su breakout con OI calo + LW svuotamento:
  OI down = breakout probabilmente falso. Aspettare close 1h o rejection.
  [Retrospettiva 24/03 10:26]

Gamma- confuso con supporto:
  Il gamma- amplifica. Se rimbalza e per altri motivi. Non shortare/comprare
  aspettandosi comportamento da supporto/resistenza classica.

Operare nel mezzo del range con LW compresso:
  La direzione non e ancora determinata. MONITOR batte anticipazione (4+ casi).
  [Multipli casi 20-24/03]

Livelli GEX di 3+ giorni fa usati come attuali:
  Il GEX si aggiorna ogni giorno. Analisi su livelli vecchi e obsoleta.
```

---

## Glossario sintetico

| Termine | Fonte | Significato operativo |
|---|---|---|
| Gamma wall | GEX | Livello con GEX assoluto molto alto - massimo attrito |
| Gamma flip | GEX | Livello gamma+ superato diventa supporto |
| Vacuum zone | GEX | Gap tra livelli - velocita libera |
| str | Confluence | Score GEX x LW su 10. > 9 = strutturale, > 7 = significativo |
| LW diff | LW History | Variazione bid/ask walls - radar del riposizionamento |
| Net bid/ask | LW Trend | Somma bid/ask aggiunti-rimossi. Positivo = rafforzamento |
| Crowding | Derivati | L/S > 2.0 o < 0.7 - flush risk elevato |
| De-leveraging | Derivati | OI in calo - fake breakout probabile |
| Pin risk | GEX | Chiusura sul gamma wall alla scadenza venerdi |
| Anti-tilt | Retrospettive | Size ridotta (80%) dopo loss consecutivi |
| Counterfactual | Retrospettive | Simulazione alternativa non eseguita |

---

## Cross-reference con le altre skill

```
LETTA DA QUESTA SKILL (input contestuale):
  context.macro_regime          <- macro-regime-monitor (modifier slow)
  context.etf_signal            <- etf-flow-interpreter (modifier strategico)
  context.funding_signal        <- funding-arb-detector (cost-aware + signal)
  scratchpad.whale_alerts       <- whale-onchain-monitor (early warning)
  calibration.asset_thresholds  <- references/calibration-thresholds.md

  -> Applicare i modifier nella PASSO 3 (strength score composito):
     edge_finale = edge_base * macro_regime.long_w * etf_signal.long_w * size_factor

DELEGA A (sub-skill chiamabili):
  derivatives-dashboard         (lettura completa derivati invece del PASSO 0 minimale)
  chart-pattern-recognition     (riconoscimento pattern visivi + reference)
  scalp-execution               (se cascata SWING NO -> SCALP CHECK)

SCRIVE:
  context.json (resistances, supports, lw_trend aggiornati)
  scratchpad.json.active_thesis (tesi operativa con confidence + key_levels)
  retrospettive.md (ogni decisione con counterfactual)
  confluence_history.md (livelli GEX × LW con strength score)

NOTA SU CALIBRAZIONE:
  Le soglie hardcoded (str>9, str>7, GEX>20M) sono BASE.
  Se calibration.json esiste, sovrascrivile con i percentile rolling 30gg
  (vedi references/calibration-thresholds.md per il framework completo).
```
