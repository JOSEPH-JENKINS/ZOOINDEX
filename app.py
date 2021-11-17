from flask import Flask, render_template, request, redirect, url_for
from pycoingecko import CoinGeckoAPI

coingecko = CoinGeckoAPI()
#print("Name: ", coingecko.get_coin_by_id('bitcoin')["id"])
#print("Price: ", coingecko.get_coin_by_id('bitcoin')["market_data"]["current_price"]["usd"])

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print("POSTing")
        inputtext = request.form["symbol"]
        print(inputtext)
        return redirect(f"/currencies/{inputtext}")
    else:
        print("GETting")
        return render_template("index.html", currencies=coingecko.get_coins_markets("usd"))

@app.route("/currencies/<id>", methods=["GET"])
def idwork(id):
    return render_template("token.html", currency=coingecko.get_coin_by_id(id))

if __name__ == "__main__":
    app.run(debug=True)