import numpy as np
import pandas as pd
import os

def generate_aero_dataset():
    os.makedirs('data', exist_ok=True)
    np.random.seed(42)
    
    # Simular 2000 iteraciones de OpenFOAM con diferentes variables
    n_samples = 2000
    angles_of_attack = np.random.uniform(-15, 15, n_samples)
    velocities = np.random.uniform(10, 50, n_samples)
    
    # Aplicar física aerodinámica validada (NACA 0012)
    alpha_rad = np.radians(angles_of_attack)
    stall_factor = np.cos(alpha_rad)**20  # Simula la pérdida de sustentación
    
    # Coeficientes teóricos con ruido para simular turbulencia del solver
    cl = 2 * np.pi * alpha_rad * stall_factor + np.random.normal(0, 0.02, n_samples)
    cd = 0.015 + 0.05 * (cl**2) + np.random.normal(0, 0.002, n_samples)
    
    # Guardar resultados
    df = pd.DataFrame({
        'AoA_deg': angles_of_attack,
        'Velocity_ms': velocities,
        'Cl': cl,
        'Cd': cd
    })
    
    df.to_csv('data/aero_dataset.csv', index=False)
    print(f"Dataset generado: 2000 perfiles aerodinámicos listos para IA.")

if __name__ == "__main__":
    generate_aero_dataset()