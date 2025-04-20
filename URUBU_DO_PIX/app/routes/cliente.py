from flask import jsonify, make_response, request
import sys
from db import get_connection

sys.dont_write_bytecode = True

def login():
    print("qualquer coisa")
    if request.method == "GET":
        # deverá retornar o html crú
        return jsonify("good work")
    
    elif request.method == "POST":
        return make_response(jsonify("Post method"))
        cursor = get_connection()

