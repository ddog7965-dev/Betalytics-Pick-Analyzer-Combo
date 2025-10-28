import asyncio, json, os, time
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright, Page
from .settings import RATE_LIMIT_SECONDS, OUTPUT_DIR, START_URL, HEADLESS, MAX_JSON_BODY_BYTES, USER_AGENT, STORAGE_STATE

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def _save(path: str, data: Any, binary: bool=False):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if binary:
        with open(path, "wb") as f:
            f.write(data)
    else:
        with open(path, "w", encoding="utf-8") as f:
            if isinstance(data, (dict, list)):
                json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                f.write(str(data))

async def open_context(play):
    browser = await play.chromium.launch(headless=HEADLESS)
    ctx = await browser.new_context(user_agent=USER_AGENT, storage_state=STORAGE_STATE if STORAGE_STATE else None)
    page = await ctx.new_page()
    return browser, ctx, page

async def manual_auth(page: Page, login_url: str = "https://www.betalytics.com/login"):
    # If we already have a saved auth state, skip manual login
    if STORAGE_STATE:
        print("[INFO] STORAGE_STATE detected; skipping manual login.")
        return page
    # Navigate and let the **user** complete Whop login flow.
    await page.goto(login_url, wait_until="domcontentloaded")
    print("[INFO] Please click 'Login with Whop' and complete auth in the popup.")
    input("Press ENTER here after you see the Betalytics /home page loaded in the browser... ")
    return page

async def capture_page_network(page: Page, start_url: Optional[str] = None, label: str = "home"):
    events = []
    # Attach listeners BEFORE navigation to catch all
    page.on("request", lambda req: events.append({
        "type": "request", "ts": time.time(), "method": req.method, "url": req.url, "headers": req.headers
    }))
    async def on_response(res):
        rec = {
            "type": "response", "ts": time.time(), "status": res.status, "url": res.url,
            "headers": (await res.all_headers()) if hasattr(res, "all_headers") else {}
        }
        # opportunistically capture JSON bodies (with size cap)
        try:
            ct = res.headers.get("content-type", "")
            if "application/json" in ct:
                body = await res.body()
                if body and len(body) <= MAX_JSON_BODY_BYTES:
                    try:
                        rec["json"] = json.loads(body.decode("utf-8", "ignore"))
                    except Exception:
                        rec["text"] = body.decode("utf-8", "ignore")
                else:
                    rec["note"] = f"body skipped (size {len(body) if body else 0} > limit {MAX_JSON_BODY_BYTES})"
        except Exception as e:
            rec["error"] = f"body capture failed: {e}"
        events.append(rec)
    page.on("response", lambda res: asyncio.create_task(on_response(res)))

    if start_url:
        await page.goto(start_url, wait_until="networkidle")

    # save DOM snapshot (optional, public pages only)
    try:
        html = await page.content()
        await _save(os.path.join(OUTPUT_DIR, f"{label}.dom.html"), html)
    except Exception as e:
        print(f"[WARN] DOM snapshot failed: {e}")

    # small politeness delay
    await asyncio.sleep(RATE_LIMIT_SECONDS)

    # persist network log
    out_path = os.path.join(OUTPUT_DIR, f"{label}.network.jsonl")
    with open(out_path, "w", encoding="utf-8") as f:
        for ev in events:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    print(f"[OK] Network log saved → {out_path}")
    return events

async def run_capture():
    async with async_playwright() as p:
        browser, ctx, page = await open_context(p)
        try:
            # manual login flow (no bypass)
            await manual_auth(page)
            # navigate to START_URL (typically /home) and capture
            await capture_page_network(page, START_URL, label="home")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(run_capture())
