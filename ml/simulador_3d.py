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
                    warning = "<red> STALL DETECTADO (PÉRDIDA)<default>"
                elif lift < 0:
                    warning = "<orange> CAÍDA LIBRE<default>"
                else:
                    warning = "<green> VUELO NOMINAL<default>"
                    
                api_data = {"lift": lift, "drag": drag, "warning": warning}
        except:
            api_data["warning"] = "<red> ERROR DE API<default>"
            
        time.sleep(0.1) # Actualiza datos 10 veces por segundo

# Iniciar la conexión con la API en paralelo
threading.Thread(target=fetch_api, daemon=True).start()

# 2. CONFIGURACIÓN DEL MOTOR 3D
app = Ursina()
window.title = 'UAV 3D Telemetry - Digital Twin'
window.borderless = False
window.color = color.rgb(15, 20, 30) # Fondo oscuro estilo radar militar

# --- CONSTRUCCIÓN DEL AVIÓN 3D ---
# Nodo central (Padre) que agrupa todo
airplane = Entity()

# 1. Fuselaje (Cuerpo principal)
fuselage = Entity(parent=airplane, model='cube', scale=(0.8, 0.8, 5), color=color.rgb(200, 200, 200))

# 2. Alas Principales (Perfil NACA)
wings = Entity(parent=airplane, model='cube', scale=(5.5, 0.1, 1.2), position=(0, 0, 0.5), color=color.azure)

# 3. Estabilizador Horizontal (Cola)
tail_h = Entity(parent=airplane, model='cube', scale=(2.2, 0.1, 0.8), position=(0, 0, -2.2), color=color.azure)

# 4. Estabilizador Vertical (Aleta trasera)
tail_v = Entity(parent=airplane, model='cube', scale=(0.1, 1.2, 0.8), position=(0, 0.6, -2.2), color=color.azure)

# 5. Cabina (Cockpit)
cockpit = Entity(parent=airplane, model='cube', scale=(0.6, 0.4, 1.2), position=(0, 0.5, 1.2), color=color.black66)

# Añadir una cuadrícula en el suelo para referencia de movimiento
grid = Entity(model='wireframe_cube', scale=(50, 0.1, 50), position=(0, -5, 0), color=color.dark_gray)

# Textos del HUD en la pantalla
hud = Text(text='', position=(-0.85, 0.45), scale=1.3, color=color.white)
Text(text='[Click Derecho] Orbitar Cámara | [Scroll] Zoom', position=(-0.85, -0.45), color=color.gray)

# 3. BUCLE DEL JUEGO (Se ejecuta 60 veces por segundo)
t = 0
def update():
    global t, current_aoa, current_vel
    t += time.dt
    
    # Simular ráfagas de viento y movimiento de nariz en el tiempo
    current_aoa = 5.0 + (math.sin(t * 1.5) * 9.0) + random.uniform(-0.5, 0.5)
    current_vel = 35.0 + random.uniform(-1, 1)
    
    # Rotar físicamente el AVIÓN COMPLETO (Eje X = Pitch/Cabeceo)
    airplane.rotation_x = -current_aoa 
    
    # Efecto visual: Las alas y la cola se ponen ROJAS si el avión entra en Stall
    if current_aoa > 12.0:
        wings.color = color.red
        tail_h.color = color.red
        tail_v.color = color.red
    else:
        wings.color = color.azure
        tail_h.color = color.azure
        tail_v.color = color.azure
    
    # Actualizar la interfaz del jugador
    hud.text = f"""
    <b>HUD TELEMETRÍA 3D UAV</b>
    --------------------------
    Ángulo (AoA): {current_aoa:.1f}°
    Velocidad   : {current_vel:.1f} m/s
    
    <b>MÉTRICAS IA (FastAPI)</b>
    Lift (Fuerza): {api_data['lift']:.1f} N
    Drag (Fricción): {api_data['drag']:.1f} N
    
    <b>ESTADO:</b> {api_data['warning']}
    """

# Ajustar cámara para que vea el avión de lado/atrás al iniciar
camera.position = (8, 4, -10)
camera.look_at(airplane)
EditorCamera() # Permite usar el ratón para orbitar

# Arrancar el mundo 3D
app.run()