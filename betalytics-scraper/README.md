# Betalytics Public Pages — Analysis & Scraper (Playwright)

**Purpose:** Educational/engineering template to analyze *publicly accessible* Betalytics pages and, **if you are an authorized subscriber**, capture your own session’s network calls to structure **your own** research outputs.  
**This repo does _not_ bypass authentication or paywalls.** It respects `robots.txt`, rate limits, and includes a manual login step for Whop auth.

> If you are not a paying user with access, do not attempt to access protected content. Review Betalytics Terms & robots.txt first.

---

## Features
- ✅ **Robots.txt check** before any crawl
- ✅ **Playwright** headless browser for JS-heavy pages
- ✅ **Network capture** (URLs + JSON bodies when allowed) for your *authorized* session
- ✅ **Rate-limiting & polite headers**
- ✅ **Normalization** pipeline → `output/*.jsonl`
- ✅ **Tests** for normalizer & robots rules
- ✅ **.env support** and **manual-login flow** (no credential harvesting; you log in yourself via Whop/OAuth popup)

---

## Quickstart

```bash
# 1) Python env
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -U pip

# 2) Install
pip install -r requirements.txt
python -m playwright install  # installs browsers

# 3) Configure
cp .env.example .env
# edit .env as desired (RATE_LIMIT_SECONDS, OUTPUT_DIR). Credentials are NOT required; login is manual.

# 4) Robots check (safe, fast)
python -m betalytics_scraper.utils.robots_check https://www.betalytics.com/home

# 5) Start an **authorized** capture (opens a real browser)
python scripts/capture_home.py

# Flow:
#   - Browser opens https://www.betalytics.com/login (or /home)
#   - Click "Login with Whop" (popup) and sign in **yourself**
#   - After you land on /home, press ENTER in the terminal to begin capture
#   - When done, close the browser; JSON saved to output/
```

### Outputs
- `output/home.dom.html` — rendered HTML snapshot (if allowed)
- `output/home.network.jsonl` — log of network requests (method, url, status, _optional_ JSON body snippets)
- `output/home.normalized.jsonl` — normalized records (if mappers written for discovered endpoints)

> **Note:** JSON bodies are only saved for `application/json` responses and with size limits; redact PII as needed.

---

## Legal & Ethical
- Read and respect `robots.txt` and the site’s Terms. Do not scrape where disallowed.
- No credential storage or automated bypass is provided.
- For commercial use or bulk data, seek a **license** or **official API** from Betalytics.
- Use conservative rate limits. Default is `1.5s` between sensitive operations.

---

## Repo Structure

```
src/betalytics_scraper/
  __init__.py
  capture.py               # shared Playwright capture helpers
  normalize.py             # normalizers/mappers
  settings.py              # env & constants
  utils/
    robots_check.py        # CLI for robots.txt allow/disallow
scripts/
  capture_home.py          # manual-auth capture flow for /home
tests/
  test_normalize.py
  test_robots.py
requirements.txt
.env.example
```

---

## Extending
- Add specific mappers in `normalize.py` when you discover stable JSON endpoints (during **your** authorized session).  
- Add page-specific capturers e.g., `scripts/capture_player_trends.py` following the `capture_home.py` pattern.
- Use saved HTML snapshots in tests to avoid hitting the live site in CI.
