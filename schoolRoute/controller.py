# controller.py
# ...
from flask import request, jsonify
from model import SchoolRouteDB
from view import print_received_request, print_db_changes


def get_username_from_token(token):
    db = SchoolRouteDB()
    username = None
    if db.connect():
        try:
            # Comprobamos si el token es válido y obtenemos el nombre de usuario asociado
            sql_query = """
                SELECT username FROM sessions
                WHERE token = %s AND expires_at > NOW();
            """
            result = db.fetch_data(sql_query, (token,))

            if result:
                username = result[0][0]

        except Exception as e:
            print(f"Error al obtener el usuario del token: {e}")
        finally:
            db.disconnect()

    return username


def getUserRoute():
    print_received_request(request)

    token = request.form.get('token')
    response = {}
    status_code = 200

    # Usamos la nueva función para obtener el nombre de usuario
    username = get_username_from_token(token)

    if username:
        db = SchoolRouteDB()
        if db.connect():
            try:
                # Buscamos la ruta del usuario
                find_route_query = """
                    SELECT * FROM rutas
                    WHERE username = %s
                    ORDER BY orden;
                """
                route_result = db.fetch_data(find_route_query, (username,))

                if route_result:
                    # Preparamos la información para enviarla como json
                    route = []
                    for row in route_result:
                        route.append({
                            "id": row[0],
                            "username": row[1],
                            "centername": row[2],
                            "latitud": row[3],
                            "longitud": row[4],
                            "orden": row[5]
                        })
                    response = {"route": route}
                    status_code = 200
                else:
                    response = {"message": "No se encontró una ruta para el usuario"}
                    status_code = 404

            except Exception as e:
                print(f"Error al obtener la ruta del usuario: {e}")
                response = {"message": "Error interno del servidor"}
                status_code = 500
            finally:
                db.disconnect()
    else:
        response = {"message": "Token no válido o expirado"}
        status_code = 401

    return jsonify(response), status_code

def register():
    print_received_request(request)

    token = request.form.get('token')
    new_username = request.form.get('username')
    password = request.form.get('password')
    isAdmin = request.form.get('isAdmin')
    startAdress = request.form.get('startAdress')
    days = request.form.get('days')

    response = {}
    status_code = 200

    # Usamos la función para obtener el nombre de usuario
    username = get_username_from_token(token)

    if username:
        db = SchoolRouteDB()
        if db.connect():
            try:
                # Comprobamos si el usuario tiene permisos de administración
                admin_query = "SELECT rol FROM users WHERE username = %s;"
                admin_result = db.fetch_data(admin_query, (username, ))
                if admin_result and admin_result[0][0] == 1:
                    # Insertamos el nuevo usuario
                    insert_user_query = """
                        INSERT INTO users (username, password, rol)
                        VALUES (%s, %s, %s);
                    """
                    db.execute_sql(insert_user_query, (new_username, password, isAdmin))

                    # Aquí deberías insertar la dirección de inicio y los días en la tabla correspondiente
                    # asumiendo que existen las tablas y columnas correspondientes

                    response = {"message": "Usuario registrado con éxito"}
                    status_code = 200
                else:
                    response = {"message": "El usuario no tiene permisos de administración"}
                    status_code = 403

            except Exception as e:
                print(f"Error al registrar el usuario: {e}")
                response = {"message": "Error interno del servidor"}
                status_code = 500
            finally:
                db.disconnect()
    else:
        response = {"message": "Token no válido o expirado"}
        status_code = 401

    return jsonify(response), status_code

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