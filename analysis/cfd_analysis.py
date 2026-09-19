import pandas as pd
import matplotlib.pyplot as plt
import os

def analyze_openfoam_data():
    file_path = 'data/cavity_data.csv'
    if not os.path.exists(file_path):
        print(f"Error: No se encontró {file_path}. Asegúrate de exportarlo desde ParaView.")
        return

    # Leer CSV exportado por ParaView
    df = pd.read_csv(file_path)
    
    # Extraer las columnas de posición en Y y componente X de la velocidad
    y_pos = df['Points:1']
    u_vel = df['U:0']

    print("--- Análisis CFD (OpenFOAM vía Docker) ---")
    print(f"Velocidad máxima (U): {u_vel.max():.4f} m/s")
    print(f"Velocidad mínima (U): {u_vel.min():.4f} m/s")

    # Generar la gráfica científica
    plt.figure(figsize=(8, 6))
    plt.plot(u_vel, y_pos, 'k-', linewidth=2, label='OpenFOAM (Gmsh 41x41)')
    plt.title('Perfil de Velocidad Central (Y vs U) - CFD Profesional')
    plt.xlabel('Velocidad U (m/s)')
    plt.ylabel('Posición Y (m)')
    plt.grid(True)
    plt.legend()
    
    # Guardar y mostrar
    plt.savefig('analysis/openfoam_profile.png')
    plt.show()

if __name__ == "__main__":
    analyze_openfoam_data()