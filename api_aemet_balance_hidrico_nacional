# -*- coding: utf-8 -*-

"""
Created on Wed Mar 12 12:21:08 2025

@author: fenris123
"""

import os
import requests
import sys
from dotenv import load_dotenv
from time import sleep

# PASO 1: CARGA DE TOKEN
load_dotenv("C:/espaciopython/enviroments/tokens.env")
Token_aemet = os.getenv("TOKEN_AEMET")

headers = {
    "accept": "application/json",
    "api_key": Token_aemet
}

# PASO 2: SOLICITAR AÑO Y DECENA
def solicitar_año():
    while True:
        año_input = input("Introduce el año (AAAA) o escribe 'FIN' para salir: ")
        if año_input.upper() == "FIN":
            print("Saliendo del programa...")
            sys.exit()
        if len(año_input) == 4 and año_input.isdigit():
            return año_input
        else:
            print("Formato incorrecto. Introduce un año en formato AAAA.")

def solicitar_decena():
    while True:
        decena_input = input("Introduce la decena (01 a 36) o escribe 'FIN' para salir: ")
        if decena_input.upper() == "FIN":
            print("Saliendo del programa...")
            sys.exit()
        if decena_input.zfill(2).isdigit() and 1 <= int(decena_input) <= 36:
            return decena_input.zfill(2)
        else:
            print("Formato incorrecto. Introduce un número entre 01 y 36.")

# PASO 3: SOLICITAR DATOS AL USUARIO
año = solicitar_año()
decena = solicitar_decena()

# PASO 4: REALIZAR LA PETICIÓN
URL_BASE = "https://opendata.aemet.es/opendata"
PETICION = f"/api/productos/climatologicos/balancehidrico/{año}/{decena}"

print(f"Realizando petición para el año {año} y la decena {decena}...")
respuesta = requests.get(URL_BASE + PETICION, headers=headers)

if respuesta.status_code == 200:
    content_type = respuesta.headers.get("Content-Type", "").lower()
    if "application/pdf" in content_type:
        nombre_archivo = f"balance_hidrico_{año}_{decena}.pdf"
        with open(nombre_archivo, "wb") as f:
            f.write(respuesta.content)
        print(f"PDF guardado como {nombre_archivo}")
    else:
        print("La respuesta no es un PDF. Verifica la URL y los parámetros.")
else:
    print(f"Error en la petición: Código {respuesta.status_code}")
    sys.exit()

sleep(5)

