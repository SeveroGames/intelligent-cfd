import matplotlib.pyplot as plt
from .mesh import create_mesh
from .pressure import build_poisson_source, pressure_poisson
from .velocity import calculate_velocity

def run_cavity_simulation():
    # Parámetros físicos (Aire a Re=100 aprox)
    nx, ny = 41, 41
    lx, ly = 2.0, 2.0
    rho = 1.0
    nu = 0.1
    u_top = 1.0 # Velocidad de la tapa
    
    # Parámetros numéricos
    dt = 0.001
    nt = 500  # Número de pasos de tiempo
    nit = 50  # Iteraciones para la presión Poisson
    
    # Inicializar malla
    X, Y, dx, dy, u, v, p, b = create_mesh(nx, ny, lx, ly)
    
    print(f"Iniciando simulación Lid-Driven Cavity (Re ~ {int(u_top*lx/nu)})")
    print(f"Resolución: {nx}x{ny}, Pasos temporales: {nt}")

    # Bucle temporal principal
    for n in range(nt):
        # 1. Calcular término fuente de presión
        b = build_poisson_source(b, rho, dt, u, v, dx, dy)
        # 2. Resolver Poisson para la presión
        p = pressure_poisson(p, dx, dy, b, nit)
        # 3. Calcular nuevas velocidades y aplicar condiciones de frontera
        u, v = calculate_velocity(u, v, p, dx, dy, dt, rho, nu, u_top)
        
        if n % 100 == 0:
            print(f"Paso {n}/{nt} completado...")

    # Visualización científica
    plt.figure(figsize=(11, 7), dpi=100)
    plt.contourf(X, Y, p, alpha=0.5, cmap='viridis')
    plt.colorbar(label='Presión')
    
    # Líneas de corriente (Streamlines)
    plt.streamplot(X, Y, u, v, density=1.5, color='white', linewidth=1, arrowsize=1.2)
    
    plt.title('Lid-Driven Cavity: Campo de Presión y Líneas de Corriente')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xlim(0, lx)
    plt.ylim(0, ly)
    plt.show()

if __name__ == "__main__":
    run_cavity_simulation()