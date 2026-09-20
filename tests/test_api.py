from fastapi.testclient import TestClient
from ml.api import app
import os

client = TestClient(app)

# Capturamos la llave que GitHub Actions inyectará en la nube
TEST_KEY = os.getenv("API_KEY", "TEST_TEMPORAL_KEY")
HEADERS = {"X-API-Key": TEST_KEY}

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200

def test_security_access_denied():
    """Prueba 2: Verifica que la API rechaza peticiones sin la llave"""
    response = client.post("/predict/", json={"angle_of_attack": 5.0, "velocity": 30.0})
    assert response.status_code == 403  # 403 Forbidden

def test_aerodynamic_physics_with_key():
    """Prueba 3: Verifica las leyes de la física con la llave correcta"""
    response = client.post("/predict/", json={"angle_of_attack": 5.0, "velocity": 30.0}, headers=HEADERS)
    assert response.status_code == 200
    
    data = response.json()
    drag = data["forces_newtons"]["drag_force"]
    cl = data["coefficients"]["C_L"]
    
    assert drag > 0, "Error físico: El arrastre no puede ser negativo."
    assert cl > 0, "Error físico: Un AoA positivo debería generar sustentación positiva."

def test_stall_warning_with_key():
    """Prueba 4: Verifica los límites físicos permitidos"""
    response = client.post("/predict/", json={"angle_of_attack": 25.0, "velocity": 30.0}, headers=HEADERS)
    assert response.status_code == 400