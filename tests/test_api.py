from fastapi.testclient import TestClient
from ml.api import app

# Creamos un cliente de pruebas que simula peticiones a tu API
client = TestClient(app)

def test_health_check():
    """Prueba 1: Verifica que el servidor enciende y responde"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_aerodynamic_physics():
    """Prueba 2: Verifica que la IA respeta las leyes de la física"""
    # Enviamos una petición de vuelo estable: AoA 5°, 30 m/s
    response = client.post("/predict/", json={"angle_of_attack": 5.0, "velocity": 30.0})
    assert response.status_code == 200
    
    data = response.json()
    
    # Extraemos las fuerzas calculadas por tu Red Neuronal
    drag = data["forces_newtons"]["drag_force"]
    cl = data["coefficients"]["C_L"]
    
    # LEYES FÍSICAS A COMPROBAR:
    # 1. El arrastre (Drag) NUNCA puede ser negativo (es físicamente imposible).
    assert drag > 0, "Error físico: El arrastre no puede ser negativo."
    
    # 2. A 5 grados de inclinación, el perfil NACA 0012 DEBE generar sustentación positiva.
    assert cl > 0, "Error físico: Un AoA positivo debería generar sustentación positiva."

def test_stall_warning():
    """Prueba 3: Verifica los límites de seguridad de la API"""
    # Enviamos un ángulo de ataque destructivo (fuera de los límites permitidos)
    response = client.post("/predict/", json={"angle_of_attack": 25.0, "velocity": 30.0})
    
    # La API debería bloquear esto con un código de error 400 (Bad Request)
    assert response.status_code == 400
    assert "El ángulo de ataque debe estar entre -20 y 20" in response.json()["detail"]