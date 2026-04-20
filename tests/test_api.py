import requests
import pytest

URL = "https://jsonplaceholder.typicode.com"

def test_get_post_retorta_200():
    response = requests.get(f"{URL}/posts/1")
    assert response.status_code == 200
    
def test_get_post_tiene_campos_correctos():
    response = requests.get(f"{URL}/posts/1")
    data = response.json()
    campos_esperados = {"id", "title", "body", "userId"}
    assert campos_esperados.issubset(data.keys())

def test_get_usuario_retorna_200():
    response = requests.get(f"{URL}/users/1")
    assert response.status_code == 200

def test_get_usuario_tiene_email():
    response = requests.get(f"{URL}/users/1")
    data = response.json()
    assert "email" in data and data["email"] != "", "El usuario debe tener un email no vacío"

def test_post_inexistente_retorna_404():
    response = requests.get(f"{URL}/posts/9999")
    assert response.status_code == 404, f"Esperado 404 para post inexistente, pero se obtuvo {response.status_code}"
    
def test_get_posts_retorna_lista():
    response = requests.get(f"{URL}/posts")
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 100