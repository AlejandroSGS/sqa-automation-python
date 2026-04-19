import json

class SuiteDePruebas:
    def __init__(self, archivo: str) -> None:
        self.conteo = {"PASSED": 0, "FAILED": 0, "SKIPPED": 0}
        self.pass_rate = 0.0
        self.archivo = archivo
        self.resultados = []
    def cargar(self) -> None:
        #lee desde self.archivo y carga resultados desde json.laod
        #guarda en self.resultados
        with open(self.archivo, "r", encoding="utf-8") as f:
            self.resultados = json.load(f)
    def analizar(self) -> None:
        #calucal self.conteo y self.pass_rate
        #reutiliza la logina de analizar_suite() para calcular conteo y pass_rate
        for test in self.resultados:
            estado = test["estado"]
            if estado in self.conteo:
                self.conteo[estado] += 1
        total = len(self.resultados) or 1
        self.pass_rate = (self.conteo["PASSED"] / total) * 100
    def obtener_fallados(self) -> list:
        return [test for test in self.resultados if test["estado"] == "FAILED"]
    def obtener_lentos(self, tiempo_max: float = 2.0) -> list:
        return [test for test in self.resultados if test["tiempo"] > tiempo_max]
    def generar_reporte(self) -> None:
        #genera reporte en consola y guarda reporte.json
        print(SEPARADOR)
        print(f"  REPORTE DE SUITE DE PRUEBAS")
        print(SEPARADOR)
        print(f"  Total de tests : {len(self.resultados)}")
        print(f"  PASSED         : {self.conteo['PASSED']}")
        print(f"  FAILED         : {self.conteo['FAILED']}")
        print(f"  SKIPPED        : {self.conteo['SKIPPED']}")
        print(SEPARADOR)
        failed_tests = self.obtener_fallados()
        print(f"  IDs fallados   : {', '.join(t['id'] for t in failed_tests)}")
        print(f"  Módulos afect. : {obtener_modulos_unicos(failed_tests)}")
        print(SEPARADOR)
        promedio = calcular_promedio_tiempo([t for t in self.resultados if t["estado"] == "PASSED"])
        print(f"  Tiempo prom.   : {promedio:.2f}s")
        print(f"  Pass rate      : {self.pass_rate:.1f}%")
        print(f"  Estado         : {evaluar_estabilidad(self.pass_rate)}")
        print(SEPARADOR)
        tests_lentos = self.obtener_lentos()
        print(f"  Tests lentos   : {', '.join(t['id'] for t in tests_lentos)}")
        print(SEPARADOR)
        reporte = {
            "total"       : len(self.resultados),
            "passed"      : self.conteo["PASSED"],
            "failed"      : self.conteo["FAILED"],
            "skipped"     : self.conteo["SKIPPED"],
            "pass_rate"   : round(self.pass_rate, 1),
            "tests_lentos": [t["id"] for t in tests_lentos],
            "estado_suite": evaluar_estabilidad(self.pass_rate),
        }
        with open("reporte.json", "w", encoding="utf-8") as f:
            json.dump(reporte, f, indent=4)
    def __str__(self) -> str:
        return f"SuiteDePruebas - {len(self.resultados)} tests, Pass rate: {self.pass_rate:.1f}%"

resultados = [
    {"id": "TC_001", "modulo": "Login",    "estado": "PASSED", "tiempo": 1.2},
    {"id": "TC_002", "modulo": "Login",    "estado": "FAILED", "tiempo": 3.5},
    {"id": "TC_003", "modulo": "Carrito",  "estado": "PASSED", "tiempo": 0.8},
    {"id": "TC_004", "modulo": "Carrito",  "estado": "PASSED", "tiempo": 1.1},
    {"id": "TC_005", "modulo": "Checkout", "estado": "FAILED", "tiempo": 5.2},
    {"id": "TC_006", "modulo": "Checkout", "estado": "SKIPPED","tiempo": 0.0},
]

SEPARADOR = "-" * 40


# ─────────────────────────────────────────
# FUNCIONES
# ─────────────────────────────────────────

def obtener_tests_por_estado(resultados: list, estado: str = "FAILED") -> list:
    return [test for test in resultados if test["estado"] == estado]


def calcular_promedio_tiempo(tests: list) -> float:
    if not tests:
        return 0.0
    return sum(t["tiempo"] for t in tests) / len(tests)


def obtener_modulos_unicos(tests: list) -> set:
    return {test["modulo"] for test in tests}


def evaluar_estabilidad(porcentaje: float, umbral: float = 80.0) -> str:
    if porcentaje >= umbral:
        return "SUITE ESTABLE"
    return "SUITE INESTABLE — se requiere revisión"


def analizar_suite(resultados: list) -> tuple[dict, float]:
    """Devuelve (conteo_por_estado, porcentaje_passed)."""
    conteo = {"PASSED": 0, "FAILED": 0, "SKIPPED": 0}
    for test in resultados:
        estado = test["estado"]
        if estado in conteo:
            conteo[estado] += 1
    total = len(resultados) or 1
    porcentaje_passed = (conteo["PASSED"] / total) * 100
    return conteo, porcentaje_passed


def buscar_test_por_id(resultados: list, test_id: str) -> dict | None:
    if not test_id.strip():
        raise ValueError("El test_id no puede estar vacio o contener espacios.")
    for test in resultados:
        if test["id"] == test_id:
            return test
    return None


def filtrar_por_tiempo(resultados: list, tiempo_max: float = 2.0) -> list:
    if not isinstance(tiempo_max, (int, float)):
        raise TypeError("El tiempo debe ser un valor int o float")
    return [test for test in resultados if test["tiempo"] > tiempo_max]


def ejecutar_busqueda(resultados: list, test_id: str) -> dict | None:
    try:
        resultado = buscar_test_por_id(resultados, test_id)
        return resultado
    except ValueError as e:
        print(f"[ERROR] {e}")
        return None


def generar_reporte() -> None:
    """Lee desde resultados.json, genera reporte en consola y guarda reporte.json."""
    with open("resultados.json", "r", encoding="utf-8") as f:
        resultados = json.load(f)

    conteo, porcentaje = analizar_suite(resultados)
    passed_tests       = obtener_tests_por_estado(resultados, "PASSED")
    failed_tests       = obtener_tests_por_estado(resultados, "FAILED")
    tests_lentos       = filtrar_por_tiempo(resultados, 2.0)
    promedio           = calcular_promedio_tiempo(passed_tests)

    print(SEPARADOR)
    print(f"  REPORTE DE SUITE DE PRUEBAS")
    print(SEPARADOR)
    print(f"  Total de tests : {len(resultados)}")
    print(f"  PASSED         : {conteo['PASSED']}")
    print(f"  FAILED         : {conteo['FAILED']}")
    print(f"  SKIPPED        : {conteo['SKIPPED']}")
    print(SEPARADOR)
    print(f"  IDs fallados   : {', '.join(t['id'] for t in failed_tests)}")
    print(f"  Módulos afect. : {obtener_modulos_unicos(failed_tests)}")
    print(SEPARADOR)
    print(f"  Tiempo prom.   : {promedio:.2f}s")
    print(f"  Pass rate      : {porcentaje:.1f}%")
    print(f"  Estado         : {evaluar_estabilidad(porcentaje)}")
    print(SEPARADOR)
    print(f"  Tests lentos   : {', '.join(t['id'] for t in tests_lentos)}")
    print(SEPARADOR)

    reporte = {
        "total"       : len(resultados),
        "passed"      : conteo["PASSED"],
        "failed"      : conteo["FAILED"],
        "skipped"     : conteo["SKIPPED"],
        "pass_rate"   : round(porcentaje, 1),
        "tests_lentos": [t["id"] for t in tests_lentos],
        "estado_suite": evaluar_estabilidad(porcentaje),
    }

    with open("reporte.json", "w", encoding="utf-8") as f:
        json.dump(reporte, f, indent=4)

    print("  [OK] reporte.json guardado")
    print(SEPARADOR)


# ─────────────────────────────────────────
# EJECUCIÓN PRINCIPAL
# ─────────────────────────────────────────

# 1. Guardar datos en archivo
with open("resultados.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, indent=4)

# 2. Reporte completo
print("\n>>> REPORTE COMPLETO")
generar_reporte()

# 3. Buscar un test que existe
print("\n>>> BÚSQUEDA DE TEST")
test_encontrado = buscar_test_por_id(resultados, "TC_003")
if test_encontrado:
    print(f"  Encontrado: {test_encontrado}")
else:
    print("  Test no encontrado")

# 4. Buscar un test que NO existe
test_inexistente = buscar_test_por_id(resultados, "TC_999")
if test_inexistente:
    print(f"  Encontrado: {test_inexistente}")
else:
    print("  TC_999 no existe en la suite")

# 5. Prueba ejecutar_busqueda con ID vacío
print("\n>>> PRUEBA ejecutar_busqueda")
ejecutar_busqueda(resultados, "")
ejecutar_busqueda(resultados, "   ")

print("\n>>> PRUEBA CLASE SuiteDePruebas")
suite = SuiteDePruebas("resultados.json")
suite.cargar()
suite.analizar()
suite.generar_reporte()
print(suite)