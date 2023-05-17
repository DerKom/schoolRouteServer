# app.py
from flask import Flask
from flask_cors import CORS
from controller import login, getUserRoute, register, get_all_users, modifyUsers, deleteUsers, changePassword, \
    getCenters, modifyCenterEmail, getMaterials, cerrarSesion, checkRol

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def handle_login():
    response, status_code = login()
    return response, status_code

@app.route('/getCenters', methods=['POST'])
def handle_get_centers():
    response, status_code = getCenters()
    return response, status_code

@app.route('/cerrarSesion', methods=['POST'])
def cerrar_sesion_route():
    return cerrarSesion()

@app.route('/checkRol', methods=['POST'])
def check_rol_route():
    return checkRol()

@app.route('/getRoute', methods=['POST'])
def handle_get_route():
    response, status_code = getUserRoute()
    return response, status_code

@app.route('/register', methods=['POST'])
def handle_register():
    response, status_code = register()
    return response, status_code

@app.route('/getUsersData', methods=['POST'])
def handle_get_all_users():
    response, status_code = get_all_users()
    return response, status_code

@app.route('/modifyUser', methods=['POST'])
def handle_modify_user():
    response, status_code = modifyUsers()
    return response, status_code

@app.route('/deleteUser', methods=['POST'])
def handle_delete_user():
    response, status_code = deleteUsers()
    return response, status_code
@app.route('/changePassword', methods=['POST'])
def handle_change_password():
    response, status_code = changePassword()
    return response, status_code

@app.route('/modifyCenterEmail', methods=['POST'])
def modify_center_email():
    return modifyCenterEmail()

@app.route('/getMaterials', methods=['POST'])
def get_materials_route():
    return getMaterials()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)