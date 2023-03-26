# controller.py
from model import SchoolRouteDB
from view import print_received_request, print_db_changes
from flask import request, jsonify

def login():
    print_received_request(request)

    username = request.form.get('username')
    password = request.form.get('password')


    #poner aquí el código para comprobar si el usuario existe en la base de datos



    return response, status_code