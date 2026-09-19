from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os

# 1. Inicializar la aplicación API
app = FastAPI(
    title="Intelligent CFD API",
    description="Motor predictivo de aerodinámica (NACA 0012) impulsado por Machine Learning.",
    version="1.0.0"
)

# 2. Definir el esquema de datos esperado (Lo que otros programas deben enviarnos)
class AeroRequest(BaseModel):
    angle_of_attack: float
    velocity: float

# Variables globales para los modelos
model = None
scaler_X = None
scaler_y = None

# 3. Cargar la IA en la memoria al iniciar el servidor
@app.on_event("startup")
def load_ai_models():
    global model, scaler_X, scaler_y
    try:
        # Rutas relativas asumiendo que ejecutamos desde la raíz del proyecto
        model = joblib.load('ml/saved_models/aero_model.pkl')
        scaler_X = joblib.load('ml/saved_models/scaler_X.pkl')
        scaler_y = joblib.load('ml/saved_models/scaler_y.pkl')
        print("✅ Modelos de IA cargados exitosamente en la memoria del servidor.")
    except Exception as e:
        print(f"❌ Error al cargar los modelos: {e}")

# 4. Crear el Endpoint (La "URL" de cálculo)
@app.post("/predict/")
def predict_aerodynamics(request: AeroRequest):
    if model is None:
        raise HTTPException(status_code=500, detail="El modelo de IA no está disponible.")
    
    # Validar límites físicos
    if not (-20.0 <= request.angle_of_attack <= 20.0):
        raise HTTPException(status_code=400, detail="El ángulo de ataque debe estar entre -20 y 20 grados.")
    if not (0.0 < request.velocity <= 100.0):
        raise HTTPException(status_code=400, detail="La velocidad debe estar entre 0 y 100 m/s.")

    # Procesar la predicción
    X_input = np.array([[request.angle_of_attack, request.velocity]])
    X_scaled = scaler_X.transform(X_input)
    y_pred_scaled = model.predict(X_scaled)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)
    
    cl, cd = y_pred[0]
    
    # Cálculos físicos extra
    rho = 1.225
    area = 0.1
    lift_n = 0.5 * rho * (request.velocity**2) * area * cl
    drag_n = 0.5 * rho * (request.velocity**2) * area * cd
    efficiency = cl / cd if cd != 0 else 0

    # Retornar la respuesta estructurada en JSON
    return {
        "status": "success",
        "input": {
            "angle_of_attack_deg": request.angle_of_attack,
            "velocity_ms": request.velocity
        },
        "coefficients": {
            "C_L": round(float(cl), 4),
            "C_D": round(float(cd), 4)
        },
        "forces_newtons": {
            "lift_force": round(float(lift_n), 2),
            "drag_force": round(float(drag_n), 2)
        },
        "performance": {
            "aerodynamic_efficiency_LD": round(float(efficiency), 2)
        }
    }

# 5. Endpoint de prueba de salud
@app.get("/")
def health_check():
    return {"status": "online", "message": "API de Aerodinámica Híbrida operando correctamente."}