from playwright.sync_api import sync_playwright

def get_data():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu"   # 👈 ADD THIS
                ]
            )

            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
            )

            page = context.new_page()

            # ---------- GOLD ----------
            page.goto("https://www.goodreturns.in/gold-rates/chennai.html", wait_until="domcontentloaded")
            page.wait_for_timeout(2000)

            elements = page.query_selector_all(".gold-each-container")

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
            page.wait_for_timeout(2000)

            elements = page.query_selector_all(".gold-each-container")

            silver = ""
            if len(elements) > 0:
                items = elements[0].query_selector_all('.gold-common-head')
                if len(items) > 1:
                    silver = items[1].inner_text()

            # ---------- USD/INR ----------
            page.goto("https://www.goodreturns.in/currency/united-states-dollar-usd-to-indian-rupee-inr-converter.html", wait_until="domcontentloaded")
            page.wait_for_timeout(2000)

            try:
                el = page.query_selector(".gr-green-color")
                usd_inr = float(el.inner_text()) if el else 0
            except:
                usd_inr = 0

            # ---------- NIFTY ----------
            page.goto("https://www.goodreturns.in/nse/", wait_until="domcontentloaded")
            page.wait_for_timeout(2000)

            try:
                el = page.query_selector(".price-value")
                nifty = el.inner_text() if el else 0
            except:
                nifty = 0

            browser.close()

        return g_24k, g_22k, silver, round(usd_inr, 2), nifty

    except Exception as e:
        import traceback
        print("ERROR in get_data():")
        print(traceback.format_exc())
        return "ERR", "ERR", "ERR", 0, 0