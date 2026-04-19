import json
from src.suite import SuiteDePruebas

resultados = [
    {"id": "TC_001", "modulo": "Login",    "estado": "PASSED", "tiempo": 1.2},
    {"id": "TC_002", "modulo": "Login",    "estado": "FAILED", "tiempo": 3.5},
    {"id": "TC_003", "modulo": "Carrito",  "estado": "PASSED", "tiempo": 0.8},
    {"id": "TC_004", "modulo": "Carrito",  "estado": "PASSED", "tiempo": 1.1},
    {"id": "TC_005", "modulo": "Checkout", "estado": "FAILED", "tiempo": 5.2},
    {"id": "TC_006", "modulo": "Checkout", "estado": "SKIPPED","tiempo": 0.0},
]

# 1. Guardar datos en archivo
with open("datos/resultados.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, indent=4)

# 2. Usar la clase
suite = SuiteDePruebas("datos/resultados.json")
suite.cargar()
suite.analizar()
suite.generar_reporte()
print(suite)