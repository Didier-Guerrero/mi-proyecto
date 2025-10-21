import json
from app.api import app
from app.validator import validar_cedula, validar_con_tiempo

def test_validar_cedula_valida():
    result = validar_cedula("1710034065")
    assert result["valida"] is True
    assert result["tipo"] == "natural"

def test_validar_cedula_invalida():
    result = validar_cedula("1710034064")
    assert result["valida"] is False

def test_validar_con_tiempo_incluye_duracion():
    result = validar_con_tiempo("1710034065")
    assert "tiempo_validacion" in result

def test_status_endpoint():
    client = app.test_client()
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_validar_endpoint_devuelve_json():
    client = app.test_client()
    response = client.post("/validar", json={"cedula": "1710034065"})
    data = json.loads(response.data)
    assert response.status_code == 200
    assert data["valida"] is True
    assert "nombre_simulado" in data or "error" in data
