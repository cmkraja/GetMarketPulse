from playwright.sync_api import sync_playwright

# --- Scrape data ---
def get_data():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )

        page = context.new_page()

        # ---------- GOLD ----------
        page.goto("https://www.goodreturns.in/gold-rates/chennai.html", wait_until="domcontentloaded")
        page.wait_for_timeout(6000)

        elements = page.query_selector_all(".gold-each-container")
        print("Gold elements:", len(elements))

        g_24k, g_22k = "", ""
        for idx, el in enumerate(elements):
            items = el.query_selector_all('.gold-common-head')
            if len(items) > 1:
                price = items[1].inner_text()
                if idx == 0:
                    g_24k = price
                elif idx == 1:
                    g_22k = price

        # ---------- SILVER ----------
        page.goto("https://www.goodreturns.in/silver-rates/chennai.html", wait_until="domcontentloaded")
        page.wait_for_timeout(6000)

        elements = page.query_selector_all(".gold-each-container")
        print("Silver elements:", len(elements))

        silver = ""
        if len(elements) > 0:
            items = elements[0].query_selector_all('.gold-common-head')
            if len(items) > 1:
                silver = items[1].inner_text()

        # ---------- USD/INR ----------
        page.goto("https://www.goodreturns.in/currency/united-states-dollar-usd-to-indian-rupee-inr-converter.html", wait_until="domcontentloaded")
        page.wait_for_timeout(6000)

        try:
            usd_inr = float(page.query_selector(".gr-green-color").inner_text())
        except:
            usd_inr = 0

        # ---------- NIFTY ----------
        page.goto("https://www.goodreturns.in/nse/", wait_until="domcontentloaded")
        page.wait_for_timeout(6000)

        rows = page.query_selector_all(".moneyweb-tabsContent table tbody tr")

        nifty = ""
        if len(rows) > 4:
            cols = rows[4].query_selector_all("td")
            if len(cols) > 1:
                nifty = cols[1].inner_text()

        browser.close()

    return g_24k, g_22k, silver, round(usd_inr, 2), nifty