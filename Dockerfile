# Usar una imagen oficial de Python ligera y optimizada
FROM python:3.12-slim

# Evitar que Python genere archivos basura (.pyc) y forzar logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear el directorio de trabajo en el servidor virtual
WORKDIR /app

# Copiar primero las dependencias para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar librerías matemáticas y web
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código fuente al contenedor
COPY . .

# Exponer los puertos (8000 para API, 8501 para Web)
EXPOSE 8000 8501