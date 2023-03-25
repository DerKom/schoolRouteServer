from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

class SchoolRouteDB:
    def __init__(self):
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                database="schoolroute",
                user="gerente",
                password="Gerente123498765",
                host="localhost",
                port="5432"
            )
            self.cur = self.conn.cursor()
        except Exception as e:
            print(f"Error al conectar con la base de datos: {e}")
            return False
        return True

    def disconnect(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()

    def fetch_data(self, sql_query):
        if not self.cur:
            print("No se ha establecido conexión con la base de datos.")
            return
        try:
            self.cur.execute(sql_query)
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            print(f"Error al obtener datos con la consulta SQL: {e}")
            return None

    def execute_sql(self, sql_query):
        if not self.cur:
            print("No se ha establecido conexión con la base de datos.")
            return
        try:
            self.cur.execute(sql_query)
            result = self.cur.fetchone()
            self.conn.commit()
            return result
        except Exception as e:
            print(f"Error al ejecutar la consulta SQL: {e}")
            self.conn.rollback()
            return None


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

