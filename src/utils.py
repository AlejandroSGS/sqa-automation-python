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