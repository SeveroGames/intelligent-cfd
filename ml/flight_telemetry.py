import requests
import time
import math
import random
import os
import warnings

warnings.filterwarnings('ignore')

API_URL = "http://127.0.0.1:8000/predict/"

def clear_screen():
    # Limpia la consola para crear el efecto de animación (funciona en Windows y Linux)
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_hud(t, aoa, vel, lift, drag, warning, latency):
    clear_screen()
    print("="*60)
    print(" 🚁 SISTEMA DE TELEMETRÍA UAV - HUD EN TIEMPO REAL")
    print("="*60)
    
    # Arte ASCII dinámico basado en el Ángulo de Ataque
    if aoa > 12.0:
        # Avión muy inclinado (Pérdida/Stall)
        print(r"""
             __!__
            /  _  \     [⚠️ ALERTA: ÁNGULO CRÍTICO]
           /  / \  \    [!!] RIESGO DE PÉRDIDA
          /__/   \__\   
             \   /      
              \ /       
        """)
    elif aoa > 3.0:
        # Avión subiendo
        print(r"""
                .
               / \      [✈️ ASCENSO]
              /   \     Nariz arriba
             /_____\    
               | |      
              /   \     
        """)
    elif aoa < -2.0:
        # Avión bajando
        print(r"""
              \   /     
               | |      [📉 DESCENSO]
             \_____/    Nariz abajo
              \   /     
               \ /      
                '
        """)
    else:
        # Avión estable
        print(r"""
             _______    
            (_______)   [✈️ VUELO ESTABLE]
             \_____/    Crucero
        """)

    print("-" * 60)
    print(f" ⏱️ TIEMPO DE VUELO : T+{t:02d}s")
    print(f" 📐 ÁNGULO (AoA)    : {aoa:>6.2f}°")
    print(f" 💨 VELOCIDAD VIENTO: {vel:>7.2f} m/s")
    print("-" * 60)
    print(f" 🛫 FUERZA LIFT     : {lift:>8.1f} Newtons")
    print(f" 🛑 FUERZA DRAG     : {drag:>8.1f} Newtons")
    print("-" * 60)
    print(f" 📡 LATENCIA API    : {latency:.1f} ms")
    print(f" 🚨 ESTADO SISTEMA  : {warning}")
    print("="*60)

def simulate_flight():
    base_velocity = 35.0  
    
    try:
        requests.get("http://127.0.0.1:8000/")
    except requests.exceptions.ConnectionError:
        print("❌ Error: La API no responde. Asegúrate de que Uvicorn esté corriendo.")
        return

    # Ciclo de Vuelo más largo para disfrutar la animación (40 segundos)
    for t in range(1, 41):
        # Física simulada
        aoa = 5.0 + (math.sin(t / 1.5) * 8.0) + random.uniform(-1, 1)
        vel = base_velocity + random.uniform(-3, 8) 
        
        payload = {"angle_of_attack": round(aoa, 2), "velocity": round(vel, 2)}
        
        start_time = time.time()
        response = requests.post(API_URL, json=payload)
        latency = (time.time() - start_time) * 1000  
        
        if response.status_code == 200:
            data = response.json()
            lift = data["forces_newtons"]["lift_force"]
            drag = data["forces_newtons"]["drag_force"]
            
            if aoa > 12.0:
                warning = "⚠️ STALL DETECTADO"
            elif lift < 0:
                warning = "📉 CAÍDA LIBRE"
            else:
                warning = "✅ SISTEMAS NOMINALES"
            
            # Llamar a la función que dibuja el avión y el tablero
            draw_hud(t, payload['angle_of_attack'], payload['velocity'], lift, drag, warning, latency)
            
        time.sleep(0.5)

    print("\n🏁 Simulación de vuelo completada. Aterrizaje exitoso.\n")

if __name__ == "__main__":
    simulate_flight()