from flask import Flask, render_template, request, redirect
import requests
import ast
import utils

from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

API_NODE = "http://10.5.9.110:5000"
SEARCH_API = "http://10.5.9.100:9200"

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
    blockchain = requests.get(API_NODE + "/blockchain").json()[::-1]
    return render_template("explore.html", blockchain=blockchain)


@app.route("/details-tx", methods=['GET'])
def details_tx():
    # get txid
    
    txid = request.args.get('txid')
    tx = requests.get(API_NODE + '/transaction/' + txid)
    if tx.status_code == 200:
        tx = tx.json()
        print tx
        tx['data'] = ast.literal_eval(tx['data'])
        return render_template("details-tx.html", tx=tx)
    else:
        return redirect("/explore")


@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'GET':
        return render_template("search.html")

    elif request.method == 'POST':
        keyword = request.form['keyword']
        ## TODO
        ## Call to api to search document
        ## result = list of block
        result = utils.search_document(SEARCH_API, keyword)
        message = ""
        if len(result) > 0:
            return render_template("search.html", result=result)
        elif len(result) == 0:
            message = "No document with keyword {1} exist".format(keyword)
            return render_template("search.html", message=message)


if __name__ == "__main__":
    
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8000
    )
