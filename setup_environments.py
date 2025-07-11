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
COQUI_REQS = [
    'TTS',  # instalará torch compatible automáticamente
]


def run(cmd, env=None):
    print(f'→ {cmd}')
    result = subprocess.run(cmd, shell=True, env=env)
    if result.returncode != 0:
        print(f'❌ Error ejecutando: {cmd}')
        sys.exit(1)


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
    run(f'python3 -m venv {venv_name}')


def install_requirements(venv_name, reqs):
    pip = os.path.join(venv_name, 'bin', 'pip')
    run(f'{pip} install --upgrade pip setuptools wheel')
    for req in reqs:
        run(f'{pip} install {req}')


def verify_install(venv_name, test_import):
    python = os.path.join(venv_name, 'bin', 'python')
    try:
        subprocess.check_call([python, '-c', test_import])
        print(f'✅ {venv_name} verificado')
    except subprocess.CalledProcessError:
        print(f'❌ Error verificando {venv_name}')
        sys.exit(1)


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
    
    # ElevenLabs
    recreate_venv(ELEVENLABS_ENV)
    install_requirements(ELEVENLABS_ENV, ELEVENLABS_REQS)
    verify_install(ELEVENLABS_ENV, 'import flask, requests; print("ElevenLabs OK")')
    
    # Coqui
    print(f'📁 Creando entorno Coqui: {COQUI_ENV}')
    recreate_venv(COQUI_ENV)
    install_requirements(COQUI_ENV, COQUI_REQS)
    verify_install(COQUI_ENV, 'from TTS.api import TTS; print("Coqui OK")')
    
    print('\n✅ Entornos virtuales listos.')
    print('Puedes iniciar la web unificada con:')
    print('  source venv-elevenlabs/bin/activate && python app/webapp_working.py')

if __name__ == '__main__':
    main() 