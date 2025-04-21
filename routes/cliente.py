from flask import jsonify, make_response, request, render_template, redirect, url_for
import sys
from db import get_connection

sys.dont_write_bytecode = True

def login():
    if request.method == "GET":
        # deverá retornar o html crú
        return render_template("login.html")
    
    elif request.method == "POST":
        dados = request.form.to_dict()
        conexao = get_connection()
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT nome, chave, saldo FROM usuarios WHERE email = %s AND senha = %s", (dados["email"], dados["password"]))
        usuario = cursor.fetchall()
        conexao.close()
        cursor.close()
        if not usuario:
            return redirect(url_for("login_route"))
        
        return render_template("home.html", nome=usuario[0]["nome"], chave_pix=usuario[0]["chave"], saldo=usuario[0]["saldo"])

def register():
    if request.method == "GET":
        return render_template("register.html")
    
    elif request.method == "POST":
        dados = request.form.to_dict()
        conexao = get_connection()
        cursor = conexao.cursor()
        cursor.execute("""
    INSERT INTO usuarios (nome, senha, data_nascimento, email, chave, telefone, saldo)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""", (
    dados["nome"],
    dados["senha"],
    dados["data-nascimento"],
    dados["email"],
    dados["chave-pix"],
    dados["telefone"],
    "0"
))
        conexao.commit()
        
        return render_template("login.html")