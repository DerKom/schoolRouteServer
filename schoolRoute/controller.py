# controller.py
from model import SchoolRouteDB
from view import print_received_request, print_db_changes
from flask import request, jsonify

def login():
    print_received_request(request)

    username = request.form.get('username')
    password = request.form.get('password')

    response = {}
    status_code = 200

    # Verificar si el usuario existe en la base de datos de forma segura
    db = SchoolRouteDB()
    if db.connect():
        try:
            # Consulta SQL parametrizada para evitar inyección de SQL
            sql_query = "SELECT password FROM users WHERE username = %s;"
            result = db.fetch_data(sql_query, (username, ))

            if result:
                stored_password = result[0][0]
                if stored_password == password:
                    response = {"message": "Inicio de sesión exitoso"}
                    status_code = 200
                else:
                    response = {"message": "Contraseña incorrecta"}
                    status_code = 401
            else:
                response = {"message": "Usuario no encontrado"}
                status_code = 404

        except Exception as e:
            print(f"Error al verificar el usuario: {e}")
            response = {"message": "Error interno del servidor"}
            status_code = 500
        finally:
            db.disconnect()

    return jsonify(response), status_code
