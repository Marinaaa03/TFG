from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def web_scrapping_ikea(busqueda):
   
    #Configuramos Selenium
    options = Options()
    options.add_argument("--headless")
    service = Service("/usr/local/bin/geckodriver")
    driver = webdriver.Firefox(options=options, service=service)

    
    #Obtenemos el URL del producto indicado en busqueda en la página web de IKEA
    url = f"https://www.ikea.com/es/es/search/?q={busqueda.replace(' ', '+')}"
    driver.get(url)

    #Creamos la lista con los resultados de la búsqueda
    resultados = []

    try:
        #Esperamos a que la página con los productos esté disponible
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "plp-mastercard"))
        )

        #Obtenemos el código HTML de dicha página y lo analizamos con Beautiful Soup
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        #Buscamos los productos
        productos = soup.find_all("div", class_="plp-mastercard")

        #Si existen productos obtenemos su nombre, precio, descripción, valoración y URL de la imagen
        if productos:
            # print(f"\nLos productos relacionados con '{busqueda}' son:")
            print(f"\nBuscando {busqueda} en IKEA ... ")

            for i, producto in enumerate(productos, 1):

                #Buscamos los atributos de los productos
                nombre_producto = producto.find("span", class_="plp-price-module__name-decorator")
                precio_entero_producto = producto.find("span", class_="plp-price__integer")
                precio_decimal_producto = producto.find("span", class_="plp-price__decimal")
                descripcion = producto.find("span", class_="plp-price-module__description")
                valoracion = producto.find("span", class_="plp-ratings plp-ratings--small plp-ratings--product-card notranslate")
                image_tag = producto.find("img", class_="plp-image")

                acceso_producto = producto.find("a", class_= "plp-product__image-link")

                #Procesamos el contenido 
                nombre = nombre_producto.text.strip() if nombre_producto else "Nombre no disponible"
                desc = descripcion.text.strip() if descripcion else "Descripción no disponible"
                nombre_final = f"{desc} ({nombre})"

                if precio_entero_producto:
                    precio_producto = precio_entero_producto.text.strip()

                    if precio_decimal_producto:  
                        precio_producto += f"{precio_decimal_producto.text.strip()}"

                    precio_producto = precio_producto + "€"
                
                else:
                    precio_producto = "Precio no disponible"

                if valoracion and valoracion.has_attr('aria-label'):
                    valoracion_texto = valoracion['aria-label']
                    estrellas = valoracion_texto.split("Revisa: ")[1].split("de")[0]
                    estrellas = estrellas + "estrellas"
                else:
                    estrellas = "Sin valoración"

                if image_tag and image_tag.has_attr('src'):
                    imagen = image_tag["src"] 
                else: 
                    imagen = None
                
                if acceso_producto and acceso_producto.has_attr('href'):
                    link_acceso = acceso_producto["href"]

                # #Imprimimos la información de cada producto
                # print(f"{i}. Nombre: {desc} ({nombre}) \t Precio: {precio_producto} \t Valoración: {estrellas} \t URL imagen: {imagen}\n")
                
                resultados.append({"nombre": nombre_final, "precio": precio_producto, "url_imagen": imagen, "tienda_origen": "IKEA", "url_acceso": link_acceso})

        else:
            print("No se encontraron productos relacionados.")

    except Exception as e:
        print(f"Error al cargar los productos de IKEA: {e}")

    finally:
        driver.quit()

    #Devolvemos los resultados obtenidos de la búsqueda
    return resultados

# if __name__ == "__main__":
#     web_scrapping_ikea("silla")