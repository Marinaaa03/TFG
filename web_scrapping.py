from web_scrapping_ikea import *
from web_scrapping_conforama import *
from funciones import *

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
    termino_busqueda = "armario"

    # Conectar a SQLite
    conn = sqlite3.connect("base_datos.db")
    cursor = conn.cursor()

    #borrar_tablas(conn)
    crear_tablas(conn)

    #Buscar en la base de datos antes de hacer Web Scraping
    resultados = buscar_en_bd(conn, termino_busqueda, True)
    if(resultados == None):
        print(f"Realizando la búsqueda de {termino_busqueda}")
        web_scrapping_global(termino_busqueda)
        insertar_productos(termino_busqueda)
    
        resultados = buscar_en_bd(conn, termino_busqueda, True)

    #Visualizar tablas
    #visualizar_tablas(cursor)

    # Cerrar conexión
    conn.close()
