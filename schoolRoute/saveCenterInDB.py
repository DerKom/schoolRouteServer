from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import pandas as pd
import psycopg2
from psycopg2 import Error

geolocator = Nominatim(user_agent="myGeocoder")

import time

def obtener_coordenadas(direccion):
    for i in range(5):  # Intenta hasta 5 veces
        try:
            location = geolocator.geocode(direccion)
            if location:
                return location.latitude, location.longitude
            else:
                return None, None
        except GeocoderTimedOut:
            continue  # Intenta de nuevo
        except geopy.exc.GeocoderServiceError:
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
    password="Gerente",
    host="138.68.185.70",
    port="5432"
)

cursor = connection.cursor()

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


    progreso = (index + 1) / total_centros * 100
    print(f"Progreso: {progreso:.2f}% ({index + 1}/{total_centros})")
    print("---------------------------------------------------")

print(f"Centros con coordenadas: {centros_con_coordenadas}")
print(f"Centros sin coordenadas: {centros_sin_coordenadas}")

cursor.close()
connection.close()