# model.py
import psycopg2
from psycopg2 import sql

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

    def fetch_data(self, sql_query, params=None):
        if not self.cur:
            print("No se ha establecido conexión con la base de datos.")
            return
        try:
            self.cur.execute(sql_query, params)
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            print(f"Error al obtener datos con la consulta SQL: {e}")
            return None

    def execute_sql(self, sql_query, params=None):
        if not self.cur:
            print("No se ha establecido conexión con la base de datos.")
            return
        try:
            self.cur.execute(sql_query, params)
            result = self.cur.fetchone()
            self.conn.commit()
        except Exception as e:
            print(f"Error al ejecutar la consulta SQL: {e}")
            return None

    def execute_sql_and_return(self, sql_query, params=None):
        if not self.cur:
            print("No se ha establecido conexión con la base de datos.")
            return
        try:
            self.cur.execute(sql_query, params)
            result = self.cur.fetchone()
            self.conn.commit()
            return result
        except Exception as e:
            print(f"Error al ejecutar la consulta SQL: {e}")
            return None