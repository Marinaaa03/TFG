from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def web_scrapping_conforama_tipo1(busqueda):

    #Configuramos Selenium
    options = Options()
    options.add_argument("--headless")
    service = Service("/usr/local/bin/geckodriver")
    driver = webdriver.Firefox(options=options, service=service)

    #Obtenemos el URL del producto indicado en busqueda en la página web de Conforama
    url = f"https://www.conforama.es/?query={busqueda.replace(' ', '+')}"
    driver.get(url)

    #Creamos la lista con los resultados de la búsqueda
    resultados = []

    try:
        #Esperamos a que la página con los productos esté disponible
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "product-container-wrapper"))
        )

        #Obtenemos el código HTML de dicha página y lo analizamos con Beautiful Soup
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        #Buscamos los productos
        productos = soup.find_all("div", class_="product-container-wrapper")
        #print(len(productos))
        
        #Si existen productos obtenemos su nombre, precio, y URL de la imagen
        if productos:
            # print(f"\nLos productos relacionados con '{busqueda}' son:")
            print(f"\nBuscando {busqueda} en Conforama ... ")

            for i, producto in enumerate(productos, 1):

                #Buscamos los atributos de los productos
                nombre_producto = producto.find("h2", class_="product-title")
                precio_producto = producto.find("div", class_="selling-price")
                image_holder = producto.find("div", class_="image-holder")
                img_tag = image_holder.find("img")
                acceso_producto = producto.find("a")
                link_acceso = acceso_producto['href'] if acceso_producto else "Acceso al producto no disponible"

                #Procesamos el contenido 
                nombre = nombre_producto.text.strip() if nombre_producto else "Nombre no disponible"
                precio = precio_producto.text.strip() if precio_producto else "Precio no disponible"
                if img_tag and img_tag.has_attr('src'):
                    image = img_tag["src"] 
                else: 
                    image = None

                if acceso_producto and acceso_producto.has_attr('href'):
                    link_acceso = acceso_producto["href"]
                else:
                    link_acceso = None

                # #Imprimimos la información de cada producto
                # print(f"{i}. Nombre: {nombre} \t Precio: {precio} \t URL imagen: {image}\n") #\t Valoración: {estrellas} \t Descripción: {desc}")
                                
                resultados.append({"nombre": nombre, "precio": precio, "url_imagen": image, "tienda_origen": "Conforama", "url_acceso": link_acceso})

        else:
            print("No se encontraron productos relacionados.")

    except Exception as e:
        print(f"Error al cargar los productos de Conforama (Función 1): {type(e).__name__}")

    finally:
        driver.quit()
    
    #Devolvemos los resultados obtenidos de la búsqueda
    return resultados




def web_scrapping_conforama_tipo2(busqueda):

    #Configuramos Selenium
    options = Options()
    options.add_argument("--headless")
    service = Service("/usr/local/bin/geckodriver")
    driver = webdriver.Firefox(options=options, service=service)

    #Obtenemos el URL de la página web de Conforama
    url = "https://www.conforama.es/"
    driver.get(url)

    #Añadimos las cookies necesarias
    cookies = [{'name': 'cto_bundle', 'value': 'UiYrkV9TNzB1a1JtSjBlJTJCdGdLM2dzODc1Y0lBODZEUzN3TUZvUmJjTk4lMkJSZmZuUjR1TXlrcGVxdiUyQmMlMkJSMUZCeUlSVGJOdnZWRTdGRXhhTUIzdm1VQWpDb2RNOXp3JTJGZk43UDBYNndqUGk3YzByRjdRQzk0SURPWEZ1dnFpUVlYUGJpclg5OFo5N3FxczJLaEdKaWdNZ3RqQ05nJTNEJTNE'}]

    for cookie in cookies:
        driver.add_cookie(cookie)

    #Obtenemos el URL del producto indicado en busqueda en la página web de Conforama
    url = f"https://www.conforama.es/?query={busqueda.replace(' ', '+')}"
    driver.get(url)

    #Creamos la lista con los resultados de la búsqueda
    resultados = []

    try:
        #Esperamos a que la página con los productos esté disponible
        WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "x-result"))
        )

        #Obtenemos el código HTML de dicha página y lo analizamos con Beautiful Soup
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        #Buscamos los productos
        productos = soup.find_all("article", class_="x-result")
        #print(len(productos))
        
        #Si existen productos obtenemos su nombre, precio, y URL de la imagen
        if productos:
            # print(f"\nLos productos relacionados con '{busqueda}' son:")
            print(f"\nBuscando {busqueda} en Conforama ... ")

            for i, producto in enumerate(productos, 1):

                #Buscamos los atributos de los productos
                nombre_producto = producto.find("h2", class_="x-text2")
                precio_producto = producto.find("span", class_="x-currency")
                image_holder = producto.find("div", class_="x-result-picture")
                img_tag = image_holder.find("img")
                acceso_producto = producto.find("a", class_="x-result-link")


                #Procesamos el contenido 
                nombre = nombre_producto.text.strip() if nombre_producto else "Nombre no disponible"
                precio = precio_producto.text.strip() if precio_producto else "Precio no disponible"
                if img_tag and img_tag.has_attr('src'):
                    image = img_tag["src"] 
                else: 
                    image = None
                
                if acceso_producto and acceso_producto.has_attr('href'):
                    link_acceso = acceso_producto["href"]
                else:
                    link_acceso = None

                # #Imprimimos la información de cada producto
                #print(f"{i}. Nombre: {nombre} \t Precio: {precio} \t URL imagen: {image}\n") #\t Valoración: {estrellas} \t Descripción: {desc}")
                                
                resultados.append({"nombre": nombre, "precio": precio, "url_imagen": image, "tienda_origen": "Conforama", "url_acceso": link_acceso})

        else:
            print("No se encontraron productos relacionados.")

    except Exception as e:
        print(f"Error al cargar los productos de Conforama (Función 2): {type(e).__name__}")
        return None

    finally:
        driver.quit()
    
    #Devolvemos los resultados obtenidos de la búsqueda
    return resultados

# if __name__ == "__main__":
#     web_scrapping_conforama_tipo1("mesa salón")
#     web_scrapping_conforama_tipo2("percha")
