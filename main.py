from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creamos una bóveda interna en el servidor
os.makedirs("pedidos_recibidos", exist_ok=True)

# Esta será nuestra "Base de datos" temporal
base_de_datos = []

@app.post("/test-pedido/")
async def simular_pedido(
    nombre: str = Form(...),
    telefono: str = Form(...),
    material: str = Form(...),
    archivo: UploadFile = File(...)
):
    # 1. Guardamos el archivo físicamente en el servidor
    ruta_archivo = f"pedidos_recibidos/{archivo.filename}"
    with open(ruta_archivo, "wb") as buffer:
        buffer.write(await archivo.read())
    
    # 2. Guardamos los datos del cliente en la memoria
    base_de_datos.append({
        "nombre": nombre,
        "telefono": telefono,
        "material": material,
        "archivo": archivo.filename
    })
    
    return {"estado": "Éxito"}

# --- RUTAS SECRETAS PARA EL ADMINISTRADOR ---

@app.get("/admin", response_class=HTMLResponse)
async def panel_administrador():
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
async def descargar_archivo(nombre_archivo: str):
    ruta = f"pedidos_recibidos/{nombre_archivo}"
    if os.path.exists(ruta):
        return FileResponse(ruta, filename=nombre_archivo)
    return {"error": "Archivo no encontrado"}
