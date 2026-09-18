"""
Independencia de Malla

Si la física cambia al cambiar la resolución numérica, tu simulación no es válida. Vamos a extraer el perfil de velocidad central en 
3 mallas distintas para demostrar que tienden a una única solución.

"""

import numpy as np
import matplotlib.pyplot as plt
from solver.mesh import create_mesh
from solver.pressure import build_poisson_source, pressure_poisson
from solver.velocity import calculate_velocity

def run_mesh(nx, ny):
    lx, ly, rho, nu, u_top = 1.0, 1.0, 1.0, 0.01, 1.0
    dt = 0.001
    nt = 1000
    
    X, Y, dx, dy, u, v, p, b = create_mesh(nx, ny, lx, ly)
    for _ in range(nt):
        b = build_poisson_source(b, rho, dt, u, v, dx, dy)
        p = pressure_poisson(p, dx, dy, b, 40)
        u, v = calculate_velocity(u, v, p, dx, dy, dt, rho, nu, u_top)
        
    # Extraer el perfil vertical de u en el centro exacto del dominio (x = 0.5)
    centro_x_idx = int(nx / 2)
    return Y[:, centro_x_idx], u[:, centro_x_idx]

def check_mesh_independence():
    mallas = [21, 31, 41]
    resultados = {}
    
    print("Ejecutando simulaciones para independencia de malla. Esto tomará unos segundos...")
    for m in mallas:
        print(f"Resolviendo malla {m}x{m}...")
        y, u_center = run_mesh(m, m)
        resultados[m] = (y, u_center)
        
    plt.figure(figsize=(8, 6))
    colores = ['#FF9999', '#FF4444', '#990000']
    for idx, m in enumerate(mallas):
        y, u_center = resultados[m]
        plt.plot(u_center, y, label=f'Malla {m}x{m}', color=colores[idx], marker='.')
        
    plt.title('Independencia de Malla: Perfil de Velocidad U en X=0.5')
    plt.xlabel('Velocidad U (m/s)')
    plt.ylabel('Posición Y (m)')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    check_mesh_independence()