#!/usr/bin/env python3
"""Screenshot all LacaStay US-site pages in EN + VI."""
import asyncio
import os
from playwright.async_api import async_playwright

BASE = "http://localhost:8901/us-site"  # served via /tmp/www/us-site symlink so <base href="/us-site/"> resolves
OUT = "/home/hatch/workspace/lacastay-us-site/screenshots"
os.makedirs(OUT, exist_ok=True)

PAGES = [
    "index.html",
    "nail-salons.html",
    "spas.html",
    "vacation-rentals.html",
    "how-it-works.html",
    "about.html",
    "pricing.html",
    "compliance.html",
    "terms.html",
    "privacy.html",
    "dpa.html",
    "subprocessors.html",
    "demo.html",
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        for pg in PAGES:
            name = pg.replace(".html", "")
            url = f"{BASE}/{pg}"
            print(f"Loading {url} ...")
            await page.goto(url, wait_until="networkidle", timeout=30000)
            await page.wait_for_timeout(1500)
            # EN screenshot (default)
            en_path = f"{OUT}/{name}-en.png"
            await page.screenshot(path=en_path, full_page=True)
            print(f"  saved {en_path}")
            # Switch to VI — try common switcher selectors
            switched = False
            for sel in [
                '[data-lang="vi"]', '[data-lang="vn"]',
                'button:has-text("VI")', 'a:has-text("VI")',
                '[data-set-lang="vi"]', '#lang-vi', '.lang-vi',
                'button:has-text("Tiếng Việt")',
            ]:
                try:
                    el = page.locator(sel).first
                    if await el.count() > 0:
                        await el.click()
                        await page.wait_for_timeout(2000)
                        switched = True
                        print(f"  switched to VI via {sel}")
                        break
                except Exception:
                    continue
            if not switched:
                # try localStorage + reload
                try:
                    await page.evaluate("localStorage.setItem('lang','vi');localStorage.setItem('language','vi');localStorage.setItem('locale','vi')")
                    await page.reload(wait_until="networkidle")
                    await page.wait_for_timeout(2000)
                    switched = True
                    print("  switched to VI via localStorage")
                except Exception as e:
                    print(f"  WARN: could not switch to VI: {e}")
            vi_path = f"{OUT}/{name}-vi.png"
            await page.screenshot(path=vi_path, full_page=True)
            print(f"  saved {vi_path}")
        await browser.close()
        print("DONE")

asyncio.run(main())
