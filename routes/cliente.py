from flask import jsonify, make_response, request, render_template, redirect, url_for, session
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
        print(usuario)
        conexao.close()
        cursor.close()
        if not usuario:
            return redirect(url_for("login_route"))
        
        session["nome"] = usuario[0]["nome"]
        session["chave"] = usuario[0]["chave"]
        session["saldo"] = usuario[0]["saldo"]
        
        return redirect(url_for("home_route"))

def register():
    if request.method == "GET":
        return render_template("register.html")
    
    elif request.method == "POST":
        dados = request.form.to_dict()
        conexao = get_connection()
        cursor = conexao.cursor()
        
        try:
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
        except:
            print("DEU ERRO")
            if cursor.rowcount <1:
                return render_template("register.html", erro="Erro ao cadastrar")
            
    return render_template("login.html")
    
    
def home():
    nome = session.get("nome")
    chave = session.get("chave")
    saldo = session.get("saldo")
    
    if not nome:
        return redirect(url_for("login_route"))
    
    return render_template("home.html", nome=nome, chave_pix=chave, saldo=saldo)


def verify_pix():
    #______________________________________________ABRINDO CONEXÃO________________________________________________________________________________
    conexao = get_connection()
    cursor = conexao.cursor(dictionary=True)
    #______________________________________________________________________________________________________________________________
    user_name = session.get("nome")
    dados_front = request.get_json()
    print(dados_front)
    chave = session.get("chave")
    cursor.execute("SELECT saldo FROM usuarios WHERE nome = %s", (user_name,))
    saldo_back = cursor.fetchall()
    status = None
    if float(saldo_back[0]["saldo"]) >= float(dados_front["valor"]):
        status = "Possível"   
    else:
        status = "Saldo insuficiente para transação"
        
    if dados_front["chave_pix"] == chave:
        return jsonify({
        "nome_destinatario": "Não encontrado",
        "chave_destino": "Chave não encontrada",
        "valor": "1000",
        "status": "Impossível"
    })
    cursor.execute("SELECT nome, chave FROM usuarios WHERE chave = %s", ((dados_front["chave_pix"]),))
    dados_recebedor = cursor.fetchone()
    
    if dados_recebedor:
        return jsonify({
            "nome_destino": dados_recebedor["nome"],
            "chave_pix": dados_recebedor["chave"],
            "valor": int(dados_front["valor"]),
            "status": status
        })
        
    
def make_pix():
    #______________________________________________ABRINDO CONEXÃO________________________________________________________________________________
    conexao = get_connection()
    cursor = conexao.cursor(dictionary=True)
    #______________________________________________________________________________________________________________________________
    user_name = session.get("nome")
    dados_front = request.get_json()
    print(dados_front)
    chave = session.get("chave")
    cursor.execute("SELECT saldo, nome, email FROM usuarios WHERE nome = %s", (user_name,))
    dados_back = cursor.fetchall()[0]

    if float(dados_back["saldo"]) >= float(dados_front["valor"]):
        
        cursor.execute("SELECT nome, chave, saldo FROM usuarios WHERE chave = %s", ((dados_front["chave_pix"]),))
        dados_recebedor = cursor.fetchall()[0]
        
        novo_saldo_remetente = float(dados_back["saldo"]) - float(dados_front["valor"])
        novo_saldo_recebedor = float(dados_recebedor["saldo"]) + float(dados_front["valor"])
        
        cursor.execute("UPDATE usuarios SET saldo = %s WHERE nome = %s", (novo_saldo_remetente, user_name,))
        cursor.execute("UPDATE usuarios SET saldo = %s WHERE nome = %s", (novo_saldo_recebedor, dados_recebedor["nome"],))
        conexao.commit()



        
        
    
    
    return jsonify({
    "chave_pix": dados_recebedor["chave"],
    "valor": float(dados_front["valor"]),
    "nome_destino": dados_recebedor["nome"],
    "nome_remetente": dados_back["nome"],
    "email_remetente": dados_back["email"]
})
    
    
def user_return():
    conexao = get_connection()
    cursor = conexao.cursor(dictionary=True)
    nome = session.get("nome")
    cursor.execute("SELECT nome, chave, saldo FROM usuarios WHERE nome = %s", (nome,))
    dados = cursor.fetchall()[0]
    print(dados)
    
    return jsonify(dados)
        
    