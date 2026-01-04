import asyncio
import datetime
import pandas as pd
import os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
SITE_PROFILES = {
    "ESPN": {
        "url": "https://www.espn.com",
        "selectors": {"Headline": "h1, h2, h3", "Subhead": ".contentItem__subhead",
                      "Video": ".video-play-button, .video-label"}
    },
    "Bleacher Report": {
        "url": "https://bleacherreport.com",
        "selectors": {"Headline": ".articleTitle, .ui-title", "Subhead": ".articleDescription", "Video": ".videoIcon"}
    },
    "CBS Sports": {
        "url": "https://www.cbssports.com",
        "selectors": {"Headline": ".marquee-headline, .listing-headline", "Subhead": ".article-deck",
                      "Video": ".video-canvas"}
    }
}
KEYWORDS_FILE = "keywords.txt"
OUTPUT_FILE = "scan_results.csv"


async def get_site_content(browser, url):
    """Fetches HTML with a more lenient timeout and wait condition."""
    page = await browser.new_page()
    # Realistic User-Agent to prevent blocking
    await page.set_extra_http_headers({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    })

    try:
        print(f"[*] Navigating to {url}...")
        # Changed 'networkidle' to 'domcontentloaded' to avoid timeout loops
        await page.goto(url, wait_until="domcontentloaded", timeout=60000)

        # Give JavaScript 3 seconds to inject the headlines/videos
        await asyncio.sleep(3)

        return await page.content()
    except Exception as e:
        print(f"[!] Error loading {url}: {e}")
        return None
    finally:
        await page.close()


def parse_and_match(html, profile_name, selectors, keywords):
    soup = BeautifulSoup(html, "html.parser")
    found = []
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for label, selector in selectors.items():
        for el in soup.select(selector):
            text = el.get_text(strip=True)
            if not text: continue

            lower_text = text.lower()
            for kw in keywords:
                if kw.lower() in lower_text:
                    found.append({
                        "Timestamp": timestamp,
                        "Source": profile_name,
                        "Type": label,
                        "Matched Text": text,
                        "Keyword": kw
                    })
                    break
    return found


async def main():
    if not os.path.exists(KEYWORDS_FILE):
        print(f"[!] {KEYWORDS_FILE} missing. Please create it.")
        return

    with open(KEYWORDS_FILE, "r") as f:
        keywords = [line.strip() for line in f if line.strip()]

    all_matches = []

    async with async_playwright() as p:
        # Launching with a slower 'slow_mo' helps bypass some bot detection
        browser = await p.chromium.launch(headless=True)

        for name, profile in SITE_PROFILES.items():
            html = await get_site_content(browser, profile["url"])
            if html:
                matches = parse_and_match(html, name, profile["selectors"], keywords)
                all_matches.extend(matches)
                print(f"[+] Found {len(matches)} potential matches on {name}")

        await browser.close()

    if all_matches:
        df = pd.DataFrame(all_matches)
        # Deduplicate to ensure the same headline isn't captured twice in one run
        df = df.drop_duplicates(subset=["Source", "Matched Text"])

        header = not os.path.exists(OUTPUT_FILE)
        df.to_csv(OUTPUT_FILE, mode='a', index=False, header=header, encoding='utf-8')
        print(f"\n[DONE] Results written to {OUTPUT_FILE}")
    else:
        print("\n[!] No matches found across all sites.")


if __name__ == "__main__":
    asyncio.run(main())