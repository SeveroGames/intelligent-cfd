import numpy as np

def create_mesh(nx, ny, lx, ly):
    """Genera la grilla espacial y los campos inicializados en cero."""
    dx = lx / (nx - 1)
    dy = ly / (ny - 1)
    
    x = np.linspace(0, lx, nx)
    y = np.linspace(0, ly, ny)
    X, Y = np.meshgrid(x, y)
    
    # Variables primitivas (velocidad en X, velocidad en Y, presión)
    u = np.zeros((ny, nx))
    v = np.zeros((ny, nx))
    p = np.zeros((ny, nx))
    
    # Término fuente para la ecuación de Poisson de la presión
    b = np.zeros((ny, nx))
    
    return X, Y, dx, dy, u, v, p, b