"""
Script para crear el ejecutable del Sistema ERP Librería JODA
Usa PyInstaller para generar un .exe para Windows
"""
import subprocess
import sys
import os

def install_pyinstaller():
    """Instala PyInstaller si no está disponible"""
    print("📦 Verificando PyInstaller...")
    try:
        import PyInstaller
        print("✅ PyInstaller ya está instalado")
        return True
    except ImportError:
        print("⚠️  PyInstaller no encontrado. Instalando...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("✅ PyInstaller instalado correctamente")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error al instalar PyInstaller")
            return False

def create_executable():
    """Crea el ejecutable usando PyInstaller"""
    print("\n" + "=" * 60)
    print("🔨 CREANDO EJECUTABLE - LIBRERÍA JODA ERP")
    print("=" * 60 + "\n")
    
    # Verificar que launcher.py existe
    if not os.path.exists('launcher.py'):
        print("❌ Error: No se encuentra launcher.py")
        return False
    
    # Verificar que el logo existe
    icon_path = 'logo/logo.ico' if os.path.exists('logo/logo.ico') else None
    
    print("📋 Configuración:")
    print(f"   - Script: launcher.py")
    print(f"   - Nombre: Libreria_JODA_ERP.exe")
    print(f"   - Icono: {icon_path if icon_path else 'Sin icono'}")
    print(f"   - Modo: Consola visible")
    print()
    
    # Comando de PyInstaller
    command = [
        'pyinstaller',
        '--onefile',  # Un solo archivo ejecutable
        '--name=Libreria_JODA_ERP',  # Nombre del ejecutable
        '--clean',  # Limpiar cache
    ]
    
    # Agregar icono si existe
    if icon_path:
        command.append(f'--icon={icon_path}')
    
    # Agregar el script
    command.append('launcher.py')
    
    print("🚀 Ejecutando PyInstaller...")
    print(f"   Comando: {' '.join(command)}")
    print()
    
    try:
        subprocess.check_call(command)
        print("\n" + "=" * 60)
        print("✅ EJECUTABLE CREADO EXITOSAMENTE")
        print("=" * 60)
        print()
        print("📁 Ubicación: dist/Libreria_JODA_ERP.exe")
        print()
        print("📝 Instrucciones de uso:")
        print("   1. El archivo .exe está en la carpeta 'dist'")
        print("   2. Copia el .exe al directorio raíz del proyecto")
        print("   3. Haz doble clic en el .exe para iniciar el sistema")
        print("   4. El navegador se abrirá automáticamente")
        print()
        print("⚠️  IMPORTANTE:")
        print("   - El .exe debe estar en el mismo directorio que 'run.py'")
        print("   - Mantén todas las carpetas del proyecto intactas")
        print("   - Asegúrate de tener Python y las dependencias instaladas")
        print()
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error al crear el ejecutable: {e}")
        return False
    except FileNotFoundError:
        print("\n❌ Error: PyInstaller no está en el PATH")
        print("   Intenta reinstalar PyInstaller")
        return False

def main():
    """Función principal"""
    if not install_pyinstaller():
        input("\nPresiona Enter para cerrar...")
        return
    
    if create_executable():
        print("✨ Proceso completado exitosamente")
    else:
        print("❌ El proceso falló")
    
    input("\nPresiona Enter para cerrar...")

if __name__ == '__main__':
    main()
