from googlemaps import Client as GoogleMaps
import pandas as pd
import psycopg2
from psycopg2 import Error

gmaps = GoogleMaps('AIzaSyBS7dV5eEin3BAt9r9qS29tQQ6wHluqgcg')

import time

def obtener_coordenadas(direccion):
    for i in range(5):  # Intenta hasta 5 veces
        try:
            geocode_result = gmaps.geocode(direccion)
            if geocode_result:
                return geocode_result[0]['geometry']['location']['lat'], geocode_result[0]['geometry']['location']['lng']
            else:
                return None, None
        except Exception as e:
            print(e)
            if i < 4:  # Si no es el último intento
                time.sleep(10)  # Espera 10 segundos antes de intentar de nuevo
                continue
            else:
                raise  # Si es el último intento, levanta la excepción
    return None, None  # Devuelve None si todos los intentos fallan

file_name = 'C:/Users/DerKom/Downloads/centrosExcel.csv'
data = pd.read_csv(file_name, delimiter=',', quotechar='"', skiprows=2, engine='python')

centros_con_coordenadas = 0
centros_sin_coordenadas = 0
total_centros = len(data)

connection = psycopg2.connect(
    database="schoolroute",
    user="gerente",
    password="Gerente123498765",
    host="138.68.185.70",
    port="5432"
)

cursor = connection.cursor()

with open("centros.txt", "w") as f:
    for index, row in data.iterrows():
        nombre_centro = row[data.columns[1]]
        direccion = row[data.columns[3]]
        municipio = row[data.columns[2]]
        telefono = row[data.columns[4]]
        correo = row[data.columns[5]]
        direccion_completa = f"{direccion}, {municipio}"

        latitud, longitud = obtener_coordenadas(direccion_completa)

        if latitud is not None and longitud is not None:
            centros_con_coordenadas += 1
            query = "INSERT INTO centros (nombre, direccion, latitud, longitud, telefono, correo) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (nombre_centro, direccion_completa, latitud, longitud, telefono, correo)
        else:
            centros_sin_coordenadas += 1
            query = "INSERT INTO centros (nombre, direccion, telefono, correo) VALUES (%s, %s, %s, %s)"
            values = (nombre_centro, direccion_completa, telefono, correo)

        try:
            cursor.execute(query, values)
            connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error insertando en la base de datos:", error)
            connection.rollback()

        print(f"Nombre del centro: {nombre_centro}")
        print(f"Dirección: {direccion_completa}")
        print(f"Latitud: {latitud}, Longitud: {longitud}\n")
        print(f"Teléfono: {telefono}")
        print(f"Correo: {correo}\n")

        f.write(f"Nombre del centro: {nombre_centro}\n")
        f.write(f"Dirección: {direccion_completa}\n")
        f.write(f"Latitud: {latitud}, Longitud: {longitud}\n")
        f.write(f"Teléfono: {telefono}\n")
        f.write(f"Correo: {correo}\n\n")

        progreso = (index + 1) / total_centros * 100
        print(f"Progreso: {progreso:.2f}% ({index + 1}/{total_centros})")
        print("---------------------------------------------------")

    print(f"Centros con coordenadas: {centros_con_coordenadas}")
    print(f"Centros sin coordenadas: {centros_sin_coordenadas}")

cursor.close()
connection.close()