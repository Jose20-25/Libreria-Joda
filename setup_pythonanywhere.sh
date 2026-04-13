#!/bin/bash
# Script de instalación para PythonAnywhere
# Ejecuta este script en la consola Bash de PythonAnywhere

set -e

PROJECT_DIR="$HOME/libreria-joda"
VENV_DIR="$HOME/.virtualenvs/libreria-joda"
GITHUB_REPO="https://github.com/Jose20-25/Libreria-Joda.git"

echo "=== Instalando Librería Joda en PythonAnywhere ==="

# 1. Clonar o actualizar el repositorio
if [ -d "$PROJECT_DIR" ]; then
    echo "Actualizando repositorio..."
    cd "$PROJECT_DIR" && git pull
else
    echo "Clonando repositorio..."
    git clone "$GITHUB_REPO" "$PROJECT_DIR"
fi

cd "$PROJECT_DIR"

# 2. Crear entorno virtual Python 3.12
if [ ! -d "$VENV_DIR" ]; then
    echo "Creando entorno virtual..."
    python3.12 -m venv "$VENV_DIR"
fi

# 3. Instalar dependencias
echo "Instalando dependencias..."
"$VENV_DIR/bin/pip" install --upgrade pip
"$VENV_DIR/bin/pip" install -r requirements.txt

# 4. Aplicar migraciones
echo "Aplicando migraciones..."
"$VENV_DIR/bin/python" manage.py migrate --no-input

# 5. Recopilar archivos estáticos
echo "Recopilando archivos estáticos..."
"$VENV_DIR/bin/python" manage.py collectstatic --no-input

echo ""
echo "=== Instalación completada ==="
echo ""
echo "Recuerda configurar en el panel de PythonAnywhere:"
echo "  - Source code: $PROJECT_DIR"
echo "  - Virtualenv: $VENV_DIR"
echo "  - WSGI file: contenido de pythonanywhere_wsgi.py"
echo ""
echo "Variables de entorno (.env) necesarias:"
echo "  SECRET_KEY=<clave-secreta>"
echo "  DEBUG=False"
echo "  PYTHONANYWHERE_HOST=joselito1988.pythonanywhere.com"
echo "  FIREBASE_STORAGE_BUCKET=tiendajoda-c73c4.firebasestorage.app"
echo "  FIREBASE_SERVICE_ACCOUNT_JSON=<contenido-json>"
