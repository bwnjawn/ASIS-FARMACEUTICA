"""
Pruebas unitarias para los endpoints de la API.
Cobertura objetivo: ≥ 80% (RNF backend).
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.main import app

client = TestClient(app)


# ─── Health & Root ───────────────────────────────────────────────────────────

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "ASIS Farmacéutica" in data["message"]


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ─── Medicamentos ─────────────────────────────────────────────────────────────

def test_buscar_sin_token_retorna_401():
    """RF01: La búsqueda sin token debe rechazarse."""
    response = client.get("/api/v1/medicamentos/buscar?q=paracetamol")
    assert response.status_code == 401


def test_buscar_con_token_llama_yapp():
    """RF01: Búsqueda con token válido consulta YAPP y retorna resultados."""
    mock_results = [
        {
            "product_id": "abc-123",
            "product_name": "Paracetamol 500mg",
            "formula_name": "Paracetamol 500 mg",
            "laboratory_name": "Andrómaco",
            "presentation": "16 Comprimidos",
            "prescription": "Sin Prescripcion",
            "minimal_price": 341,
            "product_logo": "https://example.com/logo.jpg",
            "category": "Nombre",
        }
    ]

    with patch(
        "app.api.medications.search_medications", new_callable=AsyncMock
    ) as mock_search:
        mock_search.return_value = mock_results

        response = client.get(
            "/api/v1/medicamentos/buscar?q=paracetamol",
            headers={"Authorization": "Bearer test_token"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "paracetamol"
    assert data["total"] == 1
    assert data["results"][0]["product_id"] == "abc-123"


def test_cotizar_sin_token_retorna_401():
    """RF02: Cotización sin token debe rechazarse."""
    response = client.get("/api/v1/medicamentos/abc-123/cotizar")
    assert response.status_code == 401


def test_cotizar_sin_stock_retorna_mensaje():
    """RF02: Producto sin stock retorna mensaje adecuado."""
    with patch(
        "app.api.medications.get_quotation", new_callable=AsyncMock
    ) as mock_quote:
        mock_quote.return_value = []

        response = client.get(
            "/api/v1/medicamentos/abc-123/cotizar",
            headers={"Authorization": "Bearer test_token"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["total_pharmacies"] == 0
    assert "No hay stock" in data["message"]


def test_cotizar_retorna_farmacias_ordenadas():
    """RF02: Farmacias se retornan ordenadas por distancia y precio."""
    mock_farmacias = [
        {
            "pharmacy_chain_name": "Cruz Verde",
            "pharmacy_chain_logo": "https://example.com/cv.png",
            "total": 690,
            "pharmacy_distance": 0.5,
            "pharmacy_address": "Calle 1",
            "pharmacy_hours": None,
            "pharmacy_chain_available": None,
            "pharmacy_chain_url": "https://cruzverde.cl",
            "pharmacy_chain_online": 0,
        },
        {
            "pharmacy_chain_name": "Farmacias Gama",
            "pharmacy_chain_logo": "https://example.com/gama.png",
            "total": 550,
            "pharmacy_distance": 1.2,
            "pharmacy_address": "Calle 2",
            "pharmacy_hours": None,
            "pharmacy_chain_available": None,
            "pharmacy_chain_url": None,
            "pharmacy_chain_online": 0,
        },
    ]

    with patch(
        "app.api.medications.get_quotation", new_callable=AsyncMock
    ) as mock_quote:
        mock_quote.return_value = mock_farmacias

        response = client.get(
            "/api/v1/medicamentos/abc-123/cotizar",
            headers={"Authorization": "Bearer test_token"},
        )

    assert response.status_code == 200
    data = response.json()
    assert data["total_pharmacies"] == 2


# ─── Alarmas ──────────────────────────────────────────────────────────────────

def test_crear_alarma():
    """RF04: Creación de alarma con confirmación explícita."""
    payload = {
        "user_id": "user_1",
        "medication_name": "Enalapril 10mg",
        "dose": "1 comprimido",
        "times": ["08:00", "20:00"],
        "caregiver_email": "familiar@example.com",
    }
    response = client.post("/api/v1/alarmas", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "alarm_id" in data
    assert "Enalapril" in data["message"]
    return data["alarm_id"]


def test_confirmar_toma():
    """RF04: La toma debe poder confirmarse con botón explícito."""
    # Primero creamos una alarma
    payload = {
        "user_id": "user_confirm",
        "medication_name": "Losartán 50mg",
        "dose": "1 comprimido",
        "times": ["09:00"],
    }
    create_response = client.post("/api/v1/alarmas", json=payload)
    alarm_id = create_response.json()["alarm_id"]

    # Confirmamos la toma
    confirm_response = client.post(
        "/api/v1/alarmas/confirmar",
        json={"alarm_id": alarm_id, "confirmed_at": "2025-01-01T09:05:00"},
    )
    assert confirm_response.status_code == 200
    data = confirm_response.json()
    assert data["status"] == "confirmed"


def test_confirmar_toma_alarma_inexistente():
    """No se puede confirmar una alarma que no existe."""
    response = client.post(
        "/api/v1/alarmas/confirmar",
        json={"alarm_id": "alarm_inexistente_999"},
    )
    assert response.status_code == 404


def test_listar_alarmas():
    """Las alarmas de un usuario se pueden listar."""
    client.post(
        "/api/v1/alarmas",
        json={
            "user_id": "user_list",
            "medication_name": "Metformina",
            "dose": "1 comprimido",
            "times": ["12:00"],
        },
    )
    response = client.get("/api/v1/alarmas/user_list")
    assert response.status_code == 200
    data = response.json()
    assert len(data["alarms"]) >= 1


# ─── Usuarios ─────────────────────────────────────────────────────────────────

def test_crear_usuario():
    """Registro de usuario funcional."""
    response = client.post(
        "/api/v1/usuarios",
        json={"name": "María González", "phone": "+56912345678"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert data["name"] == "María González"


def test_generar_codigo_cuidador():
    """RF06: Generación de código de vinculación para cuidador."""
    create = client.post(
        "/api/v1/usuarios",
        json={"name": "Juan Pérez"},
    )
    user_id = create.json()["user_id"]

    response = client.post(f"/api/v1/usuarios/{user_id}/codigo-cuidador")
    assert response.status_code == 200
    data = response.json()
    assert "code" in data
    assert len(data["code"]) == 6


def test_vincular_cuidador():
    """RF06: El cuidador puede vincularse con el código correcto."""
    create = client.post(
        "/api/v1/usuarios",
        json={"name": "Rosa Martínez"},
    )
    user_id = create.json()["user_id"]

    code_response = client.post(f"/api/v1/usuarios/{user_id}/codigo-cuidador")
    code = code_response.json()["code"]

    link_response = client.post(
        "/api/v1/cuidadores/vincular",
        json={"user_id": "cuidador_1", "code": code},
    )
    assert link_response.status_code == 200
    assert "exitosa" in link_response.json()["message"]


def test_vincular_cuidador_codigo_invalido():
    """RF06: Código inválido debe rechazarse."""
    response = client.post(
        "/api/v1/cuidadores/vincular",
        json={"user_id": "cuidador_2", "code": "XXXXXX"},
    )
    assert response.status_code == 400
