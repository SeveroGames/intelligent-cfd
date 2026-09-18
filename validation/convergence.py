"""
Análisis de Convergencia

Un estado estacionario real se alcanza cuando la diferencia del campo de velocidades entre el paso $n$ y $n+1$ es cercana a cero.
"""

import numpy as np
import matplotlib.pyplot as plt
from solver.mesh import create_mesh
from solver.pressure import build_poisson_source, pressure_poisson
from solver.velocity import calculate_velocity

def check_convergence():
    nx, ny = 41, 41
    lx, ly = 1.0, 1.0
    rho, nu, u_top = 1.0, 0.01, 1.0  # Re = 100
    dt = 0.001
    nt = 1500
    
    X, Y, dx, dy, u, v, p, b = create_mesh(nx, ny, lx, ly)
    
    residuals = []
    tolerancia = 1e-5
    
    print("Calculando convergencia hacia el estado estacionario...")
    for n in range(nt):
        u_old = u.copy()
        
        b = build_poisson_source(b, rho, dt, u, v, dx, dy)
        p = pressure_poisson(p, dx, dy, b, 50)
        u, v = calculate_velocity(u, v, p, dx, dy, dt, rho, nu, u_top)
        
        # Norma L-infinito (máximo cambio absoluto en la velocidad u)
        error = np.max(np.abs(u - u_old))
        residuals.append(error)
        
        if error < tolerancia and n > 100:
            print(f"¡Convergencia alcanzada en el paso {n} con error {error:.2e}!")
            break
            
    plt.figure(figsize=(8, 5))
    plt.semilogy(residuals, color='red', linewidth=2)
    plt.axhline(y=tolerancia, color='blue', linestyle='--', label=f'Tolerancia ({tolerancia})')
    plt.title('Historial de Convergencia (Residuo de Velocidad U)')
    plt.xlabel('Iteración Temporal')
    plt.ylabel('Error Máximo Absoluto (escala log)')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.show()

if __name__ == "__main__":
    check_convergence()