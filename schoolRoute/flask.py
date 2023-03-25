from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    # Aquí puedes validar las credenciales del usuario, por ejemplo,
    # comparando con un registro en una base de datos.

    if username == 'prueba' and password == '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4':
        response = {'message': 'Inicio de sesión exitoso'}
        status_code = 200
    else:
        response = {'message': 'Credenciales incorrectas'}
        status_code = 401

    return jsonify(response), status_code

app.run(host='0.0.0.0', port=5000)

