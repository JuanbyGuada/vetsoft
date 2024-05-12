# Usamos la imagen de python 3.12.3-slim porque esta es liviana; con una version en especifico para evitar problemas de compatibilidad
FROM python:3.12.3-slim

# Establecemos el directorio de trabajo en /app
WORKDIR /app

# Copiamos primero solo el archivo requirements.txt para aprovechar el cache de docker
COPY requirements.txt .

#Instalamos las dependencias del proyecto
RUN pip install --no-cache-dir -r requirements.txt

#Copiamos el resto de la app al contenedor (/app)
COPY . .

# Expone el puerto en el que se ejecutará la aplicación
EXPOSE 8000

#Definimos el comando para ejecutar la aplicación
CMD [ "python", "manage.py","runserver", "0.0.0.0:8000"]