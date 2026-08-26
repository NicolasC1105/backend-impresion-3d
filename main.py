from fastapi import FastAPI, File, UploadFile, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import os

app = FastAPI()
security = HTTPBasic()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("pedidos_recibidos", exist_ok=True)
base_de_datos = []

# --- 🔒 SISTEMA DE SEGURIDAD ---
def verificar_admin(credentials: HTTPBasicCredentials = Depends(security)):
    # ¡Cambia tu usuario y contraseña aquí!
    usuario_correcto = secrets.compare_digest(credentials.username, "kubo")
    clave_correcta = secrets.compare_digest(credentials.password, "admin123")
    
    if not (usuario_correcto and clave_correcta):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Acceso denegado a la bóveda de Kubo Studio",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# --- RUTAS PÚBLICAS (El cliente no necesita clave) ---
@app.post("/test-pedido/")
async def simular_pedido(
    nombre: str = Form(...),
    telefono: str = Form(...),
    material: str = Form(...),
    archivo: UploadFile = File(...)
):
    ruta_archivo = f"pedidos_recibidos/{archivo.filename}"
    with open(ruta_archivo, "wb") as buffer:
        buffer.write(await archivo.read())
    
    base_de_datos.append({
        "nombre": nombre,
        "telefono": telefono,
        "material": material,
        "archivo": archivo.filename
    })
    return {"estado": "Éxito"}

# --- RUTAS PRIVADAS (Protegidas por contraseña) ---
@app.get("/admin", response_class=HTMLResponse)
async def panel_administrador(usuario: str = Depends(verificar_admin)):
    html = """
    <html><head><title>Admin KUBO</title>
    <style>body{font-family: sans-serif; padding: 20px;} table{width: 100%; border-collapse: collapse;} th, td{border: 1px solid #ddd; padding: 8px; text-align: left;} th{background-color: #7c3aed; color: white;}</style>
    </head><body>
    <h1>Panel de Control - KUBO STUDIO 3D</h1>
    <table><tr><th>Cliente</th><th>WhatsApp</th><th>Material</th><th>Archivo 3D</th></tr>
    """
    for pedido in base_de_datos:
        html += f"<tr><td>{pedido['nombre']}</td><td>{pedido['telefono']}</td><td>{pedido['material']}</td><td><a href='/descargar/{pedido['archivo']}'>📥 Descargar</a></td></tr>"
    
    html += "</table></body></html>"
    return html

@app.get("/descargar/{nombre_archivo}")
async def descargar_archivo(nombre_archivo: str, usuario: str = Depends(verificar_admin)):
    ruta = f"pedidos_recibidos/{nombre_archivo}"
    if os.path.exists(ruta):
        return FileResponse(ruta, filename=nombre_archivo)
    return {"error": "Archivo no encontrado"}
