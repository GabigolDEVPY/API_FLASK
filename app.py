import sys
sys.dont_write_bytecode = True
from flask import Flask, request
from routes.cliente import login

app = Flask(__name__)


@app.route("/login", methods=["POST", "GET"])
def login_route():
        return login()


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port="3000")    