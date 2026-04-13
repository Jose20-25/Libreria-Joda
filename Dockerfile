# Imagen base Python slim
FROM python:3.12-slim

# Variables de entorno para Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el proyecto
COPY . .

# Recopilar archivos estáticos
RUN python manage.py collectstatic --no-input

# Puerto — Railway inyecta $PORT automáticamente
EXPOSE 8080

# Script de inicio: migra y arranca
RUN echo '#!/bin/sh\npython manage.py migrate --no-input\nexec gunicorn libreria_joda.wsgi:application --bind 0.0.0.0:${PORT:-8080} --workers 2 --threads 4 --timeout 60 --log-file -' > /app/start.sh \
    && chmod +x /app/start.sh

CMD ["/app/start.sh"]
