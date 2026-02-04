"""
Launcher para el Sistema ERP de Librería JODA
Inicia el servidor Flask y abre el navegador automáticamente
"""
import subprocess
import webbrowser
import time
import socket
import sys
import os
from threading import Thread

def is_port_in_use(port):
    """Verifica si un puerto está en uso"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def wait_for_server(url, timeout=30):
    """Espera a que el servidor esté disponible"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect(('localhost', 5001))
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            time.sleep(0.5)
    return False

def open_browser():
    """Abre el navegador después de que el servidor esté listo"""
    url = 'http://127.0.0.1:5001'
    print(f"⏳ Esperando a que el servidor esté listo...")
    
    if wait_for_server(url):
        print(f"✅ Servidor listo. Abriendo navegador...")
        time.sleep(1)  # Pequeña pausa adicional
        webbrowser.open(url)
    else:
        print(f"⚠️  El servidor tardó mucho en iniciar. Abre manualmente: {url}")

def main():
    """Función principal del launcher"""
    print("=" * 60)
    print("🏪 SISTEMA ERP - LIBRERÍA JODA")
    print("=" * 60)
    print()
    
    # Verificar si el puerto ya está en uso
    if is_port_in_use(5001):
        print("⚠️  El puerto 5001 ya está en uso.")
        print("   El servidor podría estar ejecutándose.")
        print(f"   Abriendo navegador en: http://127.0.0.1:5001")
        print()
        webbrowser.open('http://127.0.0.1:5001')
        input("Presiona Enter para cerrar...")
        return
    
    # Cambiar al directorio del script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("🚀 Iniciando servidor Flask...")
    print("   URL: http://127.0.0.1:5001")
    print("   Para detener el servidor: Presiona Ctrl+C")
    print()
    
    # Iniciar el navegador en un hilo separado
    browser_thread = Thread(target=open_browser, daemon=True)
    browser_thread.start()
    
    # Iniciar el servidor Flask
    try:
        # Usar python directamente
        process = subprocess.Popen(
            [sys.executable, 'run.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        # Mostrar output del servidor
        for line in process.stdout:
            print(line, end='')
            
    except KeyboardInterrupt:
        print("\n")
        print("🛑 Deteniendo servidor...")
        process.terminate()
        print("✅ Servidor detenido correctamente.")
    except Exception as e:
        print(f"❌ Error al iniciar el servidor: {e}")
        input("Presiona Enter para cerrar...")

if __name__ == '__main__':
    main()
