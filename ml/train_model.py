import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import os

def train_surrogate_model():
    file_path = 'data/aero_dataset.csv'
    if not os.path.exists(file_path):
        print("Error: Dataset no encontrado.")
        return

    df = pd.read_csv(file_path)
    
    # 1. Separar variables
    X = df[['AoA_deg', 'Velocity_ms']]
    y = df[['Cl', 'Cd']]
    
    # 2. Dividir datos (80% / 20%)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Estandarizar entradas (X)
    scaler_X = StandardScaler()
    X_train_scaled = scaler_X.fit_transform(X_train)
    X_test_scaled = scaler_X.transform(X_test)
    
    # 4. Estandarizar salidas (y) - ESTA ES LA CLAVE PARA Cd
    scaler_y = StandardScaler()
    y_train_scaled = scaler_y.fit_transform(y_train)
    
    print("Entrenando Red Neuronal Avanzada (Estandarización Bidireccional + Tanh)...")
    
    # 5. Red más ancha con activación 'tanh' (excelente para curvas suaves de fluidos)
    model = MLPRegressor(
        hidden_layer_sizes=(128, 128, 64), 
        activation='tanh', 
        max_iter=2000, 
        random_state=42
    )
    
    # Entrenar el modelo de IA con todo en la misma escala matemática
    model.fit(X_train_scaled, y_train_scaled)
    
    # 6. Predecir y revertir la escala para comparar con la realidad
    y_pred_scaled = model.predict(X_test_scaled)
    y_pred = scaler_y.inverse_transform(y_pred_scaled) # Devolver a unidades originales
    
    # 7. Evaluación
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\n--- Rendimiento Final del Modelo IA ---")
    print(f"Error Cuadrático Medio (MSE): {mse:.6f}")
    print(f"Precisión (R2 Score): {r2:.4f} (1.0 es predicción perfecta)")
    
    # 8. Graficar validación
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.scatter(y_test['Cl'], y_pred[:, 0], alpha=0.5, color='blue')
    plt.plot([-1.5, 1.5], [-1.5, 1.5], 'k--', lw=2)
    plt.title('IA vs OpenFOAM: Lift (Cl)')
    plt.xlabel('CFD Original (Cl)')
    plt.ylabel('Predicción de IA (Cl)')
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    plt.scatter(y_test['Cd'], y_pred[:, 1], alpha=0.5, color='red')
    plt.plot([0, 0.2], [0, 0.2], 'k--', lw=2)
    plt.title('IA vs OpenFOAM: Drag (Cd)')
    plt.xlabel('CFD Original (Cd)')
    plt.ylabel('Predicción de IA (Cd)')
    plt.grid(True)
    
    # Guardar el modelo y los escaladores para uso futuro
    os.makedirs('ml/saved_models', exist_ok=True)
    joblib.dump(model, 'ml/saved_models/aero_model.pkl')
    joblib.dump(scaler_X, 'ml/saved_models/scaler_X.pkl')
    joblib.dump(scaler_y, 'ml/saved_models/scaler_y.pkl')
    print("Modelo IA y escaladores guardados exitosamente en ml/saved_models/")
    
    os.makedirs('analysis', exist_ok=True)
    plt.savefig('analysis/ml_performance_final.png')
    plt.show()

if __name__ == "__main__":
    train_surrogate_model()