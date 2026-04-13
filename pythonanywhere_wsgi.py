# WSGI configuration para PythonAnywhere
# Coloca este archivo en: /var/www/josenolasco323_pythonanywhere_com_wsgi.py
# (PythonAnywhere lo configura automáticamente)

import sys
import os

# Ruta al proyecto — ajusta con tu usuario de PythonAnywhere
path = '/home/joselito1988/libreria-joda'
if path not in sys.path:
    sys.path.insert(0, path)

# Activar entorno virtual
activate_this = '/home/joselito1988/.virtualenvs/libreria-joda/bin/activate_this.py'
with open(activate_this) as f:
    exec(f.read(), {'__file__': activate_this})

os.environ['DJANGO_SETTINGS_MODULE'] = 'libreria_joda.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
