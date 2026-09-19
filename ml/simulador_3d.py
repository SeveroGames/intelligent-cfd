from ursina import *
import requests
import math
import random
import threading
import time

# Variables globales para conectar la IA con los Gráficos 3D
api_data = {"lift": 0.0, "drag": 0.0, "warning": "INICIANDO ENLACE..."}
current_aoa = 5.0
current_vel = 35.0

# 1. HILO EN SEGUNDO PLANO: Se comunica con la API sin congelar el juego
def fetch_api():
    global api_data
    url = "http://127.0.0.1:8000/predict/"
    while True:
        try:
            payload = {"angle_of_attack": round(current_aoa, 2), "velocity": round(current_vel, 2)}
            res = requests.post(url, json=payload, timeout=1)
            
            if res.status_code == 200:
                data = res.json()
                lift = data["forces_newtons"]["lift_force"]
                drag = data["forces_newtons"]["drag_force"]
                
                if current_aoa > 12.0:
                    warning = "<red>⚠️ STALL DETECTADO<default>"
                elif lift < 0:
                    warning = "<orange>📉 CAÍDA LIBRE<default>"
                else:
                    warning = "<green>✅ VUELO ESTABLE<default>"
                    
                api_data = {"lift": lift, "drag": drag, "warning": warning}
        except:
            api_data["warning"] = "<red>❌ ERROR DE API<default>"
            
        time.sleep(0.1) # Actualiza datos 10 veces por segundo

# Iniciar la conexión con la API en paralelo
threading.Thread(target=fetch_api, daemon=True).start()

# 2. CONFIGURACIÓN DEL MOTOR 3D
app = Ursina()
window.title = 'UAV 3D Telemetry - Digital Twin'
window.borderless = False
window.color = color.rgb(15, 20, 30) # Fondo oscuro de radar

# Crear el "Avión" (Un modelo 3D básico)
airplane = Entity(
    model='cube', 
    color=color.azure, 
    scale=(3, 0.1, 1.5), # Forma de Ala
    texture='white_cube'
)

# Textos del HUD en la pantalla
hud = Text(text='', position=(-0.85, 0.45), scale=1.3, color=color.white)
Text(text='[Click Derecho] Mover Cámara | [Scroll] Zoom', position=(-0.85, -0.45), color=color.gray)

# 3. BUCLE DEL JUEGO (Se ejecuta 60 veces por segundo)
t = 0
def update():
    global t, current_aoa, current_vel
    t += time.dt
    
    # Simular ráfagas de viento y movimiento de nariz
    current_aoa = 5.0 + (math.sin(t) * 10.0) + random.uniform(-0.5, 0.5)
    current_vel = 35.0 + random.uniform(-1, 1)
    
    # Rotar el modelo 3D físicamente (Pitch)
    airplane.rotation_x = -current_aoa 
    
    # Cambiar el color del avión si entra en Stall
    airplane.color = color.red if current_aoa > 12.0 else color.azure
    
    # Actualizar la interfaz del jugador
    hud.text = f"""
    <b>HUD TELEMETRÍA 3D</b>
    --------------------------
    Ángulo (AoA): {current_aoa:.1f}°
    Velocidad   : {current_vel:.1f} m/s
    
    <b>MÉTRICAS IA (FastAPI)</b>
    Lift : {api_data['lift']:.1f} N
    Drag : {api_data['drag']:.1f} N
    
    <b>ESTADO:</b> {api_data['warning']}
    """

# Permite orbitar la cámara con el ratón como en un software CAD
EditorCamera() 

# Arrancar el mundo 3D
app.run()