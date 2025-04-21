import sys
sys.dont_write_bytecode = True
from flask import Flask, request
from routes.cliente import login, register

app = Flask(__name__)


@app.route("/login", methods=["POST", "GET"])
def login_route():
        return login()


@app.route("/register", methods=["GET", "POST"])
def register_route():
        return register()

if __name__ == "__main__":
    app.run(debug=True, port="3000", host="0.0.0.0")    