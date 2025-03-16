# -*- coding: utf-8 -*-

"""
Created on Wed Mar 12 12:21:08 2025

@author: fenris123
"""


import json
import os
import requests
import sys
from dotenv import load_dotenv
from datetime import datetime
from time import sleep



# PASO 1: CARGA DE TOKEN
load_dotenv("C:/espaciopython/enviroments/tokens.env")
Token_aemet = os.getenv("TOKEN_AEMET")

headers = {
    "accept": "application/json",
    "api_key": Token_aemet
}




# PASO 2: SOLICITAR FECHAS
def solicitar_fecha(mensaje, permitir_solo_anio=False):
    while True:
        fecha_input = input(mensaje + ' (o escribe "FIN" para salir): ')
        if fecha_input.upper() == "FIN":
            print("Saliendo del programa...")
            sys.exit()

        if len(fecha_input) == 4:
            # Si el usuario introduce solo el año
            try:
                año_valido = datetime.strptime(fecha_input, "%Y")
                return año_valido.strftime("%Y")
            except ValueError:
                print("Formato incorrecto. Usa solo el año en formato AAAA.")
        else:
            # Formato fecha completa
            try:
                fecha_valida = datetime.strptime(fecha_input, "%Y-%m-%d")
                return fecha_valida.strftime("%Y-%m-%dT00:00:00UTC")
            except ValueError:
                print("Formato incorrecto. Usa AAAA-MM-DD.")




# PASO 3: SOLICITAR ID DE LAS ESTACIONES
def solicitar_estaciones(mensaje):
    while True:
        estaciones_input = input(mensaje + ' (o escribe "FIN" para salir): ')
        if estaciones_input.upper() == "FIN":
            print("Saliendo del programa...")
            sys.exit()
        estaciones = [est.strip() for est in estaciones_input.split(',')]
        
        # Verificar que todas las estaciones tienen el formato correcto (4 o 5 caracteres alfanuméricos)
        if all(len(est) == 4 or len(est) == 5 for est in estaciones) and all(est.isalnum() for est in estaciones):
            return ','.join(estaciones)
        else:
            print("Formato incorrecto. Asegúrate de que las estaciones tengan 4 o 5 caracteres alfanuméricos.")





# PASO 4: Lógica para manejar el rango de fechas
def gestionar_fechas():
    print("Introduce las fechas a estudiar. Puede ser un año completo, o un rango de fechas de hasta 6 meses.")
    fecha_ini = solicitar_fecha("Introduce la fecha de inicio (AAAA-MM-DD) o solo el año con los 4 digitos")

    if len(fecha_ini) == 4:  # Solo se ha introducido un año
        # Realizar dos peticiones, una para el primer semestre y otra para el segundo
        fecha_ini_1 = f"{fecha_ini}-01-01T00:00:00UTC"
        fecha_fin_1 = f"{fecha_ini}-06-30T23:59:59UTC"
        fecha_ini_2 = f"{fecha_ini}-07-01T00:00:00UTC"
        fecha_fin_2 = f"{fecha_ini}-12-31T23:59:59UTC"

        print ("Solicitando datos")

        return [(fecha_ini_1, fecha_fin_1), (fecha_ini_2, fecha_fin_2)]
    
    else:  # Se ha introducido un rango de fechas
        fecha_fin = solicitar_fecha("Introduce la fecha de fin (AAAA-MM-DD)")

        # Verificar que no exceda los 6 meses
        fecha_ini_obj = datetime.strptime(fecha_ini, "%Y-%m-%dT00:00:00UTC")
        fecha_fin_obj = datetime.strptime(fecha_fin, "%Y-%m-%dT00:00:00UTC")
        delta = fecha_fin_obj - fecha_ini_obj

        if delta.days > 183:
            print("El rango de fechas no puede exceder los 6 meses.")
            sys.exit()

        return [(fecha_ini, fecha_fin)]



# PASO 5 SOLICITAR AL USUARIO LOS DATOS.


# Solicitar estaciones
idema = solicitar_estaciones("Introduce las estaciones (separadas por comas)")

#  EJEMPLO A ELIMINAR  idema = "5790Y,5783,5788X"  

# Solicitar fechas
rangos_fechas = gestionar_fechas()





# PASO 6: Realizar las peticiones para cada rango de fechas



# Variables para almacenar los datos de todas las peticiones
todos_los_datos = []
metadatos = None  # Variable para almacenar los metadatos



for fecha_ini, fecha_fin in rangos_fechas:
    print(f"Realizando petición para las fechas {fecha_ini} a {fecha_fin}")
    
    
    
    # Realizar la petición a la API para obtener los metadatos solo en la primera iteración
    if metadatos is None:
        URL_BASE = "https://opendata.aemet.es/opendata"
        PETICION_METADATOS = f"/api/valores/climatologicos/diarios/datos/fechaini/{fecha_ini}/fechafin/{fecha_fin}/estacion/{idema}"
        respuesta_metadatos = requests.get(URL_BASE + PETICION_METADATOS, headers=headers)
        
        if respuesta_metadatos.status_code == 200:
            try:
                metadatos = respuesta_metadatos.json()
                print("Metadatos obtenidos correctamente.")

                # Segunda consulta para obtener los metadatos completos
                if "metadatos" in metadatos:
                    metadatos_url = metadatos["metadatos"]
                    respuesta_metadatos_completos = requests.get(metadatos_url)

                    if respuesta_metadatos_completos.status_code == 200:
                        metadatos_completos = respuesta_metadatos_completos.json()
                        print("Metadatos completos obtenidos.")
                        metadatos = metadatos_completos  # Actualizamos los metadatos con la respuesta completa
                    else:
                        print(f"Error al obtener los metadatos completos. Código: {respuesta_metadatos_completos.status_code}")
                else:
                    print("No se encontró la clave 'metadatos' en la respuesta de la primera consulta.")
            except json.JSONDecodeError as e:
                print(f"Error al decodificar los metadatos: {e}")
        else:
            print(f"Error al obtener los metadatos. Código: {respuesta_metadatos.status_code}")
            sys.exit()
    sleep(5)   



     
    # Realizar la petición para los datos climáticos
    URL_BASE = "https://opendata.aemet.es/opendata"
    PETICION = f"/api/valores/climatologicos/diarios/datos/fechaini/{fecha_ini}/fechafin/{fecha_fin}/estacion/{idema}"
    respuesta = requests.get(URL_BASE + PETICION, headers=headers)

    if respuesta.status_code == 200:
        try:
            data = respuesta.json()
            if "datos" in data:
                datos_url = data["datos"]
                print(f"Descargando datos desde: {datos_url}")

                # SEGUNDA PETICIÓN PARA OBTENER LOS DATOS
                respuesta_datos = requests.get(datos_url)

                # Procesar los datos como texto plano y convertir a JSON
                try:
                    datos_finales = json.loads(respuesta_datos.text)
                    print(f"Datos obtenidos para {fecha_ini} a {fecha_fin} (texto plano convertido)")

                    # Agregar los datos obtenidos a la lista de todos los datos
                    todos_los_datos.extend(datos_finales)  # Usamos extend para agregar todos los elementos
                    sleep(5)
                
                except json.JSONDecodeError as e:
                    print(f"Error al decodificar los datos JSON: {e}")
            else:
                print("No se encontró la clave 'datos' en la respuesta.")
        except json.JSONDecodeError as e:
            print(f"Error al decodificar los datos JSON: {e}")
    else:
        print(f"Error en la petición inicial: Código {respuesta.status_code}")

   
    
    
#  PASO 7:  GUARDAR LOS DATOS EN UN ARCHIVO JSON    
    
# Guardar los datos en un archivo JSON
nombre_archivo = input("introduzca un nombre para el archivo JSON: ")
if not nombre_archivo.endswith(".json"):
    nombre_archivo += ".json"

with open(nombre_archivo, "w", encoding="utf-8") as f:
    json.dump(todos_los_datos, f, indent=4, ensure_ascii=False)
print(f"Datos guardados en {nombre_archivo}")

# Preguntar si se quieren guardar los metadatos
if metadatos:
    guardar_metadatos = input("¿Quieres guardar los metadatos? (SI/NO): ").strip().upper()
    if guardar_metadatos == "SI":
        nombre_metadatos = "metadatos_" + nombre_archivo
        if not nombre_metadatos.endswith(".json"):
            nombre_metadatos += ".json"
        with open(nombre_metadatos, "w", encoding="utf-8") as f:
            json.dump(metadatos, f, indent=4, ensure_ascii=False)
        print(f"Metadatos guardados en {nombre_metadatos}")    
