# app.py
from flask import Flask
from flask_cors import CORS
from controller import login

app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['POST'])
def handle_login():
    response, status_code = login()
    return response, status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
