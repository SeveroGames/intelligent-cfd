from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
import joblib
import numpy as np
import os
from dotenv import load_dotenv

# 1. Cargar secretos de forma segura desde el archivo .env o el entorno
load_dotenv()
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    print("⚠️ ADVERTENCIA: No se encontró API_KEY. Usando modo inseguro por defecto temporalmente.")

# Definir la cabecera HTTP requerida
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(status_code=403, detail="Acceso denegado. Credenciales M2M inválidas.")

app = FastAPI(
    title="Intelligent CFD API (Secure)",
    description="Motor predictivo de aerodinámica protegido con Autenticación M2M.",
    version="1.1.0"
)

class AeroRequest(BaseModel):
    angle_of_attack: float
    velocity: float

model = None
scaler_X = None
scaler_y = None

@app.on_event("startup")
def load_ai_models():
    global model, scaler_X, scaler_y
    try:
        model = joblib.load('ml/saved_models/aero_model.pkl')
        scaler_X = joblib.load('ml/saved_models/scaler_X.pkl')
        scaler_y = joblib.load('ml/saved_models/scaler_y.pkl')
        print("✅ Modelos de IA cargados exitosamente.")
    except Exception as e:
        print(f"❌ Error al cargar los modelos: {e}")

# 2. Proteger el Endpoint inyectando la dependencia de seguridad
@app.post("/predict/")
def predict_aerodynamics(request: AeroRequest, api_key: str = Depends(get_api_key)):
    if model is None:
        raise HTTPException(status_code=500, detail="El modelo de IA no está disponible.")
    
    if not (-20.0 <= request.angle_of_attack <= 20.0):
        raise HTTPException(status_code=400, detail="El ángulo de ataque debe estar entre -20 y 20 grados.")
    if not (0.0 < request.velocity <= 100.0):
        raise HTTPException(status_code=400, detail="La velocidad debe estar entre 0 y 100 m/s.")

    X_input = np.array([[request.angle_of_attack, request.velocity]])
    X_scaled = scaler_X.transform(X_input)
    y_pred_scaled = model.predict(X_scaled)
    y_pred = scaler_y.inverse_transform(y_pred_scaled)
    
    cl, cd = y_pred[0]
    
    rho = 1.225
    area = 0.1
    lift_n = 0.5 * rho * (request.velocity**2) * area * cl
    drag_n = 0.5 * rho * (request.velocity**2) * area * cd
    efficiency = cl / cd if cd != 0 else 0

    return {
        "status": "success",
        "forces_newtons": {"lift_force": round(float(lift_n), 2), "drag_force": round(float(drag_n), 2)},
        "coefficients": {"C_L": round(float(cl), 4), "C_D": round(float(cd), 4)},
        "performance": {"aerodynamic_efficiency_LD": round(float(efficiency), 2)}
    }

@app.get("/")
def health_check():
    return {"status": "online", "message": "API Segura operando correctamente."}