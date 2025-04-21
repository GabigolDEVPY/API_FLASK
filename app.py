import sys
sys.dont_write_bytecode = True
from flask import Flask, request, session
from routes.cliente import login, register, home, verify_pix


app = Flask(__name__)
app.secret_key = "algumasecretbonitaquenomoranguinhaesquece" 

@app.route("/login", methods=["POST", "GET"])
def login_route():
        return login()


@app.route("/register", methods=["GET", "POST"])
def register_route():
        return register()

@app.route("/home", methods=["GET"])
def home_route():
        return home()

@app.route("/verificar-pix", methods=["POST"])
def pix():
        return verify_pix()    

@app.route("/fazer-pix", methods=["POST"])
def fazer_pix():


if __name__ == "__main__":
    app.run(debug=True, port="3000", host="0.0.0.0")    