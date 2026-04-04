from flask import Flask, jsonify
from flask_cors import CORS
from GetMarketPulse import get_data

app = Flask(__name__)
CORS(app)

@app.route("/get-data")
def fetch_data():
    gold_24k, gold_22k, silver, usd_inr, nifty = get_data()

    return jsonify({
        "gold_24k": gold_24k,
        "gold_22k": gold_22k,
        "silver": silver,
        "usd_inr": usd_inr,
        "nifty": nifty
    })

if __name__ == "__main__":
    app.run(debug=True)