from flask import Flask, request, render_template
import json
from web_scrapping import web_scrapping_global
from funciones import *
import sqlite3


app = Flask(__name__)

@app.route("/")
def index():
    # Renderiza el formulario para buscar productos
    return render_template("index.html")

@app.route("/buscar", methods=["POST"])
def buscar():
    producto = request.form["producto"]
    print(f"PRODUCTO == {producto}")
    
    web_scrapping_global(producto)

    # Cargar los resultados desde el archivo JSON
    with open("resultados.json", "r", encoding="utf-8") as file:
        resultados = json.load(file)

    # Renderizar la plantilla y pasar los resultados a la plantilla
    return render_template("resultados.html", resultados=resultados)

    # termino_busqueda = request.form["producto"]
    # print(f"PRODUCTO == {termino_busqueda}")

    # #Nos conectamos a nuestra base de datos de SQLite
    # conn = sqlite3.connect("base_datos.db")
    # #Creamos el cursor para realizar peticiones a la base de datos
    # cursor = conn.cursor()

    # #Creamos las tablas
    # #borrar_tablas(conn)
    # crear_tablas(conn)

    # #Comprobamos si el término ha sido previamente buscado (es decir, si hay información en la base de datos)
    # resultados = buscar_en_bd(conn, termino_busqueda, True)

    # #En caso de que no haya coincidencias llevamos a cabo web scrapping e introducimos los resultados en nuestra base de datos
    # if(resultados == None):
    #     print(f"Realizando la búsqueda de {termino_busqueda}")
    #     web_scrapping_global(termino_busqueda)
    #     insertar_productos(conn, termino_busqueda)
    
    #     #Visualizamos los resultados
    #     resultados = buscar_en_bd(conn, termino_busqueda, True)

    # #Visualizamos las tablas creadas
    # #visualizar_tablas(cursor)

    # #Cerramos la conexión
    # conn.close()

if __name__ == "__main__":
    app.run(debug=True)
