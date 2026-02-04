# COMANDOS RAPIDOS - Ejecuta estos comandos despues de reiniciar PowerShell

# 1. Navegar al proyecto
cd "G:\Libreria JODA"

# 2. Verificar Git instalado
git --version

# 3. Configurar usuario Git (solo la primera vez)
git config --global user.name "jose20-25"
git config --global user.email "tu_email@example.com"

# 4. Inicializar repositorio
git init
git branch -M main
git remote add origin https://github.com/jose20-25/Libreria-Joda.git

# 5. Hacer commit
git add .
git commit -m "Deploy: Sistema ERP completo"

# 6. Subir a GitHub (necesitaras tu token de acceso)
git push -u origin main

# 7. Desplegar en Firebase
firebase deploy --only hosting

# CREAR TOKEN DE GITHUB:
# 1. Ve a: https://github.com/settings/tokens
# 2. Generate new token (classic)
# 3. Nombre: Libreria JODA Deploy
# 4. Permisos: repo, workflow
# 5. Generate token
# 6. Copia el token (solo se muestra una vez)

# USAR TOKEN EN GIT:
# Cuando git push pida password, usa el token (no tu contraseña de GitHub)
