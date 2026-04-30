---
name: price-alert-trigger
description: >
  Risposta rapida quando scatta un alert di prezzo impostato dal cron o dall'agent.
  Usa questa skill IMMEDIATAMENTE quando ricevi messaggi come: "alert triggerato",
  "prezzo ha toccato", "livello raggiunto", "trigger attivato", "alert BTC/ETH/NQ/GC",
  "price alert fired", o qualsiasi notifica che indica che il prezzo ha raggiunto
  un livello precedentemente monitorato. NON fare analisi completa gex-analysis —
  questa skill e progettata per risposta in secondi, non per analisi approfondita.
  Obiettivo: decidere in 60 secondi se tradare, aggiornare il trigger, o ignorare.
---

# Price Alert Trigger Skill

## Filosofia: velocita con contesto minimo

Quando scatta un alert, il prezzo E GIA al livello. Non c'e tempo per
un'analisi completa. Questa skill legge solo le fonti strettamente necessarie
e produce una decisione binaria in formato compatto.

**Regola d'oro: meglio non tradare un'opportunita che tradare senza contesto.**
Se dopo i passi rapidi il quadro non e chiaro, la risposta e MONITOR AGGIORNATO,
non forzare un trade.

---

## PASSO 0 — Lettura minima obbligatoria (< 60 secondi)

Leggi SOLO questi file, in quest'ordine:

```
1. scratchpad.json        [OBBLIGATORIO]
   -> active_thesis: qual era il trigger impostato e per quale motivo?
   -> active_positions: c'e gia una posizione aperta sullo stesso asset?
   -> last_trade_outcome: anti-tilt check (loss recente?)
   -> last_decision.action: cosa aveva deciso il cron?

2. context.json           [SEZIONE SPECIFICA: resistances/supports + lw_trend]
   -> Trova il livello triggerato nella lista resistances o supports
   -> Leggi il suo str score e GEX value
   -> Leggi lw_trend.bias per l'asset
   -> Leggi derivati: OI trend e L/S ratio (solo questi due)

3. lw_diff_history.md     [SOLO ULTIMA SEZIONE]
   -> Cosa e cambiato nelle ultime 1-2 sessioni su quel livello specifico?
   -> Il livello ha bid/ask nuovi o spariti recentemente?
```

NON leggere: confluence_history completa, retrospettive complete,
macro approfondita, chart screenshots. Quello e lavoro del cron.

---

## PASSO 1 — Classificazione immediata del trigger

### Tipo di alert
```
TIPO A — Long trigger (prezzo scende al livello di supporto monitorato)
  Il prezzo ha TOCCATO un supporto che il cron aveva impostato come entry long.
  Domanda: il supporto sta tenendo o sta cedendo?

TIPO B — Short trigger (prezzo sale al livello di resistenza monitorato)
  Il prezzo ha TOCCATO una resistenza che il cron aveva impostato come entry short.
  Domanda: la resistenza sta tenendo o sta cedendo?

TIPO C — Breakout trigger (prezzo chiude SOPRA resistenza o SOTTO supporto)
  Il livello e stato rotto, non solo toccato.
  Domanda: e un breakout reale o un falso segnale?

TIPO D — Invalidazione trigger (prezzo ha attraversato il livello di invalidazione)
  La tesi attiva e stata invalidata.
  Azione immediata: NON tradare, aggiornare scratchpad, notificare.
```

---

## PASSO 2 — Checklist rapida (5 domande, risposta si/no)

```
DOMANDA 1: Il livello triggerato ha str > 7.0 nel context.json?
  SI -> livello strutturalmente valido, procedi
  NO -> livello debole, rischio alto. Default: MONITOR AGGIORNATO

DOMANDA 2: Il LW trend e allineato alla direzione del trade ipotetico?
  (Long trigger -> lw_trend.bias dovrebbe essere BULLISH o NEUTRO)
  (Short trigger -> lw_trend.bias dovrebbe essere BEARISH o NEUTRO)
  SI -> conferma, procedi
  NO -> conflitto, ATTENZIONE. Richiede volume spike per procedere.

DOMANDA 3: OI e in aumento o stabile? (NON in calo)
  SI -> partecipazione presente, procedi
  NO -> de-leveraging attivo. Stop devono essere > 1.5%. Size ridotta.

DOMANDA 4: Nell'ultima sessione LW diff, il livello triggerato ha
  bid/ask ancora in posizione (non spariti)?
  SI -> struttura intatta, procedi
  NO -> struttura si e alleggerita. Alta probabilita di through del livello.

DOMANDA 5: Anti-tilt check: ultima loss < 2 sessioni fa?
  NO (nessuna loss recente) -> size normale
  SI -> size ridotta al 80% automaticamente
```

**Scoring:**
- 5/5 SI -> TRADE con size normale
- 4/5 SI -> TRADE con size ridotta (-20%)
- 3/5 SI -> SCALP CONDIZIONALE (vedi PASSO 3)
- < 3/5 SI -> MONITOR AGGIORNATO (vedi PASSO 4)

---

## PASSO 3 — Verifica segnale tecnico (solo se score >= 3/5)

Il segnale tecnico e l'unica cosa che l'alert non puo dirti da solo.
Hai bisogno di guardare il grafico o ricevere i dati OHLCV.

```
SEGNALE FORTE (procedi con trade):
  Wick di rigetto sul livello con chiusura lontana dal livello
  + StochRSI in zona estrema (< 20 per long, > 80 per short)
  + Candela di conferma nella direzione del trade

SEGNALE DEBOLE (scalp condizionale, size minima):
  Prezzo sul livello ma candele ancora direzionali contro di te
  + StochRSI non estremo
  -> Entry solo se il prezzo fa un micro-rimbalzo confermato

NESSUN SEGNALE (non tradare):
  Prezzo attraversa il livello senza rimbalzo
  Candele aggressive nella direzione opposta
  -> Il livello sta cedendo. Aggiorna trigger al prossimo livello.
```

---

## PASSO 4 — Albero decisionale completo

```
ALERT SCATTATO
      |
      v
[TIPO D - Invalidazione?] -> SI -> CHIUDI POSIZIONE SE APERTA
      |                            AGGIORNA SCRATCHPAD
      | NO                         NOTIFICA: "Tesi invalidata"
      v
[Score checklist] -----> < 3 -> MONITOR AGGIORNATO
      |                          (definisci nuovo trigger)
      | >= 3
      v
[Segnale tecnico?] ----> NESSUNO -> MONITOR AGGIORNATO
      |
      | FORTE o DEBOLE
      v
[Tipo alert?]
      |
      +-> TIPO A (long support) -> LONG entry
      |
      +-> TIPO B (short resistance) -> SHORT entry
      |
      +-> TIPO C (breakout) -> [sottocaso]
                  |
                  +-> Breakout rialzista + score >= 4 + OI up -> LONG breakout
                  |
                  +-> Breakout ribassista + score >= 4 + OI up -> SHORT breakdown
                  |
                  +-> Score < 4 -> WAIT: aspetta retest del livello rotto
```

---

## PASSO 5 — Formato output (compatto, non narrativo)

```
=== ALERT TRIGGER — [Asset] @ $[prezzo] | [ora CET] ===

TIPO:         [A/B/C/D]
LIVELLO:      $[X] | str [Y] | GEX [+-ZM]
LW DIFF:      [bid/ask stato sul livello]
CHECKLIST:    [N]/5 SI  ([elenco sintetico delle 5 risposte])
SEGNALE TEC:  [FORTE / DEBOLE / ASSENTE]

DECISIONE:    [TRADE LONG / TRADE SHORT / SCALP COND. / MONITOR AGG. / INVALIDA]

SE TRADE:
  Entry:      $[X] (market / limit a $Y)
  Stop:       $[X] ([distanza%] — [motivo])
  Target 1:   $[X] ([livello confluence str>Y])
  Target 2:   $[X] (opzionale, se vacuum zone ampia)
  Size:       [normale / -20% anti-tilt / -50% segnale debole]
  Leva:       [da risk_config — aggiustata per ATR]
  Motivazione: [1 riga — perche questo trade ha edge ora]

SE MONITOR AGGIORNATO:
  Motivo:     [perche non si entra]
  Nuovo trigger LONG:  $[X] + [condizione tecnica]
  Nuovo trigger SHORT: $[X] + [condizione tecnica]
  Scadenza trigger:    [sessione / 4h / daily]

SE INVALIDAZIONE:
  Tesi precedente: [sintetico]
  Livello ceduto:  $[X]
  Azione:         [chiudi posizione / annulla ordini pendenti]
  Nuova struttura: [prossimo livello rilevante in entrambe le direzioni]
```

---

## PASSO 6 — Casistica breakout (TIPO C) — dettaglio

Il breakout e il caso piu pericoloso perche puo essere reale o falso.

### Breakout REALE (entra in direzione)
```
SEGNALI CONTEMPORANEI:
  Chiusura candela 15m/1h SOPRA il livello (non solo wick)
  Volume nella candela di breakout > media ultimi 20 periodi
  LW diff: bid nuovi sopra il livello (buyer si riposizionano sopra)
  OI in aumento nella stessa sessione

ENTRY:  Non inseguire. Aspetta il primo pullback/retest del livello rotto.
        Il livello rotto diventa supporto (gamma flip) — li si entra.
STOP:   Sotto il livello rotto (ora supporto)
TARGET: Prossimo livello confluence nella vacuum zone
```

### Breakout FALSO (opportunita di contro-trade)
```
SEGNALI CONTEMPORANEI:
  Wick sopra il livello ma chiusura sotto (rejection)
  Volume nella candela di breakout < media (bassa partecipazione)
  LW diff: ask ancora in posizione sul livello (non spariti)
  OI piatto o in calo

ENTRY:  Short/long nella direzione opposta al breakout fallito
STOP:   Sopra/sotto il massimo/minimo del wick
TARGET: Livello gamma+ precedente (verso cui rimbalza)
NOTA:   Questo e un setup ad alta probabilita — il falso breakout
        in zona gamma+ con volume basso e uno dei pattern piu affidabili
```

### WAIT — breakout ambiguo
```
QUANDO:
  Chiusura sul livello (ne sopra ne sotto chiaramente)
  Volume medio (ne spike ne assente)
  LW non da segnale chiaro

AZIONE:
  Non tradare. Imposta due trigger:
  -> Conferma breakout: chiusura 1h sopra $[X+0.3%]
  -> Rejection: ritorno sotto $[X-0.3%]
  Il mercato chiarira la direzione nella candela successiva.
```

---

## PASSO 7 — Gestione alert multipli simultanei

Quando piu alert scattano nella stessa sessione (es. BTC e ETH entrambi
toccano i loro livelli):

```
PRIORITA DI ELABORAZIONE:
1. Invalidazioni (TIPO D) -> sempre prima, su qualsiasi asset
2. Asset con posizione aperta -> gestione posizione esistente prima
3. Asset con score checklist piu alto -> elabora prima
4. Se score uguale -> elabora l'asset con str livello piu alta

REGOLA CORRELAZIONE:
  BTC e ETH in genere correlati. Se BTC da segnale SHORT ma ETH
  da segnale LONG contemporaneamente -> ATTENZIONE, divergenza rara.
  In questo caso: size dimezzata su entrambi, o MONITOR su entrambi.

MAX POSIZIONI SIMULTANEE:
  Rispetta max_trade dal risk_config (tipicamente 4 posizioni max).
  Se gia a max -> il nuovo alert diventa automaticamente MONITOR AGGIORNATO.
```

---

## PASSO 8 — Aggiornamento scratchpad post-decisione

Dopo ogni alert elaborato, aggiorna scratchpad.json:

```json
{
  "last_decision": {
    "asset": "[asset]",
    "action": "TRADE|MONITOR|INVALIDAZIONE",
    "reason": "[motivo specifico in max 20 parole]",
    "timestamp": "[ISO8601]",
    "by_agent": "price-alert-trigger"
  }
}
```

Se TRADE: aggiungi entry in active_positions.
Se MONITOR AGGIORNATO: aggiorna active_thesis con nuovi trigger.
Se INVALIDAZIONE: rimuovi tesi da active_thesis, aggiorna bias a NEUTRO.

NON scrivere retrospettiva completa — quello e compito del cron gex-analysis
che legge il context aggiornato nella sessione successiva.

Scrivi solo una nota sintetica in scratchpad.notes:
```json
{
  "ts": "[ISO8601]",
  "by_agent": "price-alert-trigger",
  "text": "Alert [tipo] su [asset] @ $[prezzo]. [Decisione]. [Motivo 10 parole]."
}
```

---

## Casi limite e regole di safety

```
POSIZIONE GIA APERTA NELLA STESSA DIREZIONE:
  Non aggiungere size sullo stesso trade (no averaging up/down)
  Alert diventa: verifica se lo stop va aggiornato (trailing)
  -> Se il prezzo si muove favorevolmente: aggiorna stop al breakeven

POSIZIONE GIA APERTA NELLA DIREZIONE OPPOSTA:
  Questo e un segnale di invalidazione parziale.
  NON aprire posizione contraria senza chiudere prima quella aperta.
  Valuta: 1) chiudi tutto e rientra, 2) mantieni con stop piu stretto

ALERT SCATTATO DURANTE ORARIO LOW LIQUIDITY:
  (BTC: 02:00-06:00 UTC | Futures: fuori RTH)
  Score richiesto sale da 3/5 a 4/5 per procedere con trade.
  Volume spike richiesto sale da 2x a 3x media.
  I livelli GEX sono meno affidabili con liquidita ridotta.

ALERT SCATTATO <30 MIN PRIMA DI EVENTO MACRO HIGH IMPACT:
  Leggi hrs_to_next_event da context.json.
  Se < 0.5h -> NON tradare. Aspetta il comunicato.
  Se tra 0.5h e 2h -> Size dimezzata, stop allargato del 50%.

ALERT SCATTATO DURANTE SESSIONE CON LOSS GIA REALIZZATA:
  Anti-tilt automatico: size -20% anche se score e 5/5.
  Non e punizione, e protezione dal revenge trading.
```

---

## Checklist rapida di riferimento (stampa mentale)

```
[ ] Qual era il trigger impostato e perche? (scratchpad)
[ ] Il livello ha str > 7? (context.json resistances/supports)
[ ] LW trend allineato? (context.json lw_trend)
[ ] OI non in calo? (context.json derivatives)
[ ] LW diff recente non mostra struttura ceduta? (lw_diff_history ultima sezione)
[ ] Anti-tilt: loss recente? (scratchpad last_trade_outcome)
[ ] Segnale tecnico presente? (dati OHLCV / grafico)
[ ] Orario / evento macro / posizioni aperte? (context.json)
-> Score e decisione in < 60 secondi
```
