"""
Comparación de Benchmark (Ghia 1982)

La validación de oro para la Lid-Driven Cavity es el paper de U. Ghia et al. (1982). Comparamos nuestra velocidad $u$ a $Re=100$ 
contra los datos experimentales/numéricos publicados por ellos.

"""

import numpy as np
import matplotlib.pyplot as plt
from solver.mesh import create_mesh
from solver.pressure import build_poisson_source, pressure_poisson
from solver.velocity import calculate_velocity

def validate_against_ghia():
    nx, ny = 41, 41
    lx, ly = 1.0, 1.0
    rho, nu, u_top = 1.0, 0.01, 1.0 # Re=100
    dt, nt = 0.001, 1200
    
    # Datos extraídos de Ghia et al. (1982) para Re=100
    ghia_y = np.array([1.0, 0.9766, 0.9688, 0.9609, 0.9531, 0.8516, 0.7344, 0.6172, 0.5000, 0.4531, 0.2813, 0.1719, 0.1016, 0.0703, 0.0625, 0.0547, 0.0000])
    ghia_u = np.array([1.0, 0.8412, 0.7887, 0.7372, 0.6872, 0.2315, 0.0033, -0.1364, -0.2058, -0.2109, -0.1566, -0.1015, -0.0643, -0.0478, -0.0419, -0.0372, 0.0000])
    
    print("Generando solución CFD para comparar con el Benchmark...")
    X, Y, dx, dy, u, v, p, b = create_mesh(nx, ny, lx, ly)
    for _ in range(nt):
        b = build_poisson_source(b, rho, dt, u, v, dx, dy)
        p = pressure_poisson(p, dx, dy, b, 50)
        u, v = calculate_velocity(u, v, p, dx, dy, dt, rho, nu, u_top)
        
    centro_x_idx = int(nx / 2)
    nuestra_u = u[:, centro_x_idx]
    nuestra_y = Y[:, centro_x_idx]
    
    # Calcular MAE Interpolando nuestra solución en los puntos de Ghia
    u_interpolada = np.interp(ghia_y, nuestra_y, nuestra_u)
    mae = np.mean(np.abs(u_interpolada - ghia_u))
    print(f"Error Medio Absoluto (MAE) contra Ghia (1982): {mae:.4f}")
    
    plt.figure(figsize=(8, 6))
    plt.plot(nuestra_u, nuestra_y, 'b-', label=f'Nuestro CFD ({nx}x{ny})')
    plt.plot(ghia_u, ghia_y, 'ro', label='Ghia et al. (1982)', fillstyle='none', markersize=8)
    
    plt.title('Validación de Benchmark: Re=100 (CFD vs Ghia)')
    plt.xlabel('Velocidad U en el centro (x=0.5)')
    plt.ylabel('Posición vertical Y')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    validate_against_ghia()