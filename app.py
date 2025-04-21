import sys
sys.dont_write_bytecode = True
from flask import Flask, request, session
from routes.cliente import login, register, home, verify_pix, make_pix, user_return

from pyngrok import ngrok  # 💥 aqui começa a mágica

app = Flask(__name__)
app.secret_key = "algumasecretbonitaquenomoranguinhaesquece"

@app.route("/login", methods=["POST", "GET"])
def login_route():
    return login()

@app.route("/register", methods=["GET", "POST"])
def register_route():
    return register()

@app.route("/home", methods=["GET", "POST"])
def home_route():
    return home()

@app.route("/verificar-pix", methods=["POST"])
def pix():
    return verify_pix()

@app.route("/confirmar-pix", methods=["POST"])
def confirmar_pix():
    return make_pix()

@app.route("/user-info", methods=["POST"])
def user_info():
    return user_return()

if __name__ == "__main__":
    # 🔓 Cria o túnel ngrok direto pela porta 3000
    # print("🚀 Seu app tá AO VIVO em:", public_url)
    # 👇 Agora o Flask roda normalmente
    app.run(debug=True, host="0.0.0.0", port="3000")
