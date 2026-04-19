import json
from src.utils import (
    analizar_suite,
    obtener_tests_por_estado,
    calcular_promedio_tiempo,
    obtener_modulos_unicos,
    evaluar_estabilidad,
    filtrar_por_tiempo,
)
SEPARADOR = "-" * 40
class SuiteDePruebas:
    def __init__(self, archivo: str) -> None:
        self.conteo = {"PASSED": 0, "FAILED": 0, "SKIPPED": 0}
        self.pass_rate = 0.0
        self.archivo = archivo
        self.resultados = []
        
    def cargar(self) -> None:
        with open(self.archivo, "r", encoding="utf-8") as f:
            self.resultados = json.load(f)
            
    def analizar(self) -> None:
        self.conteo, self.pass_rate = analizar_suite(self.resultados)
        
    def obtener_fallados(self) -> list:
        return obtener_tests_por_estado(self.resultados, "FAILED")
    
    def obtener_lentos(self, tiempo_max: float = 2.0) -> list:
        return filtrar_por_tiempo(self.resultados, tiempo_max)
    
    def generar_reporte(self) -> None:
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