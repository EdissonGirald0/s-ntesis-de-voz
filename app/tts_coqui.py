import sys
import os
import subprocess
import argparse

def tts_coqui(text, output_path, model_name="fallback"):
    """
    Convierte texto a voz usando alternativas compatibles con Python 3.12.
    :param text: Texto a convertir
    :param output_path: Ruta de salida WAV
    :param model_name: Modelo (no usado en fallbacks)
    """
    print(f"🔊 Iniciando TTS alternativo para: '{text}'")
    print(f"📁 Archivo de salida: {output_path}")
    
    # Crear directorio de salida si no existe
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"📁 Directorio creado: {output_dir}")
    
    try:
        # Intentar usar pyttsx3 primero
        print("🔧 Intentando pyttsx3...")
        import pyttsx3
        engine = pyttsx3.init()
        
        # Configurar velocidad y voz en español si está disponible
        voices = engine.getProperty('voices')
        print(f"🎤 Voces disponibles: {len(voices)}")
        
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'es' in voice.id.lower():
                engine.setProperty('voice', voice.id)
                print(f"🎤 Voz en español seleccionada: {voice.name}")
                break
        
        engine.setProperty('rate', 150)  # Velocidad moderada
        engine.save_to_file(text, output_path)
        engine.runAndWait()
        
        # Verificar si el archivo se creó
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Audio generado con pyttsx3 en {output_path} ({file_size} bytes)")
            return True
        else:
            print("❌ pyttsx3 no creó el archivo")
            
    except Exception as e:
        print(f"❌ Error con pyttsx3: {e}")
    
    # Fallback a espeak
    try:
        print("🔧 Intentando espeak...")
        # Verificar si espeak está disponible
        subprocess.run(['which', 'espeak'], check=True, capture_output=True)
        
        # Usar espeak como alternativa
        cmd = [
            'espeak', 
            '-v', 'es',  # Voz en español
            '-s', '150', # Velocidad
            '-w', output_path,  # Guardar en archivo WAV
            text
        ]
        print(f"🔧 Ejecutando: {' '.join(cmd)}")
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Audio generado con espeak en {output_path} ({file_size} bytes)")
            return True
        else:
            print("❌ espeak no creó el archivo")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error ejecutando espeak: {e}")
    except Exception as e:
        print(f"❌ Error con espeak: {e}")
    
    # Último fallback: crear un archivo de audio silencioso como placeholder
    try:
        print("🔧 Creando archivo placeholder...")
        import numpy as np
        import soundfile as sf
        
        # Crear un segundo de silencio como placeholder
        sample_rate = 22050
        duration = 1.0
        silence = np.zeros(int(sample_rate * duration))
        sf.write(output_path, silence, sample_rate)
        
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"⚠️ Archivo placeholder creado en {output_path} ({file_size} bytes) - TTS no disponible")
            return True
        
    except Exception as e:
        print(f"❌ Error creando placeholder: {e}")
    
    print("❌ Todos los métodos fallaron")
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demo TTS con alternativas compatibles Python 3.12")
    parser.add_argument('--text', type=str, required=True, help='Texto a convertir en voz')
    parser.add_argument('--output', type=str, default="static/tts_coqui_output.wav", help='Ruta de salida del audio WAV')
    parser.add_argument('--model', type=str, default="fallback", help='Modelo (no usado en fallbacks)')
    args = parser.parse_args()
    
    success = tts_coqui(args.text, args.output, args.model)
    if not success:
        print("Error: No se pudo generar el audio")
        sys.exit(1) 