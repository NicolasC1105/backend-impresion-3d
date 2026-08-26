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
TU_CORREO = "nicolascorreaballen835@gmail.com" 
PASSWORD_APP = "aqui_las_16_letras_sin_espacios" # Pega tu clave real aquí

def enviar_correo_gmail(nombre, telefono, material, nombre_archivo, contenido_archivo):
    print(f"🚀 INICIANDO EL ENVÍO DE CORREO PARA: {nombre}")
    
    try:
        msg = EmailMessage()
        msg['Subject'] = f"🚀 NUEVO PEDIDO 3D - {nombre}"
        msg['From'] = TU_CORREO
        msg['To'] = TU_CORREO 
        
        cuerpo = f"""
        ¡Tienes un nuevo pedido desde tu web!
        
        👤 Cliente: {nombre}
        📱 WhatsApp: {telefono}
        🎨 Material: {material}
        """
        msg.set_content(cuerpo)
        msg.add_attachment(contenido_archivo, maintype='application', subtype='octet-stream', filename=nombre_archivo)
        
        print("🔌 Conectando con Google...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(TU_CORREO, PASSWORD_APP)
            smtp.send_message(msg)
            
        print("✅ ¡CORREO ENVIADO CON ÉXITO A GMAIL!")
        
    except Exception as e:
        print(f"❌ ERROR FATAL AL ENVIAR EL CORREO: {e}")

@app.post("/test-pedido/")
async def simular_pedido(
    nombre: str = Form(...),
    telefono: str = Form(...),
    material: str = Form(...),
    archivo: UploadFile = File(...)
):
    print(f"📦 Archivo recibido en el servidor: {archivo.filename}")
    contenido = await archivo.read()
    enviar_correo_gmail(nombre, telefono, material, archivo.filename, contenido)
    
    return {"estado": "Éxito"}
