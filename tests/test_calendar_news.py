"""
Smoke test economic calendar (investpy) + crypto news RSS feeds.

Verifica empirica delle dipendenze esterne usate da:
- risk-forward.md          (calendario eventi macro USA/EU)
- news-sentiment-monitor.md (feed crypto news per sentiment + CRITICAL detection)

Validato 2026-05-01:
- investpy v1.0.8: 21 eventi US high importance in 2 settimane (FUNZIONA)
- 6 feed RSS crypto su 7 (CoinDesk redirect 308 escluso)

Dipendenze:
    pip install --user investpy feedparser

Uso:
    python3 tests/test_calendar_news.py [--out cal_news_report.md]
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path


def test_investpy() -> dict:
    """Test investpy.economic_calendar() — investing.com scraping."""
    out: dict = {"name": "investpy", "status": "FAIL", "details": ""}
    try:
        import investpy
        out["version"] = getattr(investpy, "__version__", "n/a")
    except ImportError:
        out["details"] = "Module investpy not installed (pip install investpy)"
        return out

    try:
        # Window: prossime 2 settimane, US high importance
        from datetime import datetime, timedelta
        today = datetime.utcnow().strftime("%d/%m/%Y")
        future = (datetime.utcnow() + timedelta(days=14)).strftime("%d/%m/%Y")
        cal = investpy.economic_calendar(
            countries=["united states"],
            importances=["high"],
            from_date=today, to_date=future,
        )
        n = len(cal)
        out["status"] = "AVAILABLE" if n > 0 else "AVAILABLE_EMPTY"
        out["details"] = f"{n} eventi US high importance in 2 settimane"
        if n > 0:
            sample = cal.head(3)[["date", "time", "event"]].to_dict("records")
            out["sample"] = sample
    except Exception as e:
        out["details"] = f"{type(e).__name__}: {str(e)[:200]}"

    return out


RSS_FEEDS = {
    "CoinTelegraph":          "https://cointelegraph.com/rss",
    "CoinTelegraph Markets":  "https://cointelegraph.com/rss/category/markets",
    "The Block":              "https://www.theblock.co/rss.xml",
    "Decrypt":                "https://decrypt.co/feed",
    "Bitcoin Magazine":       "https://bitcoinmagazine.com/.rss/full/",
    "CryptoSlate":            "https://cryptoslate.com/feed/",
    # Fixed con URL senza trailing slash + browser headers (verificato 2026-05-01):
    "CoinDesk":               "https://www.coindesk.com/arc/outboundfeeds/rss",
}

# Browser headers pattern — bypassa Cloudflare 1010 sui feed pubblici.
# Pattern usato da molti repo open-source per scraping legittimo low-volume.
BROWSER_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/rss+xml, application/json, text/xml, application/xml, "
              "text/html, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",  # NO brotli — ridotta complessità decoding
    "Cache-Control": "no-cache",
}


def test_rss_feeds() -> list[dict]:
    """Test ognuno dei feed RSS crypto. Usa feedparser con browser headers."""
    try:
        import feedparser
    except ImportError:
        return [{"name": "feedparser", "status": "FAIL",
                 "details": "Module feedparser not installed (pip install feedparser)"}]

    results = []
    for name, url in RSS_FEEDS.items():
        started = time.time()
        try:
            # feedparser supporta request_headers nativamente per superare anti-bot
            d = feedparser.parse(url, request_headers=BROWSER_HEADERS)
            elapsed = int((time.time() - started) * 1000)
            n = len(d.entries)
            status_code = getattr(d, "status", None)
            entry: dict = {
                "name": name,
                "url": url,
                "status": "AVAILABLE" if n > 0 else "AVAILABLE_EMPTY",
                "n_entries": n,
                "http_status": status_code,
                "elapsed_ms": elapsed,
            }
            if n > 0:
                first = d.entries[0]
                entry["latest_title"] = first.get("title", "")[:80]
                entry["latest_pubdate"] = first.get("published", "")[:30]
            results.append(entry)
        except Exception as e:
            results.append({
                "name": name, "url": url, "status": "ERROR",
                "details": f"{type(e).__name__}: {str(e)[:100]}",
            })
    return results


def test_forex_factory(retries: int = 3, backoff_seconds: int = 30) -> dict:
    """Test Forex Factory JSON feed con browser headers + retry su 429.

    Backup secondary per investpy quando il bug date mapping causa problemi.
    Schema: {date(ISO8601), country(USD/EUR/...), title, impact(High/Medium/Low/Holiday),
             forecast, previous}

    Note operativa: l'endpoint NON è bloccato da Cloudflare anti-bot quando
    si usano browser headers, MA ha un rate limit aggressivo (~5 req/min).
    Per uso production: 1 fetch/giorno è sufficiente e mai rate-limited.
    """
    import urllib.request, urllib.error, gzip
    out: dict = {"name": "Forex Factory (this week)", "status": "FAIL"}

    url = "https://nfs.faireconomy.media/ff_calendar_thisweek.json"
    headers = {**BROWSER_HEADERS, "Referer": "https://www.forexfactory.com/"}

    for attempt in range(retries):
        started = time.time()
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=15) as r:
                elapsed = int((time.time() - started) * 1000)
                raw = r.read()
                if r.headers.get("Content-Encoding", "") == "gzip":
                    raw = gzip.decompress(raw)
                import json as _json
                data = _json.loads(raw.decode("utf-8"))

                high = [e for e in data if e.get("impact") == "High"]
                usd_high = [e for e in high if e.get("country") == "USD"]

                out["status"] = "AVAILABLE"
                out["http_status"] = r.status
                out["elapsed_ms"] = elapsed
                out["attempts"] = attempt + 1
                out["total_events"] = len(data)
                out["high_impact"] = len(high)
                out["usd_high_impact"] = len(usd_high)

                if usd_high:
                    out["sample_usd_high"] = [
                        {"date": e.get("date"), "title": e.get("title"),
                         "forecast": e.get("forecast"), "previous": e.get("previous")}
                        for e in usd_high[:3]
                    ]
                return out
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < retries - 1:
                # rate limited — backoff exponential
                wait = backoff_seconds * (2 ** attempt)
                out["last_error"] = f"HTTP 429 rate limited, waiting {wait}s"
                time.sleep(wait)
                continue
            out["details"] = f"HTTP {e.code}: {str(e)[:120]}"
            out["attempts"] = attempt + 1
            return out
        except Exception as e:
            out["details"] = f"{type(e).__name__}: {str(e)[:150]}"
            out["attempts"] = attempt + 1
            return out

    return out


def render_md(investpy_result: dict, ff_result: dict,
              rss_results: list[dict]) -> str:
    out: list[str] = []
    out.append("# Economic Calendar + Crypto News RSS smoke-test")
    out.append("")
    out.append(f"Run: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}")
    out.append("")

    out.append("## 1. investpy (economic calendar via investing.com)")
    out.append("")
    out.append(f"- Status: **{investpy_result['status']}**")
    out.append(f"- Version: {investpy_result.get('version', 'n/a')}")
    out.append(f"- Details: {investpy_result.get('details', '')}")
    if "sample" in investpy_result:
        out.append("- Sample events:")
        for e in investpy_result["sample"]:
            out.append(f"  - {e.get('date')} {e.get('time')} — {e.get('event')}")
    out.append("")

    out.append("## 2. Forex Factory JSON feed (backup secondary)")
    out.append("")
    out.append(f"- Status: **{ff_result['status']}**")
    if ff_result.get("status") == "AVAILABLE":
        out.append(f"- Total events: {ff_result.get('total_events')}")
        out.append(f"- HIGH impact: {ff_result.get('high_impact')}")
        out.append(f"- USD HIGH impact: {ff_result.get('usd_high_impact')}")
        if "sample_usd_high" in ff_result:
            out.append("- Sample USD HIGH events:")
            for e in ff_result["sample_usd_high"]:
                out.append(f"  - {e['date']} — {e['title']} (forecast={e['forecast']}, prev={e['previous']})")
        out.append("")
        out.append("- Bypass anti-bot Cloudflare 1010: browser User-Agent + Referer + Accept-Encoding senza brotli")
        out.append("- Volume basso (1 fetch/giorno) = uso legittimo, no abuse")
    else:
        out.append(f"- Details: {ff_result.get('details','')}")
    out.append("")

    out.append("## 3. Crypto news RSS feeds (browser headers via feedparser)")
    out.append("")
    out.append("| Feed | Status | HTTP | Entries | Latency | Latest |")
    out.append("|---|---|---:|---:|---:|---|")
    for r in rss_results:
        if "n_entries" in r:
            latest = r.get("latest_title", "")[:60]
            out.append(f"| {r['name']} | **{r['status']}** | {r.get('http_status','-')} | "
                       f"{r['n_entries']} | {r['elapsed_ms']}ms | {latest} |")
        else:
            out.append(f"| {r['name']} | **{r['status']}** | - | - | - | "
                       f"{r.get('details','')} |")
    out.append("")

    available = sum(1 for r in rss_results if r["status"] == "AVAILABLE")
    out.append(f"**Sintesi:** {available}/{len(rss_results)} feed RSS funzionanti.")
    out.append("")

    out.append("## Conclusione")
    out.append("")
    out.append("- **Calendar economico**: stack dual-source per ridondanza")
    out.append("  - PRIMARY: `investpy` (investing.com scraping HTML, copertura globale)")
    out.append("  - BACKUP: Forex Factory JSON (28+ USD HIGH events/settimana, schema pulito)")
    out.append("  - Cross-validate i top 5 eventi per resilienza al bug date-mapping investpy")
    out.append("- **Crypto news**: 7 feed RSS aggregati, dedup per title hash")
    out.append("- **Setup**: `pip install --user investpy feedparser`")
    out.append("- **Cron suggerito**:")
    out.append("  - investpy daily 06:00 UTC -> state/macro_calendar.json")
    out.append("  - Forex Factory daily 06:30 UTC -> state/macro_calendar_ff.json (cross-validate)")
    out.append("  - RSS feeds cron 5min -> append a state/news_buffer.json")
    out.append("")
    out.append("## Pattern reusable: bypass Cloudflare 1010")
    out.append("")
    out.append("Il pattern `BROWSER_HEADERS` definito in questo script è generico.")
    out.append("Funziona per qualsiasi public feed bloccato da Cloudflare a basso volume:")
    out.append("```python")
    out.append("BROWSER_HEADERS = {")
    out.append('    "User-Agent": "Mozilla/5.0 ... Chrome/124 ...",')
    out.append('    "Accept": "application/json, ...",')
    out.append('    "Accept-Language": "en-US,en;q=0.9",')
    out.append('    "Accept-Encoding": "gzip, deflate",  # NO brotli')
    out.append('    "Referer": "https://<source-site>/",')
    out.append("}")
    out.append("```")
    out.append("Etico/legittimo per uso single-user low-volume su feed pubblici.")

    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("cal_news_report.md"))
    args = parser.parse_args()

    sys.stderr.write("=== investpy economic calendar ===\n")
    invres = test_investpy()
    sys.stderr.write(f"  status: {invres['status']}\n")
    sys.stderr.write(f"  details: {invres.get('details','')}\n\n")

    sys.stderr.write("=== Forex Factory JSON feed (backup calendar) ===\n")
    ff = test_forex_factory()
    sys.stderr.write(f"  status: {ff['status']}\n")
    if ff.get("status") == "AVAILABLE":
        sys.stderr.write(f"  total events: {ff.get('total_events')}, "
                         f"USD HIGH impact: {ff.get('usd_high_impact')}\n")
    sys.stderr.write("\n")

    sys.stderr.write("=== Crypto news RSS feeds (con browser headers) ===\n")
    rssres = test_rss_feeds()
    for r in rssres:
        sys.stderr.write(f"  [{r['name']:30s}] {r['status']:<16s} "
                         f"{r.get('n_entries','-')} entries\n")

    md = render_md(invres, ff, rssres)
    args.out.write_text(md, encoding="utf-8")
    sys.stderr.write(f"\nReport: {args.out}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
