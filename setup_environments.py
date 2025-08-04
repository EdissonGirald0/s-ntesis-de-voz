#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil

# Configuración de entornos
ELEVENLABS_ENV = 'venv-elevenlabs'
COQUI_ENV = 'venv-coqui'  # Volver al disco principal

# Dependencias
ELEVENLABS_REQS = [
    'flask', 'python-dotenv', 'requests', 'werkzeug'
]

# Coqui TTS tiene problemas con Python 3.12+, usar alternativas
COQUI_REQS = [
    'torch',
    'torchaudio', 
    'soundfile',
    'librosa',
    'scipy',
    'numpy',
    'espeak-ng',  # Para síntesis básica
    'pyttsx3',    # Alternativa TTS offline
]


def run(cmd, env=None):
    print(f'→ {cmd}')
    result = subprocess.run(cmd, shell=True, env=env)
    if result.returncode != 0:
        print(f'❌ Error ejecutando: {cmd}')
        return False
    return True


def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    print(f'🐍 Python {version.major}.{version.minor}.{version.micro} detectado')
    
    if version >= (3, 12):
        print('⚠️  Coqui TTS no es compatible con Python 3.12+')
        print('   Usando alternativas de TTS para Python 3.12+')
        return False
    return True


def install_coqui_alternative():
    """Instalar alternativas a Coqui TTS para Python 3.12+"""
    print('📦 Instalando alternativas de TTS para Python 3.12+...')
    
    # Instalar espeak-ng desde el sistema
    system_install_commands = [
        'sudo apt update',
        'sudo apt install -y espeak espeak-data libespeak1 libespeak-dev',
        'sudo apt install -y festival festvox-kallpc16k',
        'sudo apt install -y flite'
    ]
    
    for cmd in system_install_commands:
        print(f'→ {cmd}')
        subprocess.run(cmd, shell=True, capture_output=True)
    
    return True


def clean_disk_space():
    """Limpia espacio en el disco"""
    print('🧹 Limpiando espacio en disco...')
    try:
        # Limpiar cache de pip
        subprocess.run('pip cache purge', shell=True, capture_output=True)
        # Limpiar cache de apt
        subprocess.run('sudo apt clean', shell=True, capture_output=True)
        # Eliminar paquetes no necesarios
        subprocess.run('sudo apt autoremove -y', shell=True, capture_output=True)
        print('✅ Limpieza completada')
    except Exception as e:
        print(f'⚠️  Error en limpieza: {e}')


def recreate_venv(venv_name):
    if os.path.exists(venv_name):
        print(f'🧹 Borrando entorno virtual anterior: {venv_name}')
        shutil.rmtree(venv_name)
    print(f'🐍 Creando entorno virtual: {venv_name}')
    return run(f'python3 -m venv {venv_name}')


def install_requirements(venv_name, reqs):
    pip = os.path.join(venv_name, 'bin', 'pip')
    if not run(f'{pip} install --upgrade pip setuptools wheel'):
        return False
    
    for req in reqs:
        if not run(f'{pip} install {req}'):
            print(f'⚠️  Error instalando {req}, continuando...')
            # No fallar completamente si una dependencia falla
            continue
    return True


def verify_install(venv_name, test_import):
    python = os.path.join(venv_name, 'bin', 'python')
    try:
        result = subprocess.run([python, '-c', test_import], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f'✅ {venv_name} verificado')
            return True
        else:
            print(f'⚠️  {venv_name} verificación falló: {result.stderr}')
            return False
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
        print(f'⚠️  {venv_name} verificación falló: {str(e)}')
        return False


def create_fallback_tts_script():
    """Crear script TTS alternativo para Python 3.12+"""
    fallback_script = '''#!/usr/bin/env python3
"""
Script TTS alternativo para cuando Coqui no está disponible
"""
import subprocess
import sys
import os

def tts_with_espeak(text, output_path):
    """TTS usando espeak"""
    try:
        cmd = ['espeak', '-s', '150', '-p', '50', '-w', output_path, text]
        subprocess.run(cmd, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def tts_with_pyttsx3(text, output_path):
    """TTS usando pyttsx3"""
    try:
        import pyttsx3
        engine = pyttsx3.init()
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        return True
    except ImportError:
        return False

def main():
    if len(sys.argv) < 3:
        print("Uso: python tts_fallback.py --text 'texto' --output archivo.wav")
        sys.exit(1)
    
    text = ""
    output = "output.wav"
    
    # Parse simple de argumentos
    for i, arg in enumerate(sys.argv):
        if arg == '--text' and i + 1 < len(sys.argv):
            text = sys.argv[i + 1]
        elif arg == '--output' and i + 1 < len(sys.argv):
            output = sys.argv[i + 1]
    
    if not text:
        print("Error: Texto requerido")
        sys.exit(1)
    
    print(f"Generando TTS: {text}")
    
    # Intentar métodos en orden
    if tts_with_espeak(text, output):
        print(f"TTS generado con espeak: {output}")
    elif tts_with_pyttsx3(text, output):
        print(f"TTS generado con pyttsx3: {output}")
    else:
        print("Error: No se pudo generar TTS")
        sys.exit(1)

if __name__ == "__main__":
    main()
'''
    
    with open('app/tts_fallback.py', 'w') as f:
        f.write(fallback_script)
    
    # Hacer ejecutable
    os.chmod('app/tts_fallback.py', 0o755)
    print('✅ Script TTS alternativo creado')


def main():
    print('🔄 Configurando entornos virtuales...')
    
    # Verificar espacio disponible
    result = subprocess.run(['df', '-h', '/'], capture_output=True, text=True)
    if result.returncode == 0:
        lines = result.stdout.strip().split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            if len(parts) >= 4:
                available = parts[3]
                print(f'💾 Espacio disponible en /: {available}')
                
                # Si hay menos de 5G, limpiar espacio
                if 'G' in available:
                    try:
                        available_gb = float(available.replace('G', ''))
                        if available_gb < 5:
                            print('⚠️  Poco espacio disponible. Limpiando...')
                            clean_disk_space()
                    except:
                        pass
    
    # Verificar versión de Python
    coqui_compatible = check_python_version()
    
    # ElevenLabs
    if not recreate_venv(ELEVENLABS_ENV):
        print('❌ Error creando entorno ElevenLabs')
        sys.exit(1)
        
    install_requirements(ELEVENLABS_ENV, ELEVENLABS_REQS)
    verify_install(ELEVENLABS_ENV, 'import flask, requests; print("ElevenLabs OK")')
    
    # Coqui/Alternativas
    print(f'📁 Creando entorno de TTS: {COQUI_ENV}')
    if not recreate_venv(COQUI_ENV):
        print('❌ Error creando entorno Coqui')
        sys.exit(1)
    
    if coqui_compatible:
        # Intentar instalar Coqui TTS original
        print('📦 Intentando instalar Coqui TTS...')
        coqui_success = install_requirements(COQUI_ENV, ['TTS'])
        if coqui_success:
            verify_install(COQUI_ENV, 'from TTS.api import TTS; print("Coqui OK")')
        else:
            print('⚠️  Coqui TTS falló, usando alternativas...')
            install_requirements(COQUI_ENV, COQUI_REQS)
            install_coqui_alternative()
            create_fallback_tts_script()
    else:
        # Python 3.12+, usar alternativas directamente
        print('📦 Instalando alternativas de TTS...')
        install_requirements(COQUI_ENV, COQUI_REQS)
        install_coqui_alternative()
        create_fallback_tts_script()
        verify_install(COQUI_ENV, 'import torch, soundfile; print("TTS Alternatives OK")')
    
    # Crear directorios necesarios
    directories = ['static', 'static/audio', 'static/css', 'static/js', 'logs']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f'📁 Directorio {directory} creado/verificado')
    
    print('\n✅ Configuración completada.')
    print('Puedes iniciar la aplicación con:')
    print('  source venv-elevenlabs/bin/activate && python app/webapp_working.py')
    print('\n💡 Nota: Si Coqui TTS no está disponible, se usarán alternativas de TTS')

if __name__ == '__main__':
    main() 