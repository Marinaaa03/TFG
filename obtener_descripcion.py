# import requests
# from PIL import Image
# from io import BytesIO
# from transformers import AutoProcessor, LlavaForConditionalGeneration

# # Modelo LLaVA desde Hugging Face
# modelo = "llava-hf/llava-1.5-7b-hf"  # Asegúrate de que este modelo existe
# processor = AutoProcessor.from_pretrained(modelo)
# modelo_llava = LlavaForConditionalGeneration.from_pretrained(modelo)

# def obtener_descripcion(url_imagen):
#     """Descarga la imagen de la URL y obtiene su descripción con LLaVA."""
#     try:
#         # Descargar la imagen desde la URL
#         respuesta = requests.get(url_imagen)
#         imagen = Image.open(BytesIO(respuesta.content))

#         # Procesar la imagen con LLaVA
#         inputs = processor(images=imagen, text="Describe la imagen.", return_tensors="pt")
#         output = modelo_llava.generate(**inputs)
#         descripcion = processor.decode(output[0], skip_special_tokens=True)

#         return descripcion
#     except Exception as e:
#         return f"Error al procesar la imagen: {e}"

# #URL de la imagen que deseas describir
# url_imagen = "https://www.ikea.com/es/es/images/products/alex-cajonera-blanco__0977775_pe813763_s5.jpg?f=xxs"

# #Obtener y mostrar la descripción
# descripcion = obtener_descripcion(url_imagen)
# print(f"Descripción de la imagen: {descripcion}")





# import requests
# import base64

# #Obtenemos la imagen
# image_url = "https://www.ikea.com/es/es/images/products/sandsberg-mesa-negro__1074348_pe856162_s5.jpg?f=xxs"
# image_response = requests.get(image_url)

# #La convertimos a base64
# image_base64 = base64.b64encode(image_response.content).decode('utf-8')


# API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
# # API_URL = "https://api-inference.huggingface.co/models/Ayansk11/Image_Caption_using_ViT_GPT2"
# headers = {"Authorization": "Bearer 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"}


# data = {"image": image_base64, "question": "Describe the image in detail"}

# response = requests.post(API_URL, headers=headers, json=data)

# print(response.json())

# #https://huggingface.co/Salesforce/blip-image-captioning-base

from transformers import AutoProcessor, AutoModelForImageTextToText
import torch

model_path = "HuggingFaceTB/SmolVLM2-2.2B-Instruct"
processor = AutoProcessor.from_pretrained(model_path)
model = AutoModelForImageTextToText.from_pretrained(
    model_path,
    torch_dtype=torch.bfloat16,
    _attn_implementation="flash_attention_2"
).to("cuda")

messages = [
    {
        "role": "user",
        "content": [
            {"type": "image", "url": "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/bee.jpg"},
            {"type": "text", "text": "Can you describe this image?"},
        ]
    },
]

inputs = processor.apply_chat_template(
    messages,
    add_generation_prompt=True,
    tokenize=True,
    return_dict=True,
    return_tensors="pt",
).to(model.device, dtype=torch.bfloat16)

generated_ids = model.generate(**inputs, do_sample=False, max_new_tokens=64)
generated_texts = processor.batch_decode(
    generated_ids,
    skip_special_tokens=True,
)
print(generated_texts[0])
