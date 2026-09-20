from fastapi.testclient import TestClient
from ml.api import app
import os

# Capturamos la llave
TEST_KEY = os.getenv("API_KEY", "TEST_TEMPORAL_KEY")
HEADERS = {"X-API-Key": TEST_KEY}

def test_health_check():
    # Usamos "with TestClient" para activar automáticamente el Lifespan
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 200

def test_security_access_denied():
    with TestClient(app) as client:
        response = client.post("/predict/", json={"angle_of_attack": 5.0, "velocity": 30.0})
        assert response.status_code == 401

def test_aerodynamic_physics_with_key():
    with TestClient(app) as client:
        response = client.post("/predict/", json={"angle_of_attack": 5.0, "velocity": 30.0}, headers=HEADERS)
        assert response.status_code == 200
        
        data = response.json()
        drag = data["forces_newtons"]["drag_force"]
        cl = data["coefficients"]["C_L"]
        
        assert drag > 0, "Error físico: El arrastre no puede ser negativo."
        assert cl > 0, "Error físico: Un AoA positivo debería generar sustentación positiva."

def test_stall_warning_with_key():
    with TestClient(app) as client:
        response = client.post("/predict/", json={"angle_of_attack": 25.0, "velocity": 30.0}, headers=HEADERS)
        assert response.status_code == 400