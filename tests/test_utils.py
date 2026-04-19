import pytest
from src.utils import buscar_test_por_id, calcular_promedio_tiempo, filtrar_por_tiempo

@pytest.fixture
def suite():
    return[
        {"id": "TC_001", "estado": "PASSED", "tiempo": 1.0},
        {"id": "TC_002", "estado": "PASSED", "tiempo": 3.0},
        {"id": "TC_003", "estado": "FAILED", "tiempo": 2.0},
    ]
def test_calcular_promedio_tiempo(suite):
    # ✅ Lista de dicts — igual que los datos reales
    resultado = calcular_promedio_tiempo(suite)
    assert resultado == 2.0, f"Esperado 2.0, pero se obtuvo {resultado}"
    
def test_promedio_lista_vacia(suite):
    # ¿qué retorna calcular_promedio_tiempo([]) ?
    # assert resultado == ???
    resultado = calcular_promedio_tiempo([])
    assert resultado == 0.0, f"Esperado 0.0 para lista vacía, pero se obtuvo {resultado}"


# test 3
def test_buscar_retorna_test_correcto(suite):
    # ARRANGE — necesitas la lista de resultados y buscar TC_003
    # ACT — llama a buscar_test_por_id
    # ASSERT — verifica que el id del resultado es "TC_003"
    resultado = buscar_test_por_id(suite, "TC_003")
    assert resultado["id"] == "TC_003", f"Esperado 'TC_003', pero se obtuvo {resultado['id']}"
    
def test_buscar_retorna_none_si_no_encuentra(suite):
    # ARRANGE — necesitas la lista de resultados y buscar TC_999
    # ACT — llama a buscar_test_por_id
    # ASSERT — verifica que el resultado es None
    resultado = buscar_test_por_id(suite, "TC_999")
    assert resultado is None, f"Esperado None para test no encontrado, pero se obtuvo {resultado}"
    
def test_buscar_lanza_error_id_vacio(suite):
    # ARRANGE — necesitas la lista de resultados y un id vacío
    # ACT & ASSERT — llama a buscar_test_por_id y verifica que lanza ValueError
    try:
        buscar_test_por_id(suite, "")
        assert False, "Se esperaba ValueError para id vacío, pero no se lanzó"
    except ValueError as e:
        assert str(e) == "El test_id no puede estar vacio o contener espacios.", f"Mensaje de error inesperado: {e}"
        
def test_filtrar_retrona_test_lentos(suite):
    # ARRANGE — necesitas la lista de resultados y un umbral de tiempo
    # ACT — llama a filtrar_tests_lentos
    # ASSERT — verifica que el resultado contiene solo los tests que superan el umbral
    resultado = filtrar_por_tiempo(suite, 2.5)
    assert len(resultado) == 1 and resultado[0]["id"] == "TC_002", f"Esperado solo 'TC_002', pero se obtuvo {resultado}"
    
def test_filtrar_lanza_error_tipo_invalido():
    tests = [{"id": "TC_001", "estado": "PASSED", "tiempo": 1.0}]
    with pytest.raises(TypeError):
        filtrar_por_tiempo(tests, "2.5")