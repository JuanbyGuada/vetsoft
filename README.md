# Integrantes
- **Integrante 1:** Casas Ortiz de Rosas, Juan Bautista
- **Integrante 2:** Tastaca Lugo, Aylen

# Vetsoft

Aplicación web para veterinarias utilizada en la cursada 2024 de Ingeniería y Calidad de Software. UTN-FRLP

## Dependencias

- python 3
- Django
- sqlite
- playwright
- ruff

## Instalar dependencias

`pip install -r requirements.txt`

## Iniciar la Base de Datos

`python manage.py migrate`

## Iniciar app

`python manage.py runserver`

# Casas Ortiz de Rosas: la version actual utilizada es la 2.0

# Tastaca Lugo: la version actual utilizada es la 2.0


# Pasos para construir la imagen Docker y desplegar el contenedor.
- **1. Docker** Descargar e instalar docker desde "docker.com" para el sistema operativo correspondiente
- **2. Crear archivo Dockerfile** En el mismo se detallan las instrucciones para construir la imagen Docker, utiilizando las buenas practicas.
- **3. Crear variables de entorno** Se crea un template llamado 'env-example' para que el usuario pueda modificarlo con las variables sensibles del proyecto (como la secret_key)
- **4. Adaptar archivo settings.py** En vez de que los datos sensibles (como secret_key, DB_NAME, DB_ENGINE) se encuentren en el archivo settings.py, se las intercambia por las variables de entorno declaradas en el archivo key.env.
- **5. Crear imagen Docker** Ejecutar el comando desde la terminal 'docker build -t vetsoft-app:[version] .', el cual busca en el directorio actual el archivo Dockerfile y crea la imagen Docker bajo el nombre y la última versión. (sin corchetes el numero de version)
- **6. Desplegar contenedor** Ejecutar el comando desde la terminal 'docker run -d --env-file key.env -p 8000:8000 vetsoft-app:2.0", el cual le envia como parámetro el archivo con las variables de entorno, y luego causa que se pueda acceder localmente desde un navegador si se indica la direccion del puerto 8000:8000.