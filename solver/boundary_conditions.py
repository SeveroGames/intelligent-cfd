def apply_velocity_bcs(u, v, u_top):
    """Aplica la condición de no-deslizamiento y la tapa móvil."""
    # Paredes izquierda, derecha e inferior (u = 0, v = 0)
    u[:, 0] = 0
    u[:, -1] = 0
    u[0, :] = 0
    
    v[:, 0] = 0
    v[:, -1] = 0
    v[0, :] = 0
    v[-1, :] = 0
    
    # Pared superior (Tapa móvil)
    u[-1, :] = u_top
    
    return u, v

def apply_pressure_bcs(p):
    """Aplica gradiente nulo en paredes para la presión."""
    p[:, -1] = p[:, -2]  # Derecha (dp/dx = 0)
    p[:, 0] = p[:, 1]    # Izquierda (dp/dx = 0)
    p[0, :] = p[1, :]    # Inferior (dp/dy = 0)
    p[-1, :] = 0         # Superior (Presión de referencia p=0)
    
    return p