from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TOKEN_BOT = "8204243004:AAE8RFLI30dgGZe6nKpvGAYIcZLIhDORXcM"
TU_CHAT_ID = "7024211153"

# Nueva función mejorada que envía texto + archivo adjunto
def enviar_documento_telegram(mensaje: str, nombre_archivo: str, contenido_archivo: bytes):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendDocument"
    # El texto ahora va en "caption" (la leyenda del archivo)
    payload = {"chat_id": TU_CHAT_ID, "caption": mensaje}
    # Empaquetamos el archivo físico
    archivos = {"document": (nombre_archivo, contenido_archivo)}
    
    requests.post(url, data=payload, files=archivos)

@app.post("/test-pedido/")
async def simular_pedido(
    nombre: str = Form(...),
    telefono: str = Form(...),
    material: str = Form(...),
    archivo: UploadFile = File(...)
):
    
    # 1. Leemos el archivo directamente en la memoria RAM (ya no usamos el disco duro)
    contenido = await archivo.read()

    # 2. Armamos el reporte
    mensaje = (
        f"🚀 ¡NUEVO PEDIDO RECIBIDO!\n\n"
        f"👤 Cliente: {nombre}\n"
        f"📱 WhatsApp: {telefono}\n"
        f"🎨 Material: {material}"
    )
    
    # 3. Disparamos todo junto directo a tu celular
    enviar_documento_telegram(mensaje, archivo.filename, contenido)
    
    return {"estado": "Éxito"}