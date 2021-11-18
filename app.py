from flask import Flask, render_template, request, redirect, url_for
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

app = Flask(__name__)

@app.template_filter('descrip')
def description(id):
    res = fetch_data("https://pro-api.coinmarketcap.com/v1/cryptocurrency/info", {"id": id})
    return res["data"][str(id)]["description"]

@app.template_filter('logo')
def logo(id):
    res = fetch_data("https://pro-api.coinmarketcap.com/v1/cryptocurrency/info", {"id": id})
    return res["data"][str(id)]["logo"]

@app.template_filter('web')
def web(id):
    res = fetch_data("https://pro-api.coinmarketcap.com/v1/cryptocurrency/info", {"id": id})
    return res["data"][str(id)]["urls"]["website"]

@app.template_filter('tw')
def tw(id):
    res = fetch_data("https://pro-api.coinmarketcap.com/v1/cryptocurrency/info", {"id": id})
    return res["data"][str(id)]["urls"]["twitter"][0]

@app.template_filter('rd')
def rd(id):
    res = fetch_data("https://pro-api.coinmarketcap.com/v1/cryptocurrency/info", {"id": id})
    return res["data"][str(id)]["urls"]["reddit"][0]

def fetch_data(url, parameters):
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '27c1490a-81ea-46dc-8b32-61aa8b4f7b82',
    }
    session = Session()
    session.headers.update(headers)
    res = session.get(url, params=parameters)
    data = json.loads(res.text)
    return data

def get_coins(length):
    data = fetch_data("https://pro-api.coinmarketcap.com/v1/cryptocurrency/category?id=6051a82566fc1b42617d6dc6", {"limit": length})
    return data["data"]["coins"]

def get_coin(symbol):
    data = fetch_data("https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest", {"symbol": symbol, "convert": "USD"})
    return data["data"][str(symbol)]

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        print("POSTing")
        inputtext = request.form["symbol"]
        print(inputtext)
        return redirect(f"/currencies/{inputtext}")
    else:
        return render_template("index.html", currencies=get_coins(25))

@app.route("/currencies/<id>", methods=["GET"])
def idwork(id):
    return render_template("token.html", currency=get_coin(id))

if __name__ == "__main__":
    app.run(debug=True)
