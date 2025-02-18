import requests
from PIL import Image
from io import BytesIO
from transformers import AutoProcessor, LlavaForConditionalGeneration

# Modelo LLaVA desde Hugging Face
modelo = "llava-hf/llava-1.5-7b-hf"  # Asegúrate de que este modelo existe
processor = AutoProcessor.from_pretrained(modelo)
modelo_llava = LlavaForConditionalGeneration.from_pretrained(modelo)

def obtener_descripcion(url_imagen):
    """Descarga la imagen de la URL y obtiene su descripción con LLaVA."""
    try:
        # Descargar la imagen desde la URL
        respuesta = requests.get(url_imagen)
        imagen = Image.open(BytesIO(respuesta.content))

        # Procesar la imagen con LLaVA
        inputs = processor(images=imagen, text="Describe la imagen.", return_tensors="pt")
        output = modelo_llava.generate(**inputs)
        descripcion = processor.decode(output[0], skip_special_tokens=True)

        return descripcion
    except Exception as e:
        return f"Error al procesar la imagen: {e}"

#URL de la imagen que deseas describir
url_imagen = "https://www.ikea.com/es/es/images/products/alex-cajonera-blanco__0977775_pe813763_s5.jpg?f=xxs"

#Obtener y mostrar la descripción
descripcion = obtener_descripcion(url_imagen)
print(f"Descripción de la imagen: {descripcion}")