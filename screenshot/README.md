# Frontend Screenshots — tradevalue / gex-agentkit

Screenshot del frontend `hub.lele-tradevalue.com` catturati il 30 aprile 2026.
Servono al Claude Code remoto (sul mini-PC server) per capire lo stato visivo
attuale del prodotto, individuare incoerenze e applicare i fix descritti
in `FRONTEND-ISSUES.md` (sezione finale di questo file).

## Identità mostrata negli screenshot — non sono bug

- `montalto36@gmail.com` accanto a "ChatGPT" / "Codex Account" è l'**OAuth**
  con cui l'utente collega il provider ChatGPT (Plus subscription via Codex).
  È **corretto** che sia diverso dall'email di login.
- `leleciol8@gmail.com` è l'email con cui l'utente si **logga al sistema**
  (auth proprietaria del frontend). È **corretto** che venga mostrata.

## Mappa screenshot

| File | Vista | Cosa mostra |
|---|---|---|
| `01-hub-overview.png` | HUB (top) | Header `TRADEVALUE · gex-agentkit`, nav `HUB / CHARTS / MACRO / SETTINGS / ADMIN`, badge `PLUS · 5H:99% · WK:98%`, badge `CHATGPT LINKED`, terminal greeting "Buonasera, Leleciol8@Gmail Com.", payoff "One bus, three agents, zero polling…", chip `BTC NEUTRAL` / `ETH SHORT`, sidebar destra `CHATGPT`/`SSE LIVE`/`TENANT default`, KPI tiles (Open Trades, Alert Levels, Last Trade, Last Event, Events Buffered, SSE State), inizio sezione "Agent Constellation". |
| `02-hub-agent-constellation-live-stream.png` | HUB (mid) | Tre card agenti: `JARVIS · MAIN`, `GEX ANALYSIS · gex-analysis`, `MACRO MASTER · macro-master`, ognuno con bottone `DASHBOARD →`. Sezione `LIVE EVENT STREAM` con `RECENT EVENTS · 0 buffered · no data · No events yet — daemons are quiet`. Inizio sezione `Alert levels` (28 levels) con filtri ALL/BTC/ETH e ≥5/≥7/≥9, tabella ETH (price, direction, label, strength, action, cooldown, source). |
| `03-hub-alert-levels-btc-trades-ledger.png` | HUB (bottom) | Continuazione tabella alert con righe BTC (range 76.700 → 78.500), poi `Trades ledger · 0 OPEN`, `QUICK ACTIONS · 4 ACTIONS`, footer `TRADEVALUE · gex-agentkit · Cloudflare Tunnel + Tailscale` + `Quiet, predictable, fast to learn.` a destra. |
| `04-charts-btc-15m-1h.png` | CHARTS | Toggle BTC/ETH a destra, toggle timeframe `15M / 1H` (active) `1H / 4H` `4H / 1D`. Due chart candlestick affiancati (15M e 1H, 200 bars) con overlay dei livelli GEX/POC/bid/ask label. Pannello destro `LEVELS — BTC` (15 totali) con prezzo, label troncato `BTC accepta…` `BTC reclaim…` ecc. e strength score. Footer ticker `BTC 76.392 +585.29 (+0.78%)` + bottone `REST`. |
| `05-macro-terminal-overview.png` | MACRO | `Macro Terminal · DRUCKENMILLER FRAMEWORK`, badge `data · 29m ago`, tab numerati `1 OVERVIEW / 2 RATES / 3 INFLATION / 4 GROWTH / 5 LABOR / 6 RISK`. Banner arancione `OVERHEATING WATCH` con Fed Funds 3.64%, 10Y 4.25%, 2s10s +54bps, CPI 3.3%, 2Y 3.71%, 30Y 4.85%, 30Y mortgage 6.23%, CPI MoM +0.87%. KPI tiles `CPI INDEX 330.29`, `UNEMPLOYMENT 4.30%`, `10Y TREASURY 4.25%`, `VIX 18.81`. Market Snapshot: SPY +0.20%, QQQ -0.44%, TLT +0.23%, GLD +1.04%, USO -3.31%, HYG +0.16%, VIX -7.72%. |
| `06-settings-account-chatgpt-telegram-theme.png` | SETTINGS | `ACCOUNT & PREFERENCES`, sidebar destra `CHATGPT CONNECTED`, `PLAN plus`, `EMAIL montalto36@gmail.com`. Card `CHATGPT (CODEX) ACCOUNT` con email/plan/account ID/token expires + bottone `MANAGE CODEX ACCOUNT`, `RECONNECT / CHANGE ACCOUNT`, `SWITCH TO DEFAULT`. Card `TELEGRAM PAIRING · SOON` (stato in arrivo). Card `THEME · display preferences · AUTO` con scelte AUTO/DARK/LIGHT. |
| `07-admin-settings-exchange-bitget.png` | ADMIN > Exchange | `ADMIN · SETTINGS` badge `OWNER`. Tab `EXCHANGE / MACRO / LLM / TELEGRAM / PIPELINE / OPERATIONS / AUDIT`. Banner `BITGET ACTIVE VENUE · TESTNET` + bottone `SWITCH BACK TO MAINNET`. Form `BITGET` con `BITGET API KEY / SECRET / PASSPHRASE` (mascherate, bottoni `SHOW`/`SAVE`) e toggle `BITGET TESTNET ON`. Audit hint `DB by user#1 · 2026-04-29 21:30`. |
| `08-bug-charts-black-empty-below-footer.png` | **BUG · CHARTS** | Header + footer correttamente posizionati, ma **tutto il body è vuoto/nero**. Probabile causa: il viewport ha `min-height: 100vh` o un `padding-bottom` ereditato che fa scrollare oltre il contenuto reale. Da indagare nel layout `<main>` o nel container che wrappa la `Charts` page. |
| `09-gex-analysis-dashboard-active-thesis-summary.png` | GEX ANALYSIS dashboard | Pannello `ACTIVE THESIS · BTC` (border arancione, badge `LIVE` verde + `16h ago` rosso = stato incoerente). `BIAS NEUTRAL gex_analysis`, `CONFIDENCE 20 updated 30/04/2026, 01:54:51`. **`SUMMARY` con font gigantesco**: "PRICE ALERT sopra 75.857 triggerato, ma il protocollo non consente esecuzione: il risk manager blocca nuovi long BTC per funding oltre soglia hard. Il reclaim segnala forza locale contro la tesi short precedente, ma senza permesso risk non c'è trade. Lettura: breakout potenziale…" Sidebar destra `Trades ledger · 0 OPEN · 7d ago`, toggle `OPEN/CLOSED`, `Lessons learned · 4 entries`, search lessons, filtri tag (ALL/TRADE/MISSED/INVALIDATION/RETROSPECTIVE/POST_MORTEM/MONITOR/NO_TRADE), preview lesson `BTC RETROSPECTIVE 2026-04-29 LOSS_EVITATA · CORRECT` e `BTC MONITOR 2026-04-16 LOSS_EVITATA · CORRECT`. |
| `10-admin-telegram-routing.png` | ADMIN > Telegram | Tab `TELEGRAM` attivo. Card `BOT TOKENS · Default bot drives the user-facing channel; the GEX bot delivers analysis-only messages on a separate channel.` (campi token vuoti). Card `ROUTING · Comma-separated user IDs allowed to talk to the bot, plus the default chat for outbound notifications.` `DEFAULT CHAT ID 372637160` (badge `ENV`), `SHADOW CHAT ID` vuoto (badge `DEFAULT`). |

## FRONTEND-ISSUES (priorità per Claude Code remoto)

### 🔴 Bug funzionali

1. **Pagina nera sotto il footer** (screenshot 08). Su `Charts` (e probabilmente altre route) lo scroll prosegue oltre il contenuto. Indagare:
   - `<main>` con `min-height: 100vh` non sottratto dell'header height
   - Container con `padding-bottom` o `margin-bottom` di troppo
   - Layout flexbox con `flex-grow` che spinge oltre il viewport
   - Mancanza di `overflow: hidden` sul wrapper di pagina
   Fix tipico: `<main class="min-h-[calc(100dvh-Xpx-Ypx)]">` con X = altezza header e Y = altezza footer.

2. **Badge `LIVE` mendaci** (screenshot 09). Sul pannello `GEX ANALYSIS · LIVE` compare `last turn · 15h ago` / `thesis · 16h ago` — il badge LIVE è verde ma il dato è vecchio. Definire 3 stati con colori diversi:
   - `LIVE` (verde) → ultimo turn ≤ N min (es. 5 min)
   - `IDLE` (grigio/ambra) → N–60 min
   - `STALE` (rosso) → > 60 min
   Stessa logica per `SSE STATE · live · streaming` quando 0 eventi: usare `connected · idle` invece di `live · streaming`.

3. **Last trade `12d ago`** (screenshot 01) senza warning visivo. KPI tiles vecchi devono colorare il valore (es. ambra a >24h, rosso a >7d).

### 🟡 Coerenza visiva e copy

4. **Lingue mischiate**: greeting "Buonasera, Leleciol8@Gmail Com." (IT) accanto a payoff "One bus, three agents, zero polling…" (EN). Decidere una lingua canonica o fare i18n proprio. Raccomandazione: tutto IT (l'utente è italiano, il sistema è personale).

5. **Email title-cased "Leleciol8@Gmail Com."** (screenshot 01). Il pipe di greeting probabilmente usa una funzione `titleCase()` su `email.split('@')[0] + ' ' + email.split('@')[1].replace('.', ' ')`. Soluzione: mostrare l'email **raw lowercase** o estrarre solo lo username. Fix: `const display = email.split('@')[0]` → "leleciol8".

6. **Footer "Cloudflare Tunnel + Tailscale"** (screenshot 03 e 08). È leak di infrastruttura interna, non ha valore per l'utente. Sostituire con qualcosa di neutro o tagline; oppure spostarlo solo nella pagina ADMIN > OPERATIONS se serve come reminder tecnico.

### 🟡 Tipografia spaccata

7. **Summary `ACTIVE THESIS · BTC` con font enorme** (screenshot 09). Il blocco di testo della thesis viene renderizzato con un font-size gigantesco che fa scrollare la pagina di colonna unica. Fix:
   - Wrappare il body del summary in `<div class="prose prose-sm max-w-prose">` (Tailwind Typography)
   - Cap su `font-size: 0.95rem; line-height: 1.55`
   - `max-width: 60ch` e `word-wrap: break-word`

### 🟡 UX

8. **Charts toggle timeframe ambiguo** (screenshot 04). I tre toggle `15M/1H`, `1H/4H`, `4H/1D` sembrano coppie. In realtà sono preset per i due chart affiancati. Etichettare in modo esplicito (es. `LEFT: 15M · RIGHT: 1H`) o fare due selettori distinti.

9. **Levels list con label troncato** (screenshot 04 sidebar destra): `BTC accepta…`, `BTC reclaim…`. Allargare la colonna o aggiungere tooltip on hover.

10. **Header `PLUS · 5H:99% · WK:98%`** — significato oscuro per chiunque non abbia letto il codice. Aggiungere tooltip ("Cache hit ratio 5h / 7d") o sostituire con icone+label.

11. **Banner `OVERHEATING · WATCH`** (screenshot 05) senza spiegazione del trigger. Aggiungere un piccolo `(?)` con popover che dice quale combinazione di metriche ha attivato il flag (es. "DFF + 2s10s spread + CPI YoY oltre soglia").

### 🟢 Nice-to-have

12. **Tab `ADMIN`** sempre visibile in nav primaria. Per UX, mostrare solo se `user.role === 'OWNER'` (è già `owner` per l'utente, ma su un sistema personale non è critico).

13. **Sidebar destra HUB** mostra `CHATGPT email`, `SSE LIVE`, `TENANT default` — il `TENANT default` è leak di multi-tenancy non rilevante per single-user. Nasconderlo o spostarlo in ADMIN.

14. **Chip `BTC NEUTRAL` / `ETH SHORT`** sotto il payoff (screenshot 01) — buono. Se possibile aggiungere il timestamp dell'ultima thesis update sul chip, altrimenti rischia di sembrare statico.

15. **Mostrare versioning/build** in fondo alla pagina ADMIN > AUDIT (es. `gex-agentkit v0.4.2 · build a1b2c3d`) per debug remoto.
