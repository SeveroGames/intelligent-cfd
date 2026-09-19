import joblib
import numpy as np
import os
import warnings

# Ignorar advertencias de formato para una interfaz limpia
warnings.filterwarnings('ignore')

def interactive_predictor():
    model_path = 'ml/saved_models/aero_model.pkl'
    if not os.path.exists(model_path):
        print("Error: No se encontraron los modelos guardados.")
        return
    
    # 1. Despertar a la IA (Cargar modelo y escaladores)
    model = joblib.load(model_path)
    scaler_X = joblib.load('ml/saved_models/scaler_X.pkl')
    scaler_y = joblib.load('ml/saved_models/scaler_y.pkl')
    
    print("\n" + "="*50)
    print("   MOTOR PREDICTIVO CFD (NACA 0012) - ALIMENTADO POR IA")
    print("="*50)
    print("Escribe 'salir' en cualquier momento para terminar.\n")
    
    while True:
        try:
            # 2. Recibir parámetros físicos del usuario
            aoa_input = input("Ángulo de Ataque (grados) [-15 a 15]: ")
            if aoa_input.lower() == 'salir': break
            
            vel_input = input("Velocidad del viento (m/s) [10 a 50]: ")
            if vel_input.lower() == 'salir': break
            
            aoa = float(aoa_input)
            vel = float(vel_input)
            
            # 3. Empaquetar y estandarizar la entrada
            X_input = np.array([[aoa, vel]])
            X_scaled = scaler_X.transform(X_input)
            
            # 4. Predicción en milisegundos
            y_pred_scaled = model.predict(X_scaled)
            
            # 5. Revertir estandarización a unidades reales
            y_pred = scaler_y.inverse_transform(y_pred_scaled)
            cl, cd = y_pred[0]
            
            # 6. Mostrar resultados
            print(f"\n>>> RESULTADOS INSTANTÁNEOS <<<")
            print(f"Sustentación (C_L): {cl:.4f}")
            print(f"Arrastre (C_D):     {cd:.4f}\n")
            print("-" * 50 + "\n")
            
        except ValueError:
            print("\n[!] Por favor, ingresa un número válido.\n")

if __name__ == "__main__":
    interactive_predictor()