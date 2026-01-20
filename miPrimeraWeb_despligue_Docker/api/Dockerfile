FROM python:3.9

WORKDIR /app

# 1. Copiamos requirements
COPY web/requirements.txt .
RUN pip install -r requirements.txt

# 2. Copiamos el código
COPY web/ .

# 3. --- NUEVO: CREAR CARPETA Y DAR PERMISOS ---
# Creamos la estructura de carpetas por si no existe
RUN mkdir -p /app/static/archivos
# Le damos permisos totales (777) para que Apache pueda leer lo que Python escribe
RUN chmod -R 777 /app/static

# 4. Arrancamos
CMD ["python", "app.py"]