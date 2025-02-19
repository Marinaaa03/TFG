from web_scrapping_ikea import *
from web_scrapping_conforama import *
import json

def web_scrapping_global(producto):
    #Obtenemos los resultados del producto en diferentes tiendas
    resultados = web_scrapping_conforama_tipo2(producto)

    if(resultados == None):
        resultados = web_scrapping_conforama_tipo1(producto)

    resultados += web_scrapping_ikea(producto)


    #Escribimos los cambios en el archivo json
    with open("resultados.json", "w", encoding="utf-8") as file:
        json.dump(resultados, file, ensure_ascii=False, indent=4)

    #Mostramos el resultado
    #print(json.dumps(resultados, indent=2, ensure_ascii=False))


# if __name__ == "__main__":
#     # web_scrapping_global("mesa")
#     termino_busqueda = "armario"

#     #Nos conectamos a nuestra base de datos de SQLite
#     conn = sqlite3.connect("base_datos.db")
#     #Creamos el cursor para realizar peticiones a la base de datos
#     cursor = conn.cursor()

#     #Creamos las tablas
#     #borrar_tablas(conn)
    
#     busqueda(conn, termino_busqueda, False)

#     #Visualizamos las tablas creadas
#     #visualizar_tablas(cursor)

#     #Cerramos la conexión
#     conn.close()