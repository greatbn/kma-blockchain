from flask import Flask, render_template, request, redirect
import requests

from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

API_NODE = "http://10.5.9.110:5000"

@app.route("/")
def index():
    """
    index page for make color
    """
    return render_template("index.html")


@app.route("/transactions")
def transactions():
    """
    view latest transactions ( document)
    view detail transaction
    """
    pending_transactions = requests.get(API_NODE + "/pending-transactions")
    pending_transactions = pending_transactions.json()
    return render_template("transactions.html",
                           pending_transactions=pending_transactions['pending'])


@app.route("/sign")
def sign():
    """
    Sign a document to blockchain network
    """
    return render_template("sign.html")

@app.route("/nodes", methods=["GET", "POST"])
def nodes():
    if request.method == "GET":
        nodes = requests.get(API_NODE + "/confirm-nodes")
        nodes = nodes.json()
        return render_template("nodes.html",
                               nodes=nodes['nodes'],
                               API_NODE=API_NODE)

@app.route("/explore")
def expore():
    blockchain = requests.get(API_NODE + "/blockchain").json()
    return render_template("explore.html", blockchain=blockchain)

if __name__ == "__main__":
    
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8000
    )
