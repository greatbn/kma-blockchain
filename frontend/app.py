from flask import Flask, render_template

app = Flask(__name__)

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
    return render_template("transaction.html")


@app.route("/sign")
def sign():
    """
    Sign a document to blockchain network
    """
    return render_template("sign.html")


if __name__ == "__main__":
    
    app.run(
        debug=True,
        host="0.0.0.0",
        port=80
    )
