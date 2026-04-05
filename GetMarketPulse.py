from playwright.sync_api import sync_playwright
from datetime import datetime
import tweepy
from tweepy import TweepyException
import time
from tweepy.errors import TwitterServerError, TooManyRequests

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Twitter API credentials
bearer_token = ""
consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

# Authenticate to Twitter
client = tweepy.Client(
    bearer_token=bearer_token, consumer_key=consumer_key, consumer_secret=consumer_secret, 
    access_token=access_token, access_token_secret=access_token_secret
)

# Function to post a tweet
# def post_tweet(tweet_text):
#     try:
#         tweet = tweet_text
        
#         response = client.create_tweet(text=tweet)
#         print("Tweet posted successfully!")
#         print("Response:", response)
#     except TweepyException as e:
#         print(f"An error occurred: {e}")

def post_tweet(tweet_text, retries=5):
    for attempt in range(retries):
        try:
            response = client.create_tweet(text=tweet_text)
            print("✅ Tweet posted successfully!")
            return response

        except TwitterServerError as e:
            wait_time = (2 ** attempt) * 5  # exponential backoff
            print(f"⚠️ Server error (503). Retry in {wait_time}s...")
            time.sleep(wait_time)

        except TooManyRequests as e:
            print("⛔ Rate limit hit. Sleeping for 15 minutes...")
            time.sleep(900)

        except Exception as e:
            print("❌ Unexpected error:", e)
            break

    print("🚫 Failed after retries.")

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

        # rows = page.query_selector_all(".moneyweb-tabsContent table tbody tr")

        nifty = ""
        # if len(rows) > 4:
        #     cols = rows[4].query_selector_all("td")
        #     if len(cols) > 1:
        #         nifty = cols[1].inner_text()
        try:
            nifty = page.query_selector(".price-value").inner_text()
        except:
            nifty = 0

        browser.close()

    return g_24k, g_22k, silver, round(usd_inr, 2), nifty

# --- Main ---
def main():
    try:
        date_str = datetime.now().strftime("%d %b %Y")

        gold_24k, gold_22k, silver, usd_inr, nifty = get_data()

        tweet = f"""{date_str} - Market Captured 📊:

🪙 Gold 24K → {gold_24k} /g
🪙 Gold 22K → {gold_22k} /g
⚪ Silver → {silver} /g
💵 $1 USD → ₹{usd_inr} INR
📈 Nifty → {nifty}

🔔 Follow @GetMarketPulse 🔁 Auto-Updated daily!
#GoldRate #SilverRate #DollarRate
"""

        print("Tweet Preview:\n", tweet)
        post_tweet(tweet)

        print("✅ Tweet posted!")

    except Exception as e:
        print("❌ Error:", e)

# --- Run ---
if __name__ == "__main__":
    main()