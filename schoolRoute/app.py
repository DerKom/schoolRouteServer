# app.py
from flask import Flask
from flask_cors import CORS
from controller import login, getUserRoute, register, get_all_users, modifyUsers, deleteUsers, changePassword, \
    getCenters, modifyCenterEmail, getMaterials, cerrarSesion, checkRol, addMaterial, modifyMaterial, deleteMaterial, \
    getRouteGroups

app = Flask(__name__)
CORS(app)

@app.route('/setRouteToUser', methods=['POST'])
def handle_set_route_to_user():
    response, status_code = setRouteToUser()
    return response, status_code

@app.route('/getRouteGroups', methods=['POST'])
def handle_get_route_groups():
    response, status_code = getRouteGroups()
    return response, status_code


@app.route('/deleteMaterial', methods=['POST'])
def handle_delete_material():
    response, status_code = deleteMaterial()
    return response, status_code

@app.route('/modifyMaterial', methods=['POST'])
def handle_modify_material():
    response, status_code = modifyMaterial()
    return response, status_code

@app.route('/addMaterial', methods=['POST'])
def handle_add_material():
    response, status_code = addMaterial()
    return response, status_code

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