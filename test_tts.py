#!/usr/bin/env python3
"""
Script de prueba para verificar que el TTS funciona correctamente
"""

import os
import sys
import subprocess

def test_coqui_tts():
    """Prueba la funcionalidad de TTS con Coqui"""
    print("🧪 Probando TTS con alternativas de Coqui...")
    
    # Configurar paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_python = os.path.join(script_dir, 'venv-coqui', 'bin', 'python')
    tts_script = os.path.join(script_dir, 'app', 'tts_coqui.py')
    output_path = os.path.join(script_dir, 'static', 'test_tts_output.wav')
    
    # Texto de prueba
    test_text = "Hola, esta es una prueba del sistema de síntesis de voz."
    
    print(f"📝 Texto: {test_text}")
    print(f"🐍 Python: {venv_python}")
    print(f"📜 Script: {tts_script}")
    print(f"📁 Salida: {output_path}")
    
    # Verificar que los archivos existen
    if not os.path.exists(venv_python):
        print(f"❌ Python del entorno virtual no encontrado: {venv_python}")
        return False
    
    if not os.path.exists(tts_script):
        print(f"❌ Script TTS no encontrado: {tts_script}")
        return False
    
    try:
        # Ejecutar TTS
        cmd = [venv_python, tts_script, '--text', test_text, '--output', output_path]
        print(f"🔧 Ejecutando: {' '.join(cmd)}")
        
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        
        print("📤 Salida del script:")
        print(result.stdout)
        
        if result.stderr:
            print("⚠️ Errores:")
            print(result.stderr)
        
        # Verificar que el archivo se creó
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Archivo creado exitosamente: {output_path} ({file_size} bytes)")
            
            # Mostrar información del archivo
            import datetime
            mod_time = os.path.getmtime(output_path)
            mod_time_str = datetime.datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
            print(f"📅 Modificado: {mod_time_str}")
            
            return True
        else:
            print("❌ El archivo no se creó")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando script: {e}")
        print(f"📤 stdout: {e.stdout}")
        print(f"📤 stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_elevenlabs_import():
    """Prueba la importación de ElevenLabs"""
    print("\n🧪 Probando importación de ElevenLabs...")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_python = os.path.join(script_dir, 'venv-elevenlabs', 'bin', 'python')
    
    try:
        cmd = [venv_python, '-c', 'import elevenlabs; print("✅ ElevenLabs importado correctamente")']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(result.stdout.strip())
        return True
    except Exception as e:
        print(f"❌ Error importando ElevenLabs: {e}")
        return False

def main():
    print("🚀 Iniciando pruebas de funcionalidad TTS...")
    print("=" * 60)
    
    # Probar Coqui TTS (alternativas)
    coqui_ok = test_coqui_tts()
    
    # Probar ElevenLabs
    elevenlabs_ok = test_elevenlabs_import()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN DE PRUEBAS:")
    print(f"🔊 TTS Coqui (alternativas): {'✅ OK' if coqui_ok else '❌ FAIL'}")
    print(f"🎤 ElevenLabs import: {'✅ OK' if elevenlabs_ok else '❌ FAIL'}")
    
    if coqui_ok or elevenlabs_ok:
        print("\n🎉 Al menos un motor TTS está funcionando!")
        return True
    else:
        print("\n💥 Ningún motor TTS está funcionando correctamente")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
