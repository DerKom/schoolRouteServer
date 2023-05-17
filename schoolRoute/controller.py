# controller.py
# ...
from flask import request, jsonify
from model import SchoolRouteDB
from view import print_received_request, print_db_changes
from psycopg2 import errors


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

def deleteUsers():
    db = SchoolRouteDB()

    if db.connect():
        try:
            # Obtener el token del usuario a partir del formdata
            token = request.form.get('token')

            # Obtener el username asociado al token
            admin_username = get_username_from_token(token)

            # Obtener el username del usuario a eliminar
            user_to_delete = request.form.get('username')

            if admin_username:
                # Consulta para verificar si el usuario es administrador
                verify_admin_query = """
                    SELECT rol FROM users WHERE username = %s;
                """
                role_result = db.fetch_data(verify_admin_query, (admin_username,))

                if role_result and role_result[0][0] == 1:
                    # Consulta para eliminar el usuario
                    delete_user_query = """
                        DELETE FROM users WHERE username = %s;
                    """
                    db.execute_sql(delete_user_query, (user_to_delete,))

                    response = {"message": "El usuario ha sido eliminado con éxito"}
                    status_code = 200

                else:
                    response = {"message": "El usuario no es administrador"}
                    status_code = 403
            else:
                response = {"message": "Token no válido"}
                status_code = 401

        except Exception as e:
            print(f"Error al eliminar el usuario: {e}")
            response = {"message": "Error interno del servidor"}
            status_code = 500
        finally:
            db.disconnect()

    return jsonify(response), status_code

def changePassword():
    db = SchoolRouteDB()

    if db.connect():
        try:
            # Obtener el token del usuario a partir del formdata
            token = request.form.get('token')

            # Obtener el username asociado al token
            admin_username = get_username_from_token(token)

            # Obtener el username del usuario a modificar y la nueva contraseña
            user_to_modify = request.form.get('username')
            new_password = request.form.get('newPassword')

            if admin_username:
                # Consulta para verificar si el usuario es administrador
                verify_admin_query = """
                    SELECT rol FROM users WHERE username = %s;
                """
                role_result = db.fetch_data(verify_admin_query, (admin_username,))

                if role_result and role_result[0][0] == 1:
                    # Consulta para cambiar la contraseña del usuario
                    change_password_query = """
                        UPDATE users SET password = %s WHERE username = %s;
                    """
                    db.execute_sql(change_password_query, (new_password, user_to_modify))

                    response = {"message": "La contraseña ha sido cambiada con éxito"}
                    status_code = 200

                else:
                    response = {"message": "El usuario no es administrador"}
                    status_code = 403
            else:
                response = {"message": "Token no válido"}
                status_code = 401

        except Exception as e:
            print(f"Error al cambiar la contraseña: {e}")
            response = {"message": "Error interno del servidor"}
            status_code = 500
        finally:
            db.disconnect()

    return jsonify(response), status_code

def deleteUsers():
    db = SchoolRouteDB()

    if db.connect():
        try:
            # Obtener el token del usuario a partir del formdata
            token = request.form.get('token')

            # Obtener el username asociado al token
            admin_username = get_username_from_token(token)

            # Obtener el username del usuario a eliminar
            user_to_delete = request.form.get('username')

            if admin_username:
                # Consulta para verificar si el usuario es administrador
                verify_admin_query = """
                    SELECT rol FROM users WHERE username = %s;
                """
                role_result = db.fetch_data(verify_admin_query, (admin_username,))

                if role_result and role_result[0][0] == 1:
                    # Consulta para eliminar el usuario
                    delete_user_query = """
                        DELETE FROM users WHERE username = %s;
                    """
                    db.execute_sql(delete_user_query, (user_to_delete,))

                    response = {"message": "El usuario ha sido eliminado con éxito"}
                    status_code = 200

                else:
                    response = {"message": "El usuario no es administrador"}
                    status_code = 403
            else:
                response = {"message": "Token no válido"}
                status_code = 401

        except Exception as e:
            print(f"Error al eliminar el usuario: {e}")
            response = {"message": "Error interno del servidor"}
            status_code = 500
        finally:
            db.disconnect()

    return jsonify(response), status_code

def getMaterials():
    db = SchoolRouteDB()

    if db.connect():
        try:
            # Obtener el token del usuario a partir del formdata
            token = request.form.get('token')

            # Obtener el username asociado al token
            admin_username = get_username_from_token(token)

            if admin_username:
                # Consulta para verificar si el usuario es administrador
                verify_admin_query = """
                    SELECT rol FROM users WHERE username = %s;
                """
                role_result = db.fetch_data(verify_admin_query, (admin_username,))

                if role_result and role_result[0][0] == 1:
                    # Consulta para obtener los datos de los materiales
                    fetch_materials_query = """
                        SELECT * FROM materials;
                    """
                    materials = db.fetch_data(fetch_materials_query)

                    response = {"materials": [dict(zip(['id', 'name', 'description'], material)) for material in materials]}
                    status_code = 200

                else:
                    response = {"message": "El usuario no es administrador"}
                    status_code = 403
            else:
                response = {"message": "Token no válido"}
                status_code = 401

        except Exception as e:
            print(f"Error al obtener los materiales: {e}")
            response = {"message": "Error interno del servidor"}
            status_code = 500
        finally:
            db.disconnect()

    return jsonify(response), status_code


def modifyCenterEmail():
    db = SchoolRouteDB()

    if db.connect():
        try:
            # Obtener el token del usuario a partir del formdata
            token = request.form.get('token')

            # Obtener el username asociado al token
            admin_username = get_username_from_token(token)

            if admin_username:
                # Consulta para verificar si el usuario es administrador
                verify_admin_query = """
                    SELECT rol FROM users WHERE username = %s;
                """
                role_result = db.fetch_data(verify_admin_query, (admin_username,))

                if role_result and role_result[0][0] == 1:
                    # Obtener el correo antiguo y el nuevo del form data
                    old_email = request.form.get('old_email')
                    new_email = request.form.get('new_email')

                    # Consulta para modificar el correo de un centro
                    update_email_query = """
                        UPDATE centros SET correo = %s WHERE correo = %s;
                    """
                    db.execute_query(update_email_query, (new_email, old_email))

                    response = {"message": "Correo del centro modificado exitosamente"}
                    status_code = 200
                else:
                    response = {"message": "El usuario no es administrador"}
                    status_code = 403
            else:
                response = {"message": "Token no válido"}
                status_code = 401

        except Exception as e:
            print(f"Error al modificar el correo del centro: {e}")
            response = {"message": "Error interno del servidor"}
            status_code = 500
        finally:
            db.disconnect()

    return jsonify(response), status_code


def modifyUsers():
    db = SchoolRouteDB()

    if db.connect():
        try:
            # Obtener el token del usuario a partir del formdata
            token = request.form.get('token')

            # Obtener el username asociado al token
            admin_username = get_username_from_token(token)

            # Obtener el username del usuario a modificar, su nuevo rol y nuevo nombre de usuario
            user_to_modify = request.form.get('username')
            new_role = request.form.get('isAdmin')
            new_username = request.form.get('newUsername')

            if admin_username:
                # Consulta para verificar si el usuario es administrador
                verify_admin_query = """
                    SELECT rol FROM users WHERE username = %s;
                """
                role_result = db.fetch_data(verify_admin_query, (admin_username,))

                if role_result and role_result[0][0] == 1:
                    # Consulta para modificar el rol y el nombre de usuario
                    modify_user_query = """
                        UPDATE users SET rol = %s, username = %s WHERE username = %s;
                    """
                    db.execute_sql(modify_user_query, (new_role, new_username, user_to_modify))

                    response = {"message": "El usuario ha sido modificado con éxito"}
                    status_code = 200

                else:
                    response = {"message": "El usuario no es administrador"}
                    status_code = 403
            else:
                response = {"message": "Token no válido"}
                status_code = 401

        except Exception as e:
            print(f"Error al modificar el usuario: {e}")
            response = {"message": "Error interno del servidor"}
            status_code = 500
        finally:
            db.disconnect()

    return jsonify(response), status_code


def get_all_users():
    db = SchoolRouteDB()

    if db.connect():
        try:
            # Obtener el token del usuario a partir del formdata
            token = request.form.get('token')

            # Obtener el username asociado al token
            username = get_username_from_token(token)

            if username:
                # Consulta para verificar si el usuario es administrador
                verify_admin_query = """
                    SELECT rol FROM users WHERE username = %s;
                """
                role_result = db.fetch_data(verify_admin_query, (username,))

                if role_result and role_result[0][0] == 1:
                    # Consulta para obtener todos los usuarios
                    get_users_query = """
                        SELECT username, rol FROM users;
                    """
                    users_result = db.fetch_data(get_users_query)

                    if users_result:
                        users = [dict(zip(['username', 'rol'], user)) for user in users_result]
                        response = {"users": users}
                        status_code = 200
                    else:
                        response = {"message": "No hay usuarios en la base de datos"}
                        status_code = 404
                else:
                    response = {"message": "El usuario no es administrador"}
                    status_code = 403
            else:
                response = {"message": "Token no válido"}
                status_code = 401

        except Exception as e:
            print(f"Error al obtener usuarios: {e}")
            response = {"message": "Error interno del servidor"}
            status_code = 500
        finally:
            db.disconnect()

    return jsonify(response), status_code

def getCenters():
    db = SchoolRouteDB()

    if db.connect():
        try:
            # Obtener el token del usuario a partir del formdata
            token = request.form.get('token')

            # Obtener el username asociado al token
            admin_username = get_username_from_token(token)

            if admin_username:
                # Consulta para verificar si el usuario es administrador
                verify_admin_query = """
                    SELECT rol FROM users WHERE username = %s;
                """
                role_result = db.fetch_data(verify_admin_query, (admin_username,))

                if role_result and role_result[0][0] == 1:
                    # Consulta para obtener los datos de los centros
                    fetch_centers_query = """
                        SELECT id, nombre, direccion, correo FROM centros;
                    """
                    centers_data = db.fetch_data(fetch_centers_query)

                    if centers_data:
                        centers = [dict(zip(['id', 'nombre', 'direccion', 'correo'], center)) for center in centers_data]
                        response = {"centers": centers}
                        status_code = 200
                    else:
                        response = {"message": "No hay centros en la base de datos"}
                        status_code = 404

                else:
                    response = {"message": "El usuario no es administrador"}
                    status_code = 403
            else:
                response = {"message": "Token no válido"}
                status_code = 401

        except Exception as e:
            print(f"Error al obtener los centros: {e}")
            response = {"message": "Error interno del servidor"}
            status_code = 500
        finally:
            db.disconnect()

    return jsonify(response), status_code

def getUserRoute():
    db = SchoolRouteDB()

    if db.connect():
        try:
            # Obtener el token del usuario a partir del formdata
            token = request.form.get('token')

            # Obtener el username asociado al token
            username = get_username_from_token(token)

            if username:
                # Consulta para obtener los datos de las rutas del usuario
                fetch_route_query = """
                    SELECT id, centername, direccion, latitud, longitud 
                    FROM rutas
                    WHERE username = %s;
                """
                route_data = db.fetch_data(fetch_route_query, (username,))

                if route_data:
                    # Crear el objeto de respuesta con los datos de la ruta
                    routes = [dict(zip(['id', 'centername', 'direction', 'latitud', 'longitud'], route)) for route in route_data]
                    response = {"routes": routes}
                    status_code = 200
                else:
                    response = {"message": "No se encontraron rutas para el usuario"}
                    status_code = 404

            else:
                response = {"message": "Token no válido"}
                status_code = 401

        except Exception as e:
            print(f"Error al obtener las rutas del usuario: {e}")
            response = {"message": "Error interno del servidor"}
            status_code = 500
        finally:
            db.disconnect()

    return jsonify(response), status_code

def register():
    print_received_request(request)

    token = request.form.get('token')
    new_username = request.form.get('username')
    password = request.form.get('password')
    isAdmin = request.form.get('isAdmin')

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
                        INSERT INTO users (username, password, rol, created_at)
                        VALUES (%s, %s, %s, CURRENT_TIMESTAMP);
                    """

                    db.execute_sql(insert_user_query, (new_username, password, isAdmin))

                    # Aquí deberías insertar la dirección de inicio y los días en la tabla correspondiente
                    # asumiendo que existen las tablas y columnas correspondientes

                    response = {"message": "Usuario registrado con éxito"}
                    status_code = 200
                else:
                    response = {"message": "El usuario no tiene permisos de administración"}
                    status_code = 403

            except errors.UniqueViolation as e:
                print(f"Error al registrar el usuario: {e}")
                response = {"message": "El usuario ya existe"}
                status_code = 409
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