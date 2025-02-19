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
    # producto = request.form["producto"]
    # print(f"PRODUCTO == {producto}")
    
    # web_scrapping_global(producto)

    # # Cargar los resultados desde el archivo JSON
    # with open("productos_busqueda_actual.json", "r", encoding="utf-8") as file:
    #     resultados = json.load(file)

    # # Renderizar la plantilla y pasar los resultados a la plantilla
    # return render_template("resultados.html", resultados=resultados)


    producto = request.form["producto"]
    print(f"PRODUCTO == {producto}")

    #Nos conectamos a nuestra base de datos de SQLite
    conn = sqlite3.connect("base_datos.db")
    #cursor = conn.cursor()

    busqueda(conn, producto, False, True)

    #Visualizamos las tablas creadas
    #visualizar_tablas(cursor)

    #Cerramos la conexión
    conn.close()

    with open("productos_busqueda_actual.json", "r", encoding="utf-8") as file:
        resultados = json.load(file)

    # Renderizar la plantilla y pasar los resultados a la plantilla
    return render_template("resultados.html", resultados=resultados)

if __name__ == "__main__":
    app.run(debug=True)
