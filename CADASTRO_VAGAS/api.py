from flask import Flask, jsonify, request
from db import get_connection

app = Flask(__name__)

connection = get_connection()
cursor = connection.cursor(dictionary=True)


@app.route("/inicio", methods=["GET"])
def lista_vagas():
    cursor.execute("SELECT * FROM vagas")
    result = cursor.fetchall()
    return jsonify(result)


@app.route("/agendar", methods=["PUT"])
def agendar():
    vaga = request.get_json()
    vaga = vaga["nome"]
    cursor.execute(
    "UPDATE vagas SET estado = %s WHERE nome = %s AND (estado IS NULL OR estado = 'vazia')",
    ("ocupado", vaga)
)
    if cursor.rowcount > 0:
        print("Vaga atualizada")   
    else:
        print("Nenhuma vaga foi atualizada")      
    connection.commit()
    return lista_vagas()



if __name__ == "__main__":
    app.run(debug=True)