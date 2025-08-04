#!/usr/bin/env python3
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
