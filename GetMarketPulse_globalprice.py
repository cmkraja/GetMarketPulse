import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def get_data():
    try:
        # ---------- USD/INR ----------
        try:
            forex_url = "https://open.er-api.com/v6/latest/USD"
            forex_data = requests.get(forex_url, headers=HEADERS, timeout=10).json()
            usd_inr = forex_data["rates"]["INR"]
        except:
            usd_inr = 83.0  # fallback

        # ---------- GOLD (fallback safe calculation) ----------
        try:
            # Using Yahoo Finance Gold Futures
            gold_url = "https://query1.finance.yahoo.com/v8/finance/chart/GC=F"
            gold_data = requests.get(gold_url, headers=HEADERS, timeout=10).json()

            gold_usd_per_oz = gold_data["chart"]["result"][0]["meta"]["regularMarketPrice"]

            gold_per_gram_usd = gold_usd_per_oz / 31.1035
            gold_24k = gold_per_gram_usd * usd_inr
            gold_22k = gold_24k * 0.916

            g_24k = f"₹{round(gold_24k, 0)}"
            g_22k = f"₹{round(gold_22k, 0)}"

        except:
            g_24k, g_22k = "ERR", "ERR"

        # ---------- SILVER ----------
        try:
            silver_url = "https://query1.finance.yahoo.com/v8/finance/chart/SI=F"
            silver_data = requests.get(silver_url, headers=HEADERS, timeout=10).json()

            silver_usd_per_oz = silver_data["chart"]["result"][0]["meta"]["regularMarketPrice"]

            silver_per_gram = (silver_usd_per_oz / 31.1035) * usd_inr
            silver = f"₹{round(silver_per_gram, 0)}"

        except:
            silver = "ERR"

        # ---------- NIFTY ----------
        try:
            nifty_url = "https://query1.finance.yahoo.com/v8/finance/chart/%5ENSEI"
            nifty_data = requests.get(nifty_url, headers=HEADERS, timeout=10).json()

            nifty = nifty_data["chart"]["result"][0]["meta"]["regularMarketPrice"]
        except:
            nifty = 0

        return g_24k, g_22k, silver, round(usd_inr, 2), nifty

    except Exception as e:
        import traceback
        print("ERROR in get_data():")
        print(traceback.format_exc())
        return "ERR", "ERR", "ERR", 0, 0