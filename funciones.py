import json
import sqlite3


#Función para cargar productos desde un archivo JSON
def cargar_productos_json(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as file:
        return json.load(file)

#Función que crea las tablas
def crear_tablas(conn):
    cursor = conn.cursor()

    # Creamos las tablas si no existen
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        precio REAL NOT NULL,
        url_imagen TEXT,
        tienda_origen TEXT NOT NULL
    )""")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS busquedas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        termino TEXT NOT NULL,  
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS busquedas_productos (
        busqueda_id INTEGER,
        producto_id INTEGER,
        FOREIGN KEY (busqueda_id) REFERENCES busquedas(id),
        FOREIGN KEY (producto_id) REFERENCES productos(id),
        PRIMARY KEY (busqueda_id, producto_id)
    )""")

    conn.commit()
    print("Tablas creadas correctamente")

#Función que elimina las tablas
def borrar_tablas(conn):
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS productos")
    cursor.execute("DROP TABLE IF EXISTS busquedas")
    cursor.execute("DROP TABLE IF EXISTS busquedas_productos")
    
    print("Tablas eliminadas correctamente")


#Función para quitarle al precio el símbolo €    
def limpiar_precio(precio):
    precio = precio.replace(" ", "").replace("€", "")  # Eliminar espacios y símbolo €
    precio = precio.replace(",", ".")  # Convertir comas a puntos
    return float(precio) 

# Función para obtener el id del término de búsqueda o insertarlo si no existe
def obtener_o_insertar_busqueda(conn, termino):
    cursor = conn.cursor()

    # Verificar si el término de búsqueda ya existe
    cursor.execute("SELECT id FROM busquedas WHERE termino = ?", (termino,))
    busqueda_existente = cursor.fetchone()

    if busqueda_existente:
        # Si el término ya existe, devolver su id
        print(f"Término '{termino}' encontrado en la base de datos.")
        return busqueda_existente[0]
    else:
        # Si el término no existe, insertarlo y devolver su id
        cursor.execute("INSERT INTO busquedas (termino) VALUES (?)", (termino,))
        conn.commit()  # Guardar cambios
        print(f"Término '{termino}' insertado en la base de datos.")
        return cursor.lastrowid 
        
    

#Función para insertar los productos del json a la base de datos
def insertar_productos(termino):
    # Conectar a SQLite
    conn = sqlite3.connect("base_datos.db")
    cursor = conn.cursor()

    productos = cargar_productos_json("resultados.json")
    id_busqueda = obtener_o_insertar_busqueda(conn, termino)

    # Insertar datos en la base de datos
    for producto in productos:
        # Limpiar el precio eliminando el símbolo "€" y convirtiéndolo a float
        precio_limpio = limpiar_precio(producto["precio"])

        cursor.execute("""
            INSERT OR IGNORE INTO productos (nombre, precio, url_imagen, tienda_origen) 
            VALUES (?, ?, ?, ?)
            """, (producto["nombre"], precio_limpio, producto["url_imagen"], producto["tienda_origen"]))

        
        producto_id = cursor.lastrowid  # Aquí obtenemos el ID del producto recién insertado
        
        # Insertar la relación entre el término de búsqueda y el producto
        cursor.execute("""
            INSERT OR IGNORE INTO busquedas_productos (busqueda_id, producto_id)  
            VALUES (?, ?)
            """, (id_busqueda, producto_id))

    conn.commit()  # Guardar cambios

    print("\nProductos insertados correctamente\n")
    conn.close()
    

#Función que verifica si la búsqueda ya está en la base de datos y devuelve los productos
def buscar_en_bd(conn, termino, visualizacion = False):
    cursor = conn.cursor()

    # Paso 1: Obtener el ID del término de búsqueda
    cursor.execute("SELECT id FROM busquedas WHERE termino = ?", (termino,))
    busqueda = cursor.fetchone()

    if busqueda:
        busqueda_id = busqueda[0]
        print(f"Término de búsqueda '{termino}' encontrado con ID {busqueda_id}")

        # Paso 2: Buscar los productos asociados al término de búsqueda en la tabla busquedas_productos
        cursor.execute("""
            SELECT productos.id, productos.nombre, productos.precio, productos.tienda_origen, productos.url_imagen
            FROM productos
            JOIN busquedas_productos ON productos.id = busquedas_productos.producto_id
            WHERE busquedas_productos.busqueda_id = ?
        """, (busqueda_id,))

        productos = cursor.fetchall()

        if productos:
            print(f"Se han encontrado {len(productos)} productos\n")
            if visualizacion:
                for producto in productos:
                    print(producto)
            return productos
        else:
            print(f"No se encontraron productos asociados con el término '{termino}'")
            return None
    else:
        print(f"No se encontró el término '{termino}' en la base de datos")
        return None
    
def visualizar_tablas(cursor):
    print("\n------------------PRODUCTOS------------------------\n")
    cursor.execute("SELECT * FROM productos")
    for row in cursor.fetchall():
        print(row)
    print("\n\n------------------BUSQUEDA------------------------\n")
    cursor.execute("SELECT * FROM busquedas")
    for row in cursor.fetchall():
        print(row)
    print("\n\n---------------BÚSQUEDAS PRODUCTOS------------------------\n")
    cursor.execute("SELECT * FROM busquedas_productos")
    for row in cursor.fetchall():
        print(row)
    
