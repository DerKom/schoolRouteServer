# controller.py
# ...
from flask import request, jsonify
from model import SchoolRouteDB
from view import print_received_request, print_db_changes

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
                    # Buscar token existente y válido en la tabla sessions
                    find_token_query = """
                        SELECT token FROM sessions
                        WHERE username = %s AND expires_at > NOW();
                    """
                    token_result = db.fetch_data(find_token_query, (username,))

                    if token_result:
                        token = token_result[0][0]
                        response = {"token": token}
                        status_code = 200
                    else:
                        # Eliminar tokens caducados
                        delete_expired_tokens_query = """
                            DELETE FROM sessions WHERE username = %s AND expires_at <= NOW();
                        """
                        db.execute_sql(delete_expired_tokens_query, (username,))

                        # Generar e insertar nuevo token en la tabla sessions
                        token_creation_query = """
                            INSERT INTO sessions (username, token, created_at, expires_at)
                            VALUES (%s, gen_random_uuid(), NOW(), NOW() + INTERVAL '1 day')
                            RETURNING token;
                        """
                        token_result = db.execute_sql_and_return(token_creation_query, (username,))
                        if token_result:
                            token = token_result[0]
                            response = {"token": token}
                            status_code = 200
                        else:
                            response = {"message": "Error al generar el token"}
                            status_code = 500
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