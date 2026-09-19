# 🚀 Intelligent CFD: Motor Predictivo Híbrido (OpenFOAM + Machine Learning)

Este repositorio documenta el desarrollo de una arquitectura de ingeniería de software avanzada que fusiona la **Dinámica de Fluidos Computacional (CFD)** pura con **Inteligencia Artificial (Surrogate Modeling)**. El objetivo es predecir las fuerzas aerodinámicas (Sustentación y Arrastre) de un perfil alar en tiempo real, reduciendo el tiempo de cálculo de minutos en un clúster a milisegundos en un entorno web, manteniendo una precisión matemática de grado industrial.

---

## 📖 Resumen del Proyecto

Tradicionalmente, simular la física de fluidos requiere resolver iterativamente las ecuaciones de Navier-Stokes (un proceso computacionalmente muy costoso). Este proyecto resuelve este cuello de botella mediante una metodología de **Modelo Sustituto (Surrogate Model)**:
1. Se utiliza **OpenFOAM** (vía Docker en Ubuntu) para calcular la física real y generar "Ground Truth" (datos reales).
2. Se entrena una **Red Neuronal (MLP)** en Windows que "aprende" esta física subyacente.
3. Se despliega un **Dashboard Interactivo en la Nube** que permite a cualquier ingeniero evaluar configuraciones de vuelo al instante.

---

## 🏗️ Fases de Desarrollo y Metodología

El proyecto se desarrolló en 10 fases iterativas, abarcando dos sistemas operativos (Ubuntu/Windows) para maximizar la eficiencia de las herramientas nativas:

### Etapa 1: Fundamentos CFD y Entorno Aislado (Linux/Ubuntu)
*   **Fases 0-4:** Programación desde cero de un solver 2D basado en Diferencias Finitas (FDM) para validar los fundamentos matemáticos de las ecuaciones de Navier-Stokes.
*   **Fases 5-6 (Lid-Driven Cavity):** Configuración del entorno profesional. Uso de **Gmsh (v2.2)** para mallas estructuradas y **Docker** (`openfoam/openfoam10-paraview510`) para esquivar limitaciones de hardware y librerías, resolviendo flujo laminar con `icoFoam`.
*   **Fase 7 (NACA 0012 Aerodinámica):** Transición a régimen turbulento y estado estacionario utilizando `simpleFoam`. Se construyó un "túnel de viento" virtual, aplicando condiciones de frontera complejas (symmetry, freestream) y extrayendo coeficientes aerodinámicos ($C_L$ y $C_D$) a través de funciones integradas (`forceCoeffs`/`aerodynamicForces`).

### Etapa 2: Machine Learning y Modelado Sustituto (Windows)
*   **Fase 8:** Generación de un dataset sintético físico masivo (2,000 muestras) basado en las leyes de aerodinámica validadas en CFD (incorporando variables de pérdida/stall). Entrenamiento de un **Perceptrón Multicapa (MLPRegressor)** utilizando Scikit-Learn.
    *   *Innovación:* Se implementó una **Estandarización Bidireccional** (`StandardScaler` en entradas $X$ y salidas $y$) junto con funciones de activación `tanh` para resolver la disparidad de magnitudes entre el Lift y el Drag.
    *   *Resultado:* Una precisión predictiva ($R^2$ Score) del **98.12%** con un MSE cercano a cero.

### Etapa 3: Interfaz Gráfica y Despliegue Web (Cloud)
*   **Fases 9-10:** Desarrollo de un Dashboard de grado industrial usando **Streamlit** y **Plotly**. El motor traduce los coeficientes adimensionales a fuerzas físicas reales (Newtons) basándose en la densidad del aire, velocidad de flujo y área, calculando dinámicamente la eficiencia ($L/D$) y mostrando el espectro de rendimiento en curvas interactivas.

---

## 🛠️ Tecnologías y Stack

**CFD & Simulación:**
*   **OpenFOAM 10:** Framework principal de simulación de fluidos.
*   **Gmsh:** Generación de mallas paramétricas (`.geo` a `.msh`).
*   **Docker:** Contenerización del entorno CFD para ejecución agnóstica.
*   **ParaView:** Visualización de campos vectoriales y presiones.

**Machine Learning & Data Science:**
*   **Python 3:** Lenguaje core.
*   **Scikit-Learn:** Algoritmos de redes neuronales (MLP) y preprocesamiento numérico.
*   **Pandas & NumPy:** Manipulación de tensores y datasets vectorizados.
*   **Joblib:** Congelación y exportación de modelos entrenados (`.pkl`).

**Desarrollo Web & UI:**
*   **Streamlit:** Framework de renderizado web.
*   **Plotly:** Gráficos matemáticos interactivos y reactivos.

---

## 📂 Estructura del Repositorio

```text
intelligent-cfd/
│
├── analysis/                 # Scripts Python de extracción y ploteo de convergencia (CFD)
├── data/                     # Datasets físicos generados (.csv)
├── geometry/                 # Scripts de malla de Gmsh (.geo, .msh)
├── ml/
│   ├── saved_models/         # Modelos de Red Neuronal y Scalers exportados (.pkl)
│   ├── app.py                # Dashboard web principal (Streamlit)
│   ├── generate_dataset.py   # Script puente: Generador de física sintética
│   ├── predictor.py          # Interfaz de IA por línea de comandos (CLI)
│   └── train_model.py        # Arquitectura y entrenamiento de la IA
├── simulations/              # Casos configurados de OpenFOAM (0/, constant/, system/)
│   ├── cavity/               # Caso validación inicial (icoFoam)
│   └── naca0012/             # Caso principal turbulento (simpleFoam)
├── README.md                 # Documentación del proyecto
└── requirements.txt          # Dependencias para despliegue en la nube



🚀 Uso del Dashboard Web (Live Demo)
El modelo predictivo está publicado y accesible para cualquier navegador web. Puedes interactuar con el túnel de viento virtual aquí:

🔗 [Inserta aquí tu enlace de Streamlit Cloud, ej: https://intelligent-cfd-naca0012.streamlit.app]

💻 Instalación y Ejecución Local
Si deseas correr la Inteligencia Artificial y el Dashboard en tu máquina local:

Clonar el repositorio:

git clone [https://github.com/TU_USUARIO/intelligent-cfd.git](https://github.com/TU_USUARIO/intelligent-cfd.git)
cd intelligent-cfd