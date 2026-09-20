# 🚀 Intelligent CFD: Motor Predictivo Híbrido y Gemelo Digital 3D

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![OpenFOAM](https://img.shields.io/badge/OpenFOAM-10-black.svg)](https://www.openfoam.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Secure-00a393.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://www.docker.com/)
[![CI/CD](https://img.shields.io/badge/GitHub_Actions-Passing-success.svg)]()

Este repositorio documenta el desarrollo de una **arquitectura de ingeniería de software de grado aeroespacial** que fusiona la Dinámica de Fluidos Computacional (CFD) pura con Inteligencia Artificial (Surrogate Modeling). 

El sistema es capaz de predecir las fuerzas aerodinámicas de un perfil alar en milisegundos, exponer los cálculos mediante una API segura (M2M), y renderizar la física en tiempo real en un **Gemelo Digital 3D** y un **Dashboard Web**.

---

## 📖 Arquitectura del Sistema

El proyecto resuelve el cuello de botella computacional de las ecuaciones de Navier-Stokes transformando horas de simulación en un ecosistema instantáneo y distribuido:
1. **Física Base (Ground Truth):** Generada mediante OpenFOAM en un entorno Docker aislado (Ubuntu).
2. **Cerebro (IA):** Red Neuronal (MLP) entrenada con Scikit-Learn que aproxima el campo físico bidimensional.
3. **Microservicios (Backend/Frontend):** FastAPI y Streamlit orquestados en contenedores nativos para la nube.
4. **Telemetría Interactiva:** Simulador 3D estilo radar (Ursina Engine) que reacciona físicamente a los cálculos de la IA a 60 FPS.

---

## 🏗️ Fases de Desarrollo y Metodología

El ecosistema se construyó en **15 fases iterativas**, dominando un flujo *Cross-Platform* (Desarrollo en Windows $\rightarrow$ Despliegue en servidores Ubuntu Linux):

### Etapa 1: Fundamentos CFD y Entorno Aislado (Linux/Ubuntu)
* **Fases 0-4:** Solvers matemáticos 2D (Diferencias Finitas).
* **Fases 5-7 (Cavity & NACA 0012):** Implementación industrial con **Gmsh** y **OpenFOAM** (esquemas `icoFoam` y `simpleFoam` turbulento). Extracción paramétrica de coeficientes $C_L$ y $C_D$.

### Etapa 2: Machine Learning y Modelado Sustituto (Windows)
* **Fases 8-10:** Generación de un dataset sintético físico. Entrenamiento de un Perceptrón Multicapa (`MLPRegressor`) con estandarización bidireccional y activación `tanh`.
  * *Hito:* Precisión predictiva del **98.12%** y despliegue del modelo en la nube mediante **Streamlit**.

### Etapa 3: Microservicios y Gemelo Digital 3D (API y Simulación)
* **Fases 11-12:** Creación de un backend **FastAPI** ultrarrápido que envuelve el modelo `.pkl`. Desarrollo de un simulador cliente (**Ursina Engine**) con cámara espacial, renderizado de malla aeronáutica y un HUD de telemetría que parpadea ante pérdidas de sustentación (Stall).

### Etapa 4: MLOps, CI/CD y Seguridad Industrial (Cloud/DevOps)
* **Fase 13 (Docker Compose):** Empaquetado de la IA y el frontend en contenedores escalables de Linux (`python:3.10-slim`).
* **Fase 14 (GitHub Actions):** Pipeline de Integración Continua (CI/CD). Un robot ejecuta validaciones con `pytest` en cada actualización para asegurar que la IA nunca rompa las leyes de la física (ej. prohibir el arrastre negativo).
* **Fase 15 (Zero Trust Security):** Autenticación de máquina a máquina (M2M) con `X-API-Key`. Inyección de variables de entorno ocultas (`.env`) para asegurar que el repositorio pueda ser público sin comprometer el servidor.

---

## 🛠️ Tecnologías y Stack

* **Física y Simulación:** OpenFOAM 10, Gmsh, ParaView.
* **Inteligencia Artificial:** Scikit-Learn, Pandas, NumPy, Joblib.
* **Desarrollo Web y API:** FastAPI, Uvicorn, Streamlit, Plotly.
* **Gráficos 3D:** Ursina Engine (Motor de telemetría).
* **MLOps y DevOps:** Docker, Docker Compose, GitHub Actions, Pytest, Python-Dotenv.

---

## 📂 Estructura del Repositorio

```text
intelligent-cfd/
│
├── .github/workflows/       # Pipelines de CI/CD (GitHub Actions)
├── analysis/                # Convergencia y validación matemática
├── geometry/                # Mallas paramétricas (.geo, .msh)
├── ml/                      # Ecosistema de Inteligencia Artificial
│   ├── saved_models/        # Modelos MLP y Scalers (.pkl)
│   ├── api.py               # Servidor Backend Seguro (FastAPI)
│   ├── app.py               # Dashboard Interactivo Web (Streamlit)
│   ├── simulador_3d.py      # Telemetría de vuelo UAV en 3D
│   └── train_model.py       # Algoritmo de entrenamiento
├── simulations/             # Casos de OpenFOAM (cavity, naca0012)
├── tests/                   # Pruebas automatizadas (Físicas y de Seguridad)
├── Dockerfile               # Receta de empaquetado del clúster
├── docker-compose.yml       # Orquestador de microservicios
├── pytest.ini               # Configuración del entorno de testing
├── requirements.txt         # Dependencias globales del servidor
└── README.md                # Documentación



🚀 Uso del Dashboard Web (Live Demo)
El modelo predictivo está publicado y accesible para cualquier navegador web. Puedes interactuar con el túnel de viento virtual aquí:

https://intelligent-cfd-m8ht7kum4w3vzohygfnmro.streamlit.app/

💻 Instalación y Ejecución Local
Si deseas correr la Inteligencia Artificial y el Dashboard en tu máquina local:

1. Clonar el repositorio:

git clone https://github.com/SeveroGames/intelligent-cfd
cd intelligent-cfd


2. Crear y activar el entorno virtual:

En Windows:

python -m venv venv
venv\Scripts\activate

En Linux/Mac:

python3 -m venv venv
source venv/bin/activate


3. Instalar dependencias:

pip install -r requirements.txt

Ejecutar la Interfaz Web:

streamlit run ml/app.py


Autor: Andres Chichande
