from flask import Flask, render_template, request, redirect, jsonify, flash
import requests
import ast
import utils
import os
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import s3
from config import UPLOAD_FOLDER

app = Flask(__name__)
Bootstrap(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

API_NODE = "http://10.5.9.110:5000"
SEARCH_API = "http://10.5.9.110:9200"

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
    if len(pending_transactions['pending']) > 0:
        for pending in pending_transactions['pending']:
            pending['data'] = ast.literal_eval(pending['data'])
    return render_template("transactions.html",
                           pending_transactions=pending_transactions['pending'])



@app.route("/sign", methods=['GET', 'POST'])
def sign():
    """
    Sign a document to blockchain network
    """
    if request.method == 'GET':
        return render_template("sign.html")
    elif request.method == 'POST' and request.files['file']:
        file = request.files['file']
        filename = secure_filename(file.filename)
        create_new_folder(app.config['UPLOAD_FOLDER'])
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)
        s3.upload_to_s3(path, request.form.get('doc_hash'))
        data = {
            'author': request.form.get('author'),
            'title': request.form.get('title'),
            'description': request.form.get('description'),
            'doc_hash': request.form.get('doc_hash'),
            'signature': request.form.get('signature'),
            's3_url': 'https://blockchain.s3.sapham.net/{}'.format(request.form.get('doc_hash'))
        }
        new_tx = utils.create_new_transaction(data)
        if new_tx:
            return render_template("sign.html", message=new_tx['message'])
        else:
            return render_template("sign.html", message="Cannot create a document in blockchain")



@app.route("/get-s3-presign-url", methods=["POST"])
def get_s3_presign_url():
    """
    get pre-signed s3 url to upload file
    """
    data = request.json()
    url = s3.get_presigned_url(data['key'])
    return jsonify(url=url)


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
        keyword = request.form.get('keyword')
        ## TODO
        ## Call to api to search document
        ## result = list of block
        result = utils.search_document(SEARCH_API, keyword)
        message = ""
        if len(result) > 0:
            return render_template("search.html", result=result)
        elif len(result) == 0:
            message = "No document with keyword {0} exist".format(keyword)
            return render_template("search.html", message=message)

@app.route("/check-hash", methods=['GET'])
def check_hash():
    doc_hash = request.args.get('hash')
    if utils.check_hash(SEARCH_API, doc_hash) >= 1:
        return jsonify(message='This document is exist on '\
        'blockchain database'), 403
    else:
        return jsonify(message="Not exist"), 200


# def allowed_file(filename):
#     return '.' in filename and \
#         filename.split('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

if __name__ == "__main__":
    
    app.run(
        debug=True,
        host="0.0.0.0",
        port=8000
    )
