# USING-AEMET-API-TO-OBTAIN-WEATHER-DATA-FROM-SPANISH-CITIES.

This Python script is designed to aquire wheather data from Spanish Meteorologic Agency AEMET.
The rest of the document is in Spanish. (i'm spanish after all).  If you are interested on this, i recomend to use google translator.



DESCRIPCIÓN GENERAL.

El primer script esta diseñado para obtener los datos meteorologicos de la AEMET usando su API.
Al iniciar el programa, se solicitara la ID de las estaciones meteorologicas a estudiar y el rango de fechas.
El programa admite un rango de fechas de hasta 6 meses, o bien 1 año completo del 1 de Enero al 31 de Diciembre.

Los datos recibidos se descargaran en un archivo tipo JSON.
Como somos conscientes de que no todo el mundo maneja ese formato, un segundo Script transforma si se desea los datos de ese archivo en datos tipo excel.




REQUISITOS:


1 - TOKEN DE ACCESO:
Para ejecutar este script, se necesita un token de acceso de la AEMET, que debe ser introducido en un archivo .env
Los pasos para hacer esto son:

A) Solicitar el token (API key)  en esta direccion:   https://opendata.aemet.es/centrodedescargas/inicio

B) Una vez obtenido, con el block de notas abrimos un archivo y escribiremos lo siguiente:

      TOKEN_AEMET= Insertar el codigo que nos manden aqui  

C) Guardaremos el archivo con el nombre token.env (Guardar como, ponemos el nombre con .env y en "tipo" seleccionamos   "todos los archivos")

D) En el programa de python cambiamos la linea load_dotenv("C:/espaciopython/enviroments/tokens.env")  y ponemos la ruta de nuestro archivo.  
   Si no se quiere cambiar nada en el programa, se puede crear las carpetas C:/espaciopython/enviroments  y meter el archivo en ella.


2 - LIBRERIAS

A) Para el script api_aemet (obtener datos de la API)

json
os
requests
sys
dotenv
datetime 

B) Para el script convertidor_excel  (transformar los datos de JSON a Excel)

pandas
json
os


3 - IDENTIFICADOR DE LAS ESTACIONES

El programa requiere introducir los identificadores de las estaciones que se quieran estudiar.  
Si se quiere probar con un ejemplo, estos 3 codigos corresponden a 3 estaciones de la provincia de Sevilla:  5790Y,5783,5788X

Para obtener los id de todas las estaciones, pueden buscarse aqui:  [https://datosclima.es/index.htm](https://datosclima.es/Aemethistorico/Descargahistorico.html)
En esa web puede encontrarse el siguiente enlace, que iniciara directamente ladescarga del listado de estaciones en excel:  https://datosclima.es/Aemethistorico/Archivos/ListadoEstaciones.xlsx




4 - NOTA LEGAL SOBRE EL USO DE LOS DATOS OBTENIDOS DE LA AEMET. 

Si se van a emplear los datos obtenidos de la AEMET de alguna manera mas alla de la estrictamente personal, debe leerse antes esta nota legal de la AEMET:
https://www.aemet.es/es/nota_legal




5- USO RESPONSABLE.

Hemos limitado conscientemente la peticion de datos a un rango de 6 meses, o a un año entero.
La API de AEMET admite una peticion de un rango maximo de 7 meses.  Para el año completo, el script simplemente encadena  2 peticiones.
Si se quiere solicitar datos de varios años es posible, pero recomendamos prudencia, particularmente si va a adaptarse el codigo.  
No va a suceder nada por ejecutarlo 2 o 3 veces seguidas para obtener los datos de 2 o 3 años distintos, pero si se quiere obtener los datos de muchos años por favor espacie sus consultas en el tiempo para no saturar el servidor.


De la misma forma, aunque el programa admite que se inserten varias estaciones separadas por comas, recomendamos moderacion. 
Como referencia cuando se consultan los datos de todas las estaciones directamente (funcion no incluida en este script, si lo necesita, contacte conmigo) la AEMET limita las fechas a consultar a un rango de 15 dias.
Introducir 5 o 6 estaciones en una sola consulta es razonable.  Si necesita introducir muchas mas, recomendamos lo mismo que antes: Dividirlo en varias consultas espaciadas en el tiempo.

Por lo demas, si el uso va a ser intensivo o se va a adaptar y modificar el script, recomendamos leer la documentacion disponible aqui:

https://opendata.aemet.es/centrodedescargas/inicio
https://opendata.aemet.es/centrodedescargas/docs/FAQs220424.pdf




NOTAS FINALES.

Excepto por lo ya indicado, el resto del manejo del script es bastante simple e intuitivo.
Este script nace como un pequeño proyecto personal, y cumple su funcion para lo que el autor del mismo quiere. 
No obstante, Somos conscientes de que el programa admite modificaciones, particularmente si quisiera emplearse posteriormente dentro de otro programa. 


Animamos a cualquiera interesado a cogerlo, modificarlo y adaptarlo sin miedo.




