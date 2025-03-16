# -*- coding: utf-8 -*-
"""
Created on Sat Mar 15 18:05:39 2025

@author: fenris123
"""

import pandas as pd
import json
import os

# Solicitar el nombre del archivo JSON de entrada
nombre_archivo_entrada = input("Introduce el nombre del archivo JSON de entrada (con extensión .json): ")

# Comprobar que el archivo tiene la extensión .json
if not nombre_archivo_entrada.endswith(".json"):
    print("El archivo debe tener la extensión .json")
    print("Si el archivo incluía dicha extensión, asegúrese de que está en su entorno de trabajo, o introduzca la ruta completa")
    exit()

# Cargar los datos desde el archivo JSON
with open(nombre_archivo_entrada, "r", encoding="utf-8") as f:
    datos = json.load(f)

# Convertir los datos a un DataFrame
df = pd.DataFrame(datos)

# Dividir los datos por estación
estaciones = df["nombre"].unique()

# Crear un diccionario para almacenar los DataFrames por estación
dataframes_estaciones = {}

# Procesar cada estación
for estacion in estaciones:
    # Filtrar los datos por estación
    df_estacion = df[df["nombre"] == estacion].copy()
    
    # Establecer la columna "fecha" como índice
    df_estacion.set_index("fecha", inplace=True)
    
    # Eliminar la columna "nombre" después de separar los datos por estación
    df_estacion = df_estacion.drop(columns=["provincia", "indicativo", "nombre"])
      
    # Guardar el DataFrame transpuesto en el diccionario
    dataframes_estaciones[estacion] = df_estacion

# Generar el nombre del archivo de salida, cambiando la extensión a .xlsx
nombre_archivo_salida = os.path.splitext(nombre_archivo_entrada)[0] + ".xlsx"

# Guardar los datos en un archivo Excel
try: 
    with pd.ExcelWriter(nombre_archivo_salida) as writer:
        for estacion, df_estacion in dataframes_estaciones.items():
            df_estacion.to_excel(writer, sheet_name=estacion)
    print(f"Los datos han sido transformados y guardados en {nombre_archivo_salida}")
        
except: 
    print ("No se pudo guardar el archivo.  Asegurese de que no existe un archivo excel con ese nombre.")

