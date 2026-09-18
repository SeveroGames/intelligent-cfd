import numpy as np
from .boundary_conditions import apply_pressure_bcs

def build_poisson_source(b, rho, dt, u, v, dx, dy):
    """Calcula el término fuente (b) basado en la divergencia de la velocidad."""
    b[1:-1, 1:-1] = (rho * (1 / dt * 
                    ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx) + 
                     (v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy))) -
                     ((u[1:-1, 2:] - u[1:-1, 0:-2]) / (2 * dx))**2 -
                     2 * ((u[2:, 1:-1] - u[0:-2, 1:-1]) / (2 * dy) * 
                          (v[1:-1, 2:] - v[1:-1, 0:-2]) / (2 * dx)) -
                     ((v[2:, 1:-1] - v[0:-2, 1:-1]) / (2 * dy))**2)
    return b

def pressure_poisson(p, dx, dy, b, nit):
    """Resuelve la ecuación de Poisson para la presión iterativamente."""
    pn = np.empty_like(p)
    
    for q in range(nit):
        pn = p.copy()
        p[1:-1, 1:-1] = (((pn[1:-1, 2:] + pn[1:-1, 0:-2]) * dy**2 + 
                          (pn[2:, 1:-1] + pn[0:-2, 1:-1]) * dx**2) /
                         (2 * (dx**2 + dy**2)) -
                         dx**2 * dy**2 / (2 * (dx**2 + dy**2)) * 
                         b[1:-1, 1:-1])
        
        p = apply_pressure_bcs(p)
        
    return p