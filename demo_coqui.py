#!/usr/bin/env python3
"""
Demo Coqui TTS (Open Source)
"""
import os
from TTS.api import TTS

def tts_coqui(text, output_path, model_name="tts_models/es/mai/tacotron2-DDC"):
    """
    Convierte texto a voz usando Coqui TTS y guarda el resultado como WAV.
    """
    try:
        print(f"🔄 Cargando modelo: {model_name}")
        tts = TTS(model_name)
        
        print(f"🎵 Generando audio...")
        tts.tts_to_file(text=text, file_path=output_path)
        
        print(f"✅ Audio de Coqui TTS guardado en {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error en Coqui TTS: {str(e)}")
        return False

if __name__ == "__main__":
    print("🎤 Demo Coqui TTS (Open Source)")
    print("=" * 40)
    
    text = "Hola, esta es una prueba de Coqui TTS usando tecnología open source."
    output_file = "static/coqui_demo.wav"
    
    success = tts_coqui(text, output_file)
    if success:
        print(f"📁 Archivo generado: {output_file}")
        print(f"📏 Tamaño: {os.path.getsize(output_file)} bytes") 