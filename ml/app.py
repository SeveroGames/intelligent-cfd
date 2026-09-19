import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go
import warnings

warnings.filterwarnings('ignore')

# 1. Configuración premium de la página
st.set_page_config(page_title="CFD AI Predictor", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

# 2. Inyección de CSS para un diseño más limpio y moderno
st.markdown("""
    <style>
    .main {background-color: #f8f9fa;}
    div[data-testid="metric-container"] {
        background-color: white; 
        padding: 15px; 
        border-radius: 10px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        border-left: 5px solid #0052cc;
    }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_ai_engine():
    model = joblib.load('ml/saved_models/aero_model.pkl')
    scaler_X = joblib.load('ml/saved_models/scaler_X.pkl')
    scaler_y = joblib.load('ml/saved_models/scaler_y.pkl')
    return model, scaler_X, scaler_y

try:
    model, scaler_X, scaler_y = load_ai_engine()
except FileNotFoundError:
    st.error("⚠️ Error: No se encontraron los modelos .pkl.")
    st.stop()

# 3. Encabezado
st.title("🚀 Túnel de Viento Virtual AI | NACA 0012")
st.markdown("**Motor Predictivo Híbrido:** Simulación CFD (OpenFOAM) $\\rightarrow$ IA (Redes Neuronales)")
st.markdown("---")

# Constantes Físicas
rho = 1.225
area = 0.1

# 4. Sidebar rediseñado con imagen de referencia
with st.sidebar:
    st.header("🎛️ Panel de Control")
    st.markdown("Modifica las variables físicas:")
    
    aoa = st.slider("📐 Ángulo de Ataque (°)", min_value=-15.0, max_value=15.0, value=5.0, step=0.5)
    vel = st.slider("💨 Velocidad del Viento (m/s)", min_value=10.0, max_value=50.0, value=30.0, step=1.0)
    
    st.markdown("---")
    st.info("💡 **Interacción:** Mueve la velocidad y observa en tiempo real cómo las fuerzas escalan exponencialmente. Pasa el ratón por la gráfica para ver los datos exactos.")

# 5. Cálculos para el punto actual
X_input = np.array([[aoa, vel]])
y_pred = scaler_y.inverse_transform(model.predict(scaler_X.transform(X_input)))
cl, cd = y_pred[0]
efficiency = cl / cd if cd != 0 else 0

lift_force = 0.5 * rho * (vel**2) * area * cl
drag_force = 0.5 * rho * (vel**2) * area * cd
presion_dinamica = 0.5 * rho * (vel**2)

# 6. Tarjetas de Métricas Elegantes
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🛫 Sustentación (Lift)", f"{lift_force:.1f} N", f"Coef. CL: {cl:.3f}")
with col2:
    # Se pone delta_color="inverse" porque un mayor arrastre suele ser negativo
    st.metric("🛑 Arrastre (Drag)", f"{drag_force:.1f} N", f"Coef. CD: {cd:.3f}", delta_color="inverse")
with col3:
    st.metric("⚡ Eficiencia (L/D)", f"{efficiency:.2f}")
with col4:
    st.metric("🌪️ Presión Dinámica", f"{presion_dinamica:.1f} Pa")

st.markdown("<br>", unsafe_allow_html=True)

# 7. Sweep completo para la Gráfica
aoa_range = np.linspace(-15, 15, 100)
X_sweep = np.column_stack((aoa_range, np.full_like(aoa_range, vel)))
y_sweep = scaler_y.inverse_transform(model.predict(scaler_X.transform(X_sweep)))

lift_curve = 0.5 * rho * (vel**2) * area * y_sweep[:, 0]
drag_curve = 0.5 * rho * (vel**2) * area * y_sweep[:, 1]

# 8. Gráfico Interactivo de Alta Fidelidad (Plotly)
fig = go.Figure()

# Curva Suave de Sustentación
fig.add_trace(go.Scatter(x=aoa_range, y=lift_curve, mode='lines', name='Lift (Sustentación)', 
                         line=dict(color='#0052cc', width=4), hovertemplate='Fuerza: %{y:.1f} N'))
# Curva Suave de Arrastre
fig.add_trace(go.Scatter(x=aoa_range, y=drag_curve, mode='lines', name='Drag (Arrastre)', 
                         line=dict(color='#e11d48', width=4), hovertemplate='Fuerza: %{y:.1f} N'))

# Estrellas Brillantes para el punto exacto donde te encuentras
fig.add_trace(go.Scatter(x=[aoa], y=[lift_force], mode='markers', name='Punto de Vuelo (Lift)',
                         marker=dict(color='#0052cc', size=14, symbol='star', line=dict(color='white', width=2))))
fig.add_trace(go.Scatter(x=[aoa], y=[drag_force], mode='markers', name='Punto de Vuelo (Drag)',
                         marker=dict(color='#e11d48', size=14, symbol='star', line=dict(color='white', width=2))))

# Línea punteada dinámica vertical
fig.add_vline(x=aoa, line_width=2, line_dash="dash", line_color="gray")

# Estilización general de la gráfica web
fig.update_layout(
    title=dict(text=f"Espectro Físico a {vel} m/s", font=dict(size=20)),
    xaxis_title="Ángulo de Ataque (°)",
    yaxis_title="Fuerza Aerodinámica (Newtons)",
    hovermode="x unified", # Muestra Lift y Drag juntos al pasar el ratón
    plot_bgcolor='rgba(255,255,255,1)', # Fondo de la gráfica limpio
    paper_bgcolor='rgba(0,0,0,0)',
    xaxis=dict(showgrid=True, gridcolor='#e5e7eb', zeroline=True, zerolinecolor='black'),
    yaxis=dict(showgrid=True, gridcolor='#e5e7eb', zeroline=True, zerolinecolor='black'),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(255,255,255,0.9)", bordercolor="black", borderwidth=1),
    margin=dict(l=40, r=40, t=60, b=40)
)

st.plotly_chart(fig, width="stretch")