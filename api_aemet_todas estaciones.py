# -*- coding: utf-8 -*-
"""
Created on Sat Mar 29 12:44:00 2025

@author: fenris123
"""

import json
import os
import requests
import sys
from dotenv import load_dotenv
from datetime import datetime, timedelta
from time import sleep

# CARGA DE TOKEN
load_dotenv("C:/espaciopython/enviroments/tokens.env")
Token_aemet = os.getenv("TOKEN_AEMET")

headers = {
    "accept": "application/json",
    "api_key": Token_aemet
}

# SOLICITAR FECHAS
def solicitar_fecha(mensaje):
    while True:
        fecha_input = input(mensaje + ' (o escribe "FIN" para salir): ')
        if fecha_input.upper() == "FIN":
            print("Saliendo del programa...")
            sys.exit()
        try:
            return datetime.strptime(fecha_input, "%Y-%m-%d")
        except ValueError:
            print("Formato incorrecto. Usa AAAA-MM-DD.")

# SOLICITAR TIPO DE FILTRADO
def solicitar_filtro():
    while True:
        opcion = input("¿Deseas obtener todas las estaciones (1) o solo las que incluyen los datos de irradiación solar y presión (2)? ")
        if opcion in ["1", "2"]:
            return opcion == "2"
        print("Opción no válida. Introduce 1 o 2.")

# GESTIÓN DE FECHAS
def gestionar_fechas():
    print("Introduce las fechas a estudiar.")
    while True:
        fecha_ini = solicitar_fecha("Introduce la fecha de inicio (AAAA-MM-DD)")
        fecha_fin = solicitar_fecha("Introduce la fecha de fin (AAAA-MM-DD)")
        if fecha_fin >= fecha_ini:
            return fecha_ini, fecha_fin
        else:
            print("La fecha final debe ser posterior a la fecha inicial. Por favor, intenta nuevamente.")

# SOLICITAR PARAMETROS
todos_los_datos = []
fecha_ini, fecha_fin = gestionar_fechas()
filtrar = solicitar_filtro()

URL_BASE = "https://opendata.aemet.es/opendata"
DIAS_PETICION = 14  # Intervalo máximo por petición

# PROCESO DE PETICIONES
date_actual = fecha_ini
while date_actual <= fecha_fin:
    fecha_limite = min(date_actual + timedelta(days=DIAS_PETICION - 1), fecha_fin)
    fecha_ini_str = date_actual.strftime("%Y-%m-%dT00:00:00UTC")
    fecha_fin_str = fecha_limite.strftime("%Y-%m-%dT00:00:00UTC")
    
    print(f"Realizando petición para las fechas {fecha_ini_str} a {fecha_fin_str}")
    PETICION = f"/api/valores/climatologicos/diarios/datos/fechaini/{fecha_ini_str}/fechafin/{fecha_fin_str}/todasestaciones"
    respuesta = requests.get(URL_BASE + PETICION, headers=headers)

    if respuesta.status_code == 200:
        try:
            data = respuesta.json()
            if "datos" in data:
                datos_url = data["datos"]
                print(f"Descargando datos desde: {datos_url}")
                respuesta_datos = requests.get(datos_url)
                try:
                    datos_finales = json.loads(respuesta_datos.text)
                    for elemento in datos_finales:
                        if not filtrar or ("sol" in elemento and "presMax" in elemento and "presMin" in elemento):
                            todos_los_datos.append(elemento)
                except json.JSONDecodeError as e:
                    print(f"Error al decodificar los datos JSON: {e}")
            else:
                print("No se encontró la clave 'datos' en la respuesta.")
        except json.JSONDecodeError as e:
            print(f"Error al decodificar los datos JSON: {e}")
    else:
        print(f"Error en la petición: Código {respuesta.status_code}")
    
    sleep(5)  # Espera de 5 segundos entre peticiones
    date_actual = fecha_limite + timedelta(days=1)

# GUARDADO DE DATOS
nombre_archivo = input("Introduce un nombre para el archivo JSON: ")
if not nombre_archivo.endswith(".json"):
    nombre_archivo += ".json"

with open(nombre_archivo, "w", encoding="utf-8") as f:
    json.dump(todos_los_datos, f, indent=4, ensure_ascii=False)
print(f"Datos guardados en {nombre_archivo}")