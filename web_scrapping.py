from web_scrapping_ikea import *
from web_scrapping_conforama import *
from funciones import *
import sqlite3

def web_scrapping_global(producto):
    #Obtenemos los resultados del producto en diferentes tiendas
    resultados = web_scrapping_ikea(producto)
    resultados += web_scrapping_conforama_tipo1(producto)
    resultados += web_scrapping_conforama_tipo2(producto)

    #Escribimos los cambios en el archivo json
    with open("resultados.json", "w", encoding="utf-8") as file:
        json.dump(resultados, file, ensure_ascii=False, indent=4)

    #Mostramos el resultado
    #print(json.dumps(resultados, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    # web_scrapping_global("mesa")
    termino_busqueda = "mesa"

    #Nos conectamos a nuestra base de datos de SQLite
    conn = sqlite3.connect("base_datos.db")
    #Creamos el cursor para realizar peticiones a la base de datos
    cursor = conn.cursor()

    #Creamos las tablas
    #borrar_tablas(conn)
    crear_tablas(conn)

    #Comprobamos si el término ha sido previamente buscado (es decir, si hay información en la base de datos)
    resultados = buscar_en_bd(conn, termino_busqueda, True)

    #En caso de que no haya coincidencias llevamos a cabo web scrapping e introducimos los resultados en nuestra base de datos
    if(resultados == None):
        print(f"Realizando la búsqueda de {termino_busqueda}")
        web_scrapping_global(termino_busqueda)
        insertar_productos(conn, termino_busqueda)
    
        #Visualizamos los resultados
        resultados = buscar_en_bd(conn, termino_busqueda, True)

    #Visualizamos las tablas creadas
    #visualizar_tablas(cursor)

    #Cerramos la conexión
    conn.close()
