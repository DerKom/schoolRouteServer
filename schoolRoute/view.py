# view.py

def print_received_request(request):
    print(f"Recibida petición {request.method} en {request.path}")

def print_db_changes(sql_query):
    print(f"Realizando cambios en la base de datos con la consulta: {sql_query}")