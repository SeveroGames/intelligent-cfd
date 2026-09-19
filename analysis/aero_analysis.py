import pandas as pd
import matplotlib.pyplot as plt
import os

def analyze_aerodynamics():
    # Ruta actualizada al nombre que usamos en controlDict (aerodynamicForces)
    file_path = 'simulations/naca0012/postProcessing/aerodynamicForces/0/forceCoeffs.dat'
    
    if not os.path.exists(file_path):
        print(f"Error: No se encontró el archivo en {file_path}")
        return

    # Leer archivo ignorando líneas de comentarios iniciales
    df = pd.read_csv(file_path, sep='\t', comment='#', header=None, 
                     names=['Iter', 'Cd', 'Cs', 'Cl', 'CmRoll', 'CmPitch', 'CmYaw', 'Cd(f)', 'Cd(r)', 'Cl(f)', 'Cl(r)'])

    # Graficar convergencia
    plt.figure(figsize=(10, 5))
    plt.plot(df['Iter'], df['Cl'], label='Lift ($C_L$)', color='blue', linewidth=2)
    plt.plot(df['Iter'], df['Cd'], label='Drag ($C_D$)', color='red', linewidth=2)
    
    plt.title('Convergencia Aerodinámica (NACA 0012)')
    plt.xlabel('Iteraciones del Solver')
    plt.ylabel('Coeficiente de Fuerza')
    plt.grid(True)
    plt.legend()
    plt.savefig('analysis/naca0012_forces.png')
    
    print(f"--- Análisis Aerodinámico (Estado Estacionario) ---")
    print(f"Lift Coef final (C_L): {df['Cl'].iloc[-1]:.4f}")
    print(f"Drag Coef final (C_D): {df['Cd'].iloc[-1]:.4f}")
    
    plt.show()

if __name__ == "__main__":
    analyze_aerodynamics()