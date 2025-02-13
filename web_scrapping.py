import json
from web_scrapping_ikea import web_scrapping_ikea
from web_scrapping_conforama import web_scrapping_conforama_tipo1, web_scrapping_conforama_tipo2

def web_scrapping_global(producto):
    #Obtenemos los resultados del producto en diferentes tiendas
    resultados = web_scrapping_ikea(producto)
    resultados += web_scrapping_conforama_tipo1(producto)
    resultados += web_scrapping_conforama_tipo2(producto)


    #Añadimos el id a los productos
    for i, resultado in enumerate(resultados, start=1):  
        resultado["id"] = i

    #Escribimos los cambios en el archivo json
    with open("resultados.json", "w", encoding="utf-8") as file:
        json.dump(resultados, file, ensure_ascii=False, indent=4)

    #Mostramos el resultado
    #print(json.dumps(resultados, indent=2, ensure_ascii=False))


# if __name__ == "__main__":
#     web_scrapping_global("mesa salón")
