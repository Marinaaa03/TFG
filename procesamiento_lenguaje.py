import spacy
from sentence_transformers import SentenceTransformer, util
from funciones import cargar_productos_json
from web_scrapping import web_scrapping_global


#Función para extraer un producto y sus atributos dada una frase
def extraer_producto_y_atributos(frase):
    doc = nlp(frase.lower())

    producto = None
    atributos = []

    for token in doc:
        # El primer sustantivo detectado es el producto
        if token.pos_ == "NOUN" and producto is None:
            producto = token.text
        # Cualquier otro sustantivo o adjetivo podría ser un atributo
        elif token.pos_ in ["NOUN", "ADJ"]:
            atributos.append(token.text)

    return producto, atributos


#Función para filtrar productos de acuerdo a sus atributos
def filtrar_productos_semanticos(productos, atributos_usuario):
    productos_filtrados = []
    atributos_embedding = modelo.encode(" ".join(atributos_usuario))

    for producto in productos:
        descripcion_embedding = modelo.encode(producto['nombre'])
        
        # Calcular similitud de coseno entre atributos y descripción
        score = util.cos_sim(atributos_embedding, descripcion_embedding).item()

        if score > 0.3:  # Umbral ajustable
            productos_filtrados.append((producto, score))

    # Ordenar por mayor similitud
    productos_filtrados.sort(key=lambda x: x[1], reverse=True)

    # if len(productos_filtrados) == 0:
    #     return productos
    # else:
    #     
    return [p[0] for p in productos_filtrados]




# Cargamos modelo en español
nlp = spacy.load("es_core_news_md")
# Cargar modelo de embeddings en español
modelo = SentenceTransformer("hiiamsid/sentence_similarity_spanish_es")


#El usuario aporta la información de la que se extrae el producto y sus atributos
frase_usuario = input("¿Qué desea? ") 
producto, atributos = extraer_producto_y_atributos(frase_usuario)
print(f"Producto: {producto}, Atributos: {atributos}")

web_scrapping_global(producto)
productos = cargar_productos_json("resultados.json")


productos_recomendados = filtrar_productos_semanticos(productos, atributos)
print("\nProductos recomendados:")
for producto in productos_recomendados:
    print(f"Nombre: {producto['nombre']}")
    print(f"Precio: {producto['precio']}")
    print(f"Imagen: {producto['url_imagen']}")
    print(f"Tienda: {producto['tienda_origen']}\n")
