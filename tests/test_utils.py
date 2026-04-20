import pytest
from src.utils import buscar_test_por_id, calcular_promedio_tiempo, filtrar_por_tiempo

# ══════════════════════════════════════════════════════
# DISEÑO DE CASOS DE PRUEBA — filtrar_por_tiempo()
# Técnicas: Partición de equivalencia + Valores límite
# ══════════════════════════════════════════════════════

# PARTICIÓN DE EQUIVALENCIA
# ─────────────────────────
# Grupo 1 — tiempo_max válido (int o float)
#   TC_FT_001: tiempo_max = 2.0  → retorna tests con tiempo > 2.0
#   TC_FT_002: tiempo_max = 0.0  → retorna todos los tests
#   TC_FT_003: tiempo_max = 99.0 → retorna lista vacía

# Grupo 2 — tiempo_max inválido
#   TC_FT_004: tiempo_max = "2.0" → TypeError
#   TC_FT_005: tiempo_max = None  → TypeError
#   TC_FT_006: tiempo_max = []    → TypeError

# VALORES LÍMITE
# ──────────────
#   TC_FT_007: tiempo = tiempo_max exacto (2.0 == 2.0) → NO incluye
#   TC_FT_008: tiempo = tiempo_max + 0.01 (2.01 > 2.0) → SÍ incluye
#   TC_FT_009: tiempo = tiempo_max - 0.01 (1.99 < 2.0) → NO incluye

# CASOS POSITIVOS
# ───────────────
#   TC_FT_010: lista con 1 test lento  → retorna ese test
#   TC_FT_011: lista con todos lentos  → retorna todos

# CASOS NEGATIVOS
# ───────────────
#   TC_FT_012: lista vacía             → retorna []
#   TC_FT_013: ningún test supera max  → retorna []

@pytest.fixture
def suite():
    return[
        {"id": "TC_001", "estado": "PASSED", "tiempo": 1.0},
        {"id": "TC_002", "estado": "PASSED", "tiempo": 3.0},
        {"id": "TC_003", "estado": "FAILED", "tiempo": 2.0},
    ]
def test_calcular_promedio_tiempo(suite):
    resultado = calcular_promedio_tiempo(suite)
    assert resultado == 2.0, f"Esperado 2.0, pero se obtuvo {resultado}"
    
def test_promedio_lista_vacia(suite):
    resultado = calcular_promedio_tiempo([])
    assert resultado == 0.0, f"Esperado 0.0 para lista vacía, pero se obtuvo {resultado}"

def test_buscar_retorna_test_correcto(suite):
    resultado = buscar_test_por_id(suite, "TC_003")
    assert resultado["id"] == "TC_003", f"Esperado 'TC_003', pero se obtuvo {resultado['id']}"
    
def test_buscar_retorna_none_si_no_encuentra(suite):
    resultado = buscar_test_por_id(suite, "TC_999")
    assert resultado is None, f"Esperado None para test no encontrado, pero se obtuvo {resultado}"
    
def test_buscar_lanza_error_id_vacio(suite):
    try:
        buscar_test_por_id(suite, "")
        assert False, "Se esperaba ValueError para id vacío, pero no se lanzó"
    except ValueError as e:
        assert str(e) == "El test_id no puede estar vacio o contener espacios.", f"Mensaje de error inesperado: {e}"
        
def test_filtrar_retrona_test_lentos(suite):
    resultado = filtrar_por_tiempo(suite, 2.5)
    assert len(resultado) == 1 and resultado[0]["id"] == "TC_002", f"Esperado solo 'TC_002', pero se obtuvo {resultado}"
    
def test_filtrar_lanza_error_tipo_invalido():
    tests = [{"id": "TC_001", "estado": "PASSED", "tiempo": 1.0}]
    with pytest.raises(TypeError):
        filtrar_por_tiempo(tests, "2.5")
        
# TC_FT_002
def test_filtrar_tiempo_max_cero_retorna_todos(suite):
    resultado = filtrar_por_tiempo(suite, 0.0)
    assert len(resultado) == 3

# TC_FT_003
def test_filtrar_tiempo_max_alto_retorna_vacio(suite):
    resultado = filtrar_por_tiempo(suite, 99.0)
    assert resultado == []

# TC_FT_007 — valor límite exacto
def test_filtrar_tiempo_exacto_no_incluye():
    tests = [{"id": "TC_001", "estado": "PASSED", "tiempo": 2.0}]
    resultado = filtrar_por_tiempo(tests, 2.0)
    assert resultado == []  # 2.0 > 2.0 es False

# TC_FT_012
def test_filtrar_lista_vacia_retorna_vacia():
    resultado = filtrar_por_tiempo([], 2.0)
    assert resultado == []

# TC_FT_005
def test_filtrar_none_lanza_type_error():
    with pytest.raises(TypeError):
        filtrar_por_tiempo([], None)