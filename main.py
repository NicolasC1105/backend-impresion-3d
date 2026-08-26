from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.message import EmailMessage

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURACIÓN DE GMAIL ---
# --- CONFIGURACIÓN DE GMAIL ---
TU_CORREO = "nicolascorreaballen835@gmail.com" 
PASSWORD_APP = "momegmjifazehgrg" # Todo junto, sin espacios # Pega la clave que te dio Google

def enviar_correo_gmail(nombre, telefono, material, nombre_archivo, contenido_archivo):
    msg = EmailMessage()
    msg['Subject'] = f"🚀 NUEVO PEDIDO 3D - {nombre}"
    msg['From'] = TU_CORREO
    msg['To'] = TU_CORREO # Te lo envías a ti mismo
    
    # El cuerpo del correo
    cuerpo = f"""
    ¡Tienes un nuevo pedido desde tu web!
    
    👤 Cliente: {nombre}
    📱 WhatsApp: {telefono}
    🎨 Material: {material}
    📁 El archivo 3D viene adjunto a este correo.
    """
    msg.set_content(cuerpo)
    
    # Empaquetamos el archivo .stl o .obj
    msg.add_attachment(contenido_archivo, maintype='application', subtype='octet-stream', filename=nombre_archivo)
    
    # Conexión con el servidor de Google
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(TU_CORREO, PASSWORD_APP)
        smtp.send_message(msg)

@app.post("/test-pedido/")
async def simular_pedido(
    nombre: str = Form(...),
    telefono: str = Form(...),
    material: str = Form(...),
    archivo: UploadFile = File(...)
):
    # Leemos el archivo y disparamos el correo
    contenido = await archivo.read()
    enviar_correo_gmail(nombre, telefono, material, archivo.filename, contenido)
    
    return {"estado": "Éxito"}
