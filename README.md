This Python script is designed to aquire wheather data from Spanish Meteorologic Agency AEMET.
The rest of the document is in Spanish. (i'm spanish after all).  If you are interested on this, i recomend to use google translator.



DESCRIPCIÓN GENERAL.

El primer script (api_aemet) esta diseñado para obtener los datos meteorologicos de las estaciones de AEMET usando su API.
Al iniciar el programa, se solicitara la ID de las estaciones meteorologicas a estudiar y el rango de fechas.
El programa admite un rango de fechas de hasta 6 meses, o bien 1 año completo del 1 de Enero al 31 de Diciembre.

Los datos recibidos se descargaran en un archivo tipo JSON.




Un segundo script nos permitira obtener la informacion de todas las estaciones de España,  filtrando si se desea para quedarnos solocon aquellas que incluyen datos de irradiacion solar y presion atmosferica, o coger los datos de todas.
ATENCION. RECOMENDAMOS PRECAUCIÓN AL USAR ESTE SCRIPT SI EL RANGO DE FECHAS A SELECCIONAR VA A SER MUY AMPLIO.
SEAMOS RESPONSABLES AL USAR LOS RECURSOS DEL SERVIDOR.
SI EL RANGO DE FECHAS ES MUY AMPLIO PLANTEESE DIVIDIR LA CONSULTA EN VARIAS MAS PEQUEÑAS, Y REALIZARLAS ESPACIADA EN EL TIEMPO.


.  


Por ultimo, el tercer script (api_aemet_balance_hidrico_nacional) permite descargarse los balances hidricos nacionales publicados cada 10 dias.
Este script solicita el año  y los dias en decenas.  Por ejemplo:   si introducimos el 2021  y 26, nos bajaremos el balance hidrico nacional del año 2023, dia 260  (16 de septiembre, si no hay error por nuestra parte)
En un proximo desarrollo, se cambiara el sistema para que la introduccion de la fecha sea un poco mas intuitiva.



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



 B) Para el script del balance hidricon nacional:

os
requests
sys
dotenv 
time





3 - IDENTIFICADOR DE LAS ESTACIONES

El script para obtener datos de las estaciones requiere introducir los identificadores de las estaciones que se quieran estudiar.  
Si se quiere probar con un ejemplo, estos 3 codigos corresponden a 3 estaciones de la provincia de Sevilla:  5790Y,5783,5788X

Los id de  las estaciones pueden buscarse aqui:  [https://datosclima.es/index.htm](https://datosclima.es/Aemethistorico/Descargahistorico.html)
En esa web puede encontrarse el siguiente enlace, que iniciara directamente ladescarga del listado de estaciones en excel:  https://datosclima.es/Aemethistorico/Archivos/ListadoEstaciones.xlsx


4 - SOBRE LOS METADATOS

La API de AEMET permite descargar tambien los metadatos de las estaciones . Basicamente son la "leyenda" con la descripcion de los datos.
No obstante, los nombres asignados son muy descriptivos.  Ademas, una vez descargados son los mismos siempre.
Por ello el programa da la opcion de guardarlos o no.

Ademas aunque esten en formato json, son muy simples de entender y manejar  incluso para alguien sin formacion, asi que el programa convertidor a excel no afectara a este segundo archivo. 
Basta con abrirlo con el bloc de notas.




5 - NOTA LEGAL SOBRE EL USO DE LOS DATOS OBTENIDOS DE LA AEMET. 

Si se van a emplear los datos obtenidos de la AEMET de alguna manera mas alla de la estrictamente personal, debe leerse antes esta nota legal de la AEMET:
https://www.aemet.es/es/nota_legal




6- USO RESPONSABLE.

En el primer script (api_aemet)  hemos limitado conscientemente la peticion de datos a un rango de 6 meses, o bien a partir de ahi se salta al  año completo.
La API de AEMET para los datos de estaciones individuales admite una peticion de un rango maximo de 7 meses.  Para el año completo, el script simplemente encadena  2 peticiones.
Si se quiere solicitar datos de varios años haciendo varias consultas es posible, pero recomendamos prudencia, particularmente si va a adaptarse el codigo.  
No va a suceder nada por ejecutarlo 2 o 3 veces seguidas para obtener los datos de 2 o 3 años distintos, pero si se quiere obtener los datos de muchos años por favor espacie sus consultas en el tiempo para no saturar el servidor.


De la misma forma, aunque el programa admite que se inserten varias estaciones separadas por comas, recomendamos moderacion. 
Como referencia cuando se consultan los datos de todas las estaciones directamente (funcion no incluida en este script, si lo necesita, contacte conmigo) la AEMET limita las fechas a consultar a un rango de 15 dias.
Introducir 5 o 6 estaciones en una sola consulta es razonable.  Si necesita introducir muchas mas, recomendamos lo mismo que antes: Dividirlo en varias consultas espaciadas en el tiempo.


En el segundo script (api_aemet_todas_estaciones.py) recomendamos aun mas prudencia. El rango limite de la API para las peticiones de todas las estaciones es de 15 dias.
Nuestro script toma el rango de fechas introducido y lo divide en varias peticiones de 14 dias, encadenando estas con una parada de 5 segundos entre una y otra.
Hemos probado el script con un rango de fechas de 1 mes completo (31 dias). Hasta ahi no da problemas. 
Si se quiere un rango de fechas mas amplio, recomendamos precaución. 



Por lo demas, si el uso va a ser intensivo o se va a adaptar y modificar los scripts, recomendamos leer la documentacion disponible aqui:

https://opendata.aemet.es/centrodedescargas/inicio
https://opendata.aemet.es/centrodedescargas/docs/FAQs220424.pdf




NOTAS FINALES.

Excepto por lo ya indicado, el resto del manejo del script es bastante simple e intuitivo.
Este script nace como un pequeño proyecto personal, y cumple su funcion para lo que el autor del mismo quiere. 
No obstante, Somos conscientes de que el programa admite modificaciones, particularmente si quisiera emplearse posteriormente dentro de otro programa. 


Animamos a cualquiera interesado a cogerlo, modificarlo y adaptarlo sin miedo.




