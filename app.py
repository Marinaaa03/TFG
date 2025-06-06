from flask import Flask, request, render_template, jsonify
import json
from funciones import *
import sqlite3


app = Flask(__name__)

@app.route("/")
def index():
    #Renderizamos la plantilla inicial para buscar productos
    return render_template("index.html")

@app.route("/buscar", methods=["GET","POST"])
def buscar():
    # producto = request.form["producto"]
    # print(f"PRODUCTO == {producto}")

    if request.method == "POST":
        if request.is_json:
            data = request.get_json(silent=True) or {}
            producto = data.get("producto")
            filtro_precio = data.get("filtro_precio")
            tiendas_seleccionadas = data.get("tiendas") or []
            desde_cero = data.get("desde_cero", False)
        else:
            producto = request.form.get("producto")
            filtro_precio = request.form.get("filtro_precio")
            tiendas_seleccionadas = request.form.getlist("tiendas")  
            desde_cero = 'desde_cero' in request.form
    else:  
        producto = request.args.get("producto")
        filtro_precio = request.args.get("filtro_precio")
        tiendas_seleccionadas = request.args.getlist("tiendas")
        desde_cero = request.args.get("desde_cero") == 'true'

    
    #Nos conectamos a nuestra base de datos de SQLite
    conn = sqlite3.connect("base_datos.db")
    #cursor = conn.cursor()

    busqueda(conn, producto, False, desde_cero)

    #Visualizamos las tablas creadas
    #visualizar_tablas(cursor)

    #Cerramos la conexión
    conn.close()

    with open("productos_busqueda_actual.json", "r", encoding="utf-8") as file:
        resultados = json.load(file)

    #Por defecto seleccionamos los productos de todas las tiendas
    productos_tienda = resultados

    #Aplicamos el filtro de tiendas
    if tiendas_seleccionadas:
        productos_tienda = filtrar_productos_por_tienda(resultados, tiendas_seleccionadas)

    #Por defecto ordenamos los productos de menor a mayor precio
    productos_ordenados = filtrar_productos_por_precio(productos_tienda, False)

    #Aplicamos el filtro de precio
    if filtro_precio:
        if(filtro_precio == "asc"):
            productos_ordenados = filtrar_productos_por_precio(productos_tienda, False)
        else:
            productos_ordenados = filtrar_productos_por_precio(productos_tienda, True)

    #Renderizamos la plantilla y le pasamos los productos
    if not request.is_json:
        return render_template("resultados.html", resultados = productos_ordenados, producto = producto, filtro_precio = filtro_precio, tiendas_seleccionadas = tiendas_seleccionadas, desde_cero=desde_cero)

    #Si la petición viene de Android, devolvemos los productos en formato JSON
    return jsonify(productos_ordenados)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
