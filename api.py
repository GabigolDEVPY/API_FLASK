from flask import Flask, jsonify, request

app = Flask(__name__)

vagas = [
    {"nome": "vaga 1", "estado": "vazia"},
    {"nome": "vaga 2", "estado": "vazia"},
    {"nome": "vaga 3", "estado": "vazia"},
    {"nome": "vaga 4", "estado": "vazia"},
]


@app.route("/inicio", methods=["GET", "PUT"])
def return_vagas():
    return jsonify(vagas)
                    

@app.route("/agendar", methods=["PUT", "POST"])
def agendar():
    if request.method == "PUT":
        marcar = request.get_json()
        for vaga in vagas:
            if marcar["nome"] == vaga["nome"]:
                if vaga["estado"] == "ocupado":
                    return "Esse lugar já está ocupado"
                else:
                    vaga["estado"] = "ocupado"
                    return "Sua vaga foi agendada"
                    
    elif request.method == "POST":
        print("chegou aqui")
        editar = request.get_json()
        for i, vaga in enumerate(vagas):
            if vaga["nome"] == editar["nome"]:
                vagas[i] = editar
                return "sua vaga foi editada"

#coment

if __name__ == "__main__":
    app.run(debug=True)