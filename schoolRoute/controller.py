# controller.py
from model import SchoolRouteDB
from view import print_received_request, print_db_changes
from flask import request, jsonify

def login():
    print_received_request(request)

    username = request.form.get('username')
    password = request.form.get('password')

    # Aquí puedes validar las credenciales del usuario, por ejemplo,
    # comparando con un registro en una base de datos.
    # Asegúrate de llamar a print_db_changes() cuando realices cambios en la base de datos.

    if username == 'prueba' and password == '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4':
        response = {'message': 'Inicio de sesión exitoso'}
        status_code = 200
    else:
        response = {'message': 'Credenciales incorrectas'}
        status_code = 401

    return response, status_code

def validateUser