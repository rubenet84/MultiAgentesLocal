# 1. Usamos una imagen de Python oficial y ligera
FROM python:3.11-slim

# 2. Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# 3. Copiamos el archivo de requisitos primero (para aprovechar la caché)
COPY requirements.txt .

# 4. Instalamos las librerías
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copiamos todo el código de nuestro proyecto
COPY . .

# 6. Exponemos el puerto que usa Streamlit
EXPOSE 8501

# 7. Comando para lanzar la app al iniciar el contenedor
CMD ["streamlit", "run", "interfaz_agentes.py", "--server.port=8501", "--server.address=0.0.0.0"]