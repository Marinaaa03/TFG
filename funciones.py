import json
from web_scrapping import *

#Función para cargar productos desde un archivo JSON
def cargar_productos_json(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as file:
        return json.load(file)

#Función para crear las tablas (si no existen)
def crear_tablas(conn):
    cursor = conn.cursor()

    #TABLA PRODUCTOS
    cursor.execute(""" CREATE TABLE IF NOT EXISTS productos (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nombre TEXT NOT NULL,
                            precio REAL NOT NULL,
                            url_imagen TEXT,
                            tienda_origen TEXT NOT NULL, 
                            url_acceso TEXT NOT NULL,
                            descripcion TEXT,
                            atributos TEXT)""")

    #TABLA BUSQUEDAS
    cursor.execute(""" CREATE TABLE IF NOT EXISTS busquedas (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,  
                            termino TEXT NOT NULL,  
                            fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

    #TABLA BUSQUEDAS_PRODUCTOS (Conecta los productos con su búsqueda asociada)
    cursor.execute(""" CREATE TABLE IF NOT EXISTS busquedas_productos (
                            busqueda_id INTEGER,
                            producto_id INTEGER,
                            FOREIGN KEY (busqueda_id) REFERENCES busquedas(id),
                            FOREIGN KEY (producto_id) REFERENCES productos(id),
                            PRIMARY KEY (busqueda_id, producto_id) )""")

    #Guardamos los cambios
    conn.commit()
    print("Tablas creadas correctamente")

#Función para eliminar las tablas (si existen)
def borrar_tablas(conn):
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS productos")
    cursor.execute("DROP TABLE IF EXISTS busquedas")
    cursor.execute("DROP TABLE IF EXISTS busquedas_productos")
    
    print("Tablas eliminadas correctamente")


#Función para quitarle al precio los espacios, el símbolo € y transformar las comas en puntos (dejar el precio limpio en la base de datos)    
def limpiar_precio(precio):
    precio = precio.replace(" ", "").replace("€", "") 
    precio = precio.replace(",", ".")  
    return float(precio) 

#Función para obtener el id del término de búsqueda e insertarlo si no existiese
def obtener_o_insertar_busqueda(conn, termino):
    cursor = conn.cursor()

    #Comprobamos si el término ya existe
    cursor.execute("SELECT id FROM busquedas WHERE termino = ?", (termino,))
    busqueda_existente = cursor.fetchone()

    #Si el término existe, devolvemos su id. En caso contrario, lo insertamos y, de nuevo, devolvemos su id
    if busqueda_existente:
        print(f"Término '{termino}' encontrado en la base de datos.")
        return busqueda_existente[0]
    else:
        cursor.execute("INSERT INTO busquedas (termino) VALUES (?)", (termino,))
        conn.commit()  
        print(f"Término '{termino}' insertado en la base de datos.")
        return cursor.lastrowid 
        
    

#Función para insertar los productos del json (tras haber realizado web scrapping) a la base de datos
def insertar_productos(conn, termino):
    cursor = conn.cursor()

    #Cargamos los productos del archivo json
    productos = cargar_productos_json("resultados.json")
    #Obtenemos su id de búsqueda asociado
    id_busqueda = obtener_o_insertar_busqueda(conn, termino)

    for producto in productos:
        #Limpiamos el precio asociado a cada prodcuto
        precio_limpio = limpiar_precio(producto["precio"])

        #Insertamos los productos en la tabla correspondiente
        cursor.execute("""INSERT OR IGNORE INTO productos (nombre, precio, url_imagen, tienda_origen, url_acceso, descripcion, atributos) VALUES (?, ?, ?, ?, ?, ?, ?)""", 
                          (producto["nombre"], precio_limpio, producto["url_imagen"], producto["tienda_origen"], producto["url_acceso"], '', ''))


        #Obtenemos el id del producto
        producto_id = cursor.lastrowid  
        
        #Insertamos el vínculo existente entre el id de la búsqueda y el id del producto
        cursor.execute("""INSERT OR IGNORE INTO busquedas_productos (busqueda_id, producto_id) VALUES (?, ?)""", 
                          (id_busqueda, producto_id))

    
    insertar_descripcion(conn)

    #Guardamos los cambios
    conn.commit() 
    print("\nProductos insertados correctamente\n")
       

#Función para comprobar si la búsqueda ya se ha realizado previamente (está en la base de datos), donde si lo está se 
#devuelven los productos (no hay necesidad de volver a repetir el proceso de web scrapping)
def buscar_en_bd(conn, termino, visualizacion = False):
    cursor = conn.cursor()

    #Obtenemos el id del término de búsqueda
    cursor.execute("SELECT id FROM busquedas WHERE termino = ?", (termino,))
    busqueda = cursor.fetchone()

    #Si existe coincidencia (si se ha buscado previamente)
    if busqueda:
        busqueda_id = busqueda[0]
        print(f"Término de búsqueda '{termino}' encontrado con ID {busqueda_id}")

        #Buscamos los productos asociados, obteniendo el id de busqueda (que coincida en la tabla busquedas y en la tabla productos_busquedas), 
        #obteniendo el id de producto (que coincida en la tabla productos_busquedas y en la tabla productos), y con ese id obtenemos el listado con los diferentes productos
        cursor.execute(""" SELECT productos.id, productos.nombre, productos.precio, productos.tienda_origen, productos.url_imagen, productos.url_acceso, productos.descripcion, productos.atributos
                           FROM productos
                           JOIN busquedas_productos ON productos.id = busquedas_productos.producto_id
                           WHERE busquedas_productos.busqueda_id = ? """, (busqueda_id,))

        productos = cursor.fetchall()

        #Si existen productos se muestra el número de productos encontrados
        if productos:
            print(f"Se han encontrado {len(productos)} productos\n")

            productos_dict = []
            for producto in productos:
                producto_dict = {
                    'id': producto[0],
                    'nombre': producto[1],
                    'precio': producto[2],
                    'tienda_origen': producto[3],
                    'url_imagen': producto[4],
                    'url_acceso': producto[5],
                    'descripcion': producto[6],
                    'atributos': producto[7]
                }
                productos_dict.append(producto_dict)

            #Si la visualización está a True se muestran los productos
            if visualizacion:
                for producto in productos:
                    print(producto)

            with open('productos_busqueda_actual.json', 'w', encoding='utf-8') as f:
                json.dump(productos_dict, f, ensure_ascii=False, indent=4)
            
            # Extraemos las URLs de las imágenes de los productos para pasárselas al modelo
            urls_productos = [producto['url_imagen'] for producto in productos_dict]
            # print(f"SE HAN BUSCADO {len(urls_productos)} PRODUCTOS")

            with open('productos_modelo.json', 'w', encoding='utf-8') as f:
                json.dump(urls_productos, f, ensure_ascii=False, indent=4)

            
            return productos_dict
        
        #Si no existen productos se indica al usuario
        else:
            print(f"No se encontraron productos asociados con el término '{termino}'")
            return None
    
    #Si no se ha buscado ese término previamente
    else:
        print(f"No se encontró el término '{termino}' en la base de datos")
        return None


#Función para visualizar las tablas creadas
def visualizar_tablas(cursor):
    #Tabla productos
    print("\n------------------PRODUCTOS------------------------\n")
    cursor.execute("SELECT * FROM productos")
    for row in cursor.fetchall():
        print(row)

    #Tabla busquedas
    print("\n\n------------------BUSQUEDA------------------------\n")
    cursor.execute("SELECT * FROM busquedas")
    for row in cursor.fetchall():
        print(row)

    #Tabla busquedas_productos
    print("\n\n---------------BÚSQUEDAS PRODUCTOS------------------------\n")
    cursor.execute("SELECT * FROM busquedas_productos")
    for row in cursor.fetchall():
        print(row)


#Función para realizar una búsqueda de productos
def busqueda(conn, termino_busqueda, visualizacion = True, borra_tablas = False):
    
    if(borra_tablas):
        borrar_tablas(conn)

    crear_tablas(conn)

    #Comprobamos si el término ha sido previamente buscado (es decir, si hay información en la base de datos)
    resultados = buscar_en_bd(conn, termino_busqueda, visualizacion)

    #En caso de que no haya coincidencias llevamos a cabo web scrapping e introducimos los resultados en nuestra base de datos
    if(resultados == None):
        print(f"Realizando la búsqueda de {termino_busqueda}")
        web_scrapping_global(termino_busqueda)
        insertar_productos(conn, termino_busqueda)
    
        #Visualizamos los resultados
        resultados = buscar_en_bd(conn, termino_busqueda, visualizacion)
    
    return resultados


#Función para completar la información de los productos (Sección del modelo descriptivo IA)
def insertar_descripcion(conn):
    cursor = conn.cursor()

    #Cargamos la información obtenida por el modelo descriptivo
    descripciones = cargar_productos_json("productos_procesados.json")

    #Recorremos la información actualizando los productos (su descripción y atributos en función del url) en la base de datos
    for prod in descripciones:
        url = prod["url"]
        descripcion = prod["descripcion"]
        atributos = prod.get("atributos", [])

        #Convertimos los atributos en una lista válida 
        if isinstance(atributos, str):
            try:
                atributos = json.loads(atributos)
            except:
                atributos = []

        #Convertimos la lista con los atributos a cadena JSON
        atributos_str = json.dumps(atributos, ensure_ascii=False)
        
        #Actualizamos la tabla de los productos
        cursor.execute("""UPDATE productos
                          SET descripcion = ?, atributos = ?
                          WHERE url_imagen = ?""", (descripcion, atributos_str, url))

    #Guardamos los cambios
    conn.commit()
    print("Base de datos actualizada con las descripciones y atributos.")


#Función encargada de realizar el filtrado de los precios (tanto ascendentemente como descendientemente)
def filtrar_productos_por_precio(productos, descendente):
    productos_ordenados = sorted(productos, key=lambda x: x['precio'], reverse=descendente)
   
    # for p in productos_ordenados:
    #     print(f"{p['nombre']} ) {p['precio']}")
    return productos_ordenados

#Función encargada de realizar el filtrado de las tiendas (para que solo se vean productos pertenecientes a las tiendas seleccionadas)
def filtrar_productos_por_tienda(productos, tiendas_seleccionadas):
    productos_tienda = []
    for prod in productos:
        if prod['tienda_origen'] in tiendas_seleccionadas:
            productos_tienda.append(prod)
    
    return productos_tienda
    


