import pandas
from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route('/')
@app.route("/home")
def upload():
    return render_template("Index.html")


if __name__ == "__main__":
    app.run(host="localhost", port=int("5000"))
