from dotenv import load_dotenv
import os
from src.database import DBManager

load_dotenv(r"C:\Users\aleja\OneDrive\Desktop\SQA\.env")

resultados = [
    {"id": "TC_001", "modulo": "Login",    "estado": "PASSED", "tiempo": 1.2},
    {"id": "TC_002", "modulo": "Login",    "estado": "FAILED", "tiempo": 3.5},
    {"id": "TC_003", "modulo": "Carrito",  "estado": "PASSED", "tiempo": 0.8},
    {"id": "TC_004", "modulo": "Carrito",  "estado": "PASSED", "tiempo": 1.1},
    {"id": "TC_005", "modulo": "Checkout", "estado": "FAILED", "tiempo": 5.2},
    {"id": "TC_006", "modulo": "Checkout", "estado": "SKIPPED","tiempo": 0.0},
]

db = DBManager(
    host     = os.getenv("DB_HOST"),
    dbname   = os.getenv("DB_NAME"),
    user     = os.getenv("DB_USER"),
    password = os.getenv("DB_PASSWORD")
)

db.conectar()
db.crear_tabla()
db.insertar_resultados(resultados)
db.cerrar()
db.conectar()
fallados = db.obtener_fallos()
resumen  = db.obtener_resumen()
lentos  = db.obtener_lentos()

print(f"Fallados : {[t['id'] for t in fallados]}")
print(f"Resumen  : {resumen}")
print(f"Lentos   : {[t['id'] for t in lentos]}")
