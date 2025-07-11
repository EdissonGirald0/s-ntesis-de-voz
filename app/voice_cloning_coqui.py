import argparse
import os
import sys
import tempfile
import subprocess
from pathlib import Path

def check_coqui_environment():
    """Verifica que el entorno de Coqui esté disponible"""
    try:
        import torch
        import TTS
        print(f"✅ Coqui TTS disponible: {TTS.__version__}")
        print(f"✅ PyTorch disponible: {torch.__version__}")
        return True
    except ImportError as e:
        print(f"❌ Error: {e}")
        print("💡 Asegúrate de activar el entorno virtual de Coqui:")
        print("   source venv-coqui/bin/activate")
        return False

def voice_cloning_coqui(audio_path, text, output_path):
    """
    Clona voz usando Coqui TTS con YourTTS o modelo similar
    """
    if not check_coqui_environment():
        return False
    
    try:
        from TTS.api import TTS
        
        print("🎤 Iniciando clonación de voz con Coqui TTS...")
        print(f"📁 Audio de referencia: {audio_path}")
        print(f"📝 Texto a sintetizar: {text}")
        print(f"💾 Archivo de salida: {output_path}")
        
        # Listar modelos disponibles
        print("\n📋 Modelos disponibles:")
        models = TTS.list_models()
        tts_models = [m for m in models if "tts_models" in m]
        
        # Buscar modelos que soporten clonación de voz
        voice_cloning_models = [
            m for m in tts_models 
            if any(keyword in m.lower() for keyword in ["yourtts", "voice_cloning", "multilingual"])
        ]
        
        if not voice_cloning_models:
            print("⚠️  No se encontraron modelos de clonación de voz")
            print("📦 Modelos TTS disponibles:")
            for i, model in enumerate(tts_models[:5]):  # Mostrar solo los primeros 5
                print(f"   {i+1}. {model}")
            return False
        
        # Usar el primer modelo de clonación disponible
        model_name = voice_cloning_models[0]
        print(f"🎯 Usando modelo: {model_name}")
        
        # Inicializar TTS
        tts = TTS(model_name)
        
        # Generar audio clonado
        print("🔄 Generando audio clonado...")
        tts.tts_to_file(
            text=text,
            speaker_wav=audio_path,
            file_path=output_path,
            language="es"  # Español
        )
        
        print(f"✅ Audio clonado generado: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error durante la clonación: {e}")
        print("\n💡 Soluciones posibles:")
        print("1. Verifica que el audio de referencia sea válido (WAV/MP3)")
        print("2. Asegúrate de tener suficiente espacio en disco")
        print("3. El audio de referencia debe ser de buena calidad (16kHz+ recomendado)")
        return False

def voice_cloning_coqui_simple(audio_path, text, output_path):
    """
    Implementación simplificada usando YourTTS específicamente
    """
    if not check_coqui_environment():
        return False
    
    try:
        from TTS.api import TTS
        
        print("🎤 Clonación de voz con YourTTS...")
        
        # Usar YourTTS específicamente
        tts = TTS("tts_models/multilingual/multi-dataset/your_tts")
        
        # Generar audio
        tts.tts_to_file(
            text=text,
            speaker_wav=audio_path,
            file_path=output_path,
            language="es"
        )
        
        print(f"✅ Audio generado: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def record_audio_for_cloning(duration=5, output_path="static/audio_referencia.wav"):
    """
    Graba audio para usar como referencia en clonación
    """
    try:
        import sounddevice as sd
        import soundfile as sf
        import numpy as np
        
        print(f"🎙️  Grabando audio de referencia ({duration} segundos)...")
        print("Habla claramente para obtener mejores resultados")
        
        # Configurar grabación
        sample_rate = 22050  # Frecuencia recomendada para TTS
        recording = sd.rec(int(duration * sample_rate), 
                          samplerate=sample_rate, 
                          channels=1, 
                          dtype=np.float32)
        
        sd.wait()  # Esperar a que termine la grabación
        
        # Guardar audio
        sf.write(output_path, recording, sample_rate)
        print(f"✅ Audio guardado: {output_path}")
        return output_path
        
    except ImportError:
        print("❌ sounddevice no está instalado")
        print("💡 Instala con: pip install sounddevice")
        return None
    except Exception as e:
        print(f"❌ Error grabando audio: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demo de clonación de voz con Coqui TTS")
    parser.add_argument('--audio', type=str, help='Ruta del audio de referencia (WAV/MP3)')
    parser.add_argument('--text', type=str, help='Texto a sintetizar con la voz clonada')
    parser.add_argument('--output', type=str, default="static/clone_coqui_output.wav", 
                       help='Ruta de salida del audio WAV')
    parser.add_argument('--record', action='store_true', 
                       help='Grabar audio de referencia')
    parser.add_argument('--duration', type=int, default=5, 
                       help='Duración de la grabación en segundos')
    
    args = parser.parse_args()
    
    if args.record:
        audio_path = record_audio_for_cloning(args.duration)
        if audio_path:
            print(f"\n🎯 Audio de referencia grabado: {audio_path}")
            print("💡 Ahora puedes usar este archivo con --audio")
    elif args.audio and args.text:
        success = voice_cloning_coqui(args.audio, args.text, args.output)
        if success:
            print(f"\n🎉 ¡Clonación completada! Archivo: {args.output}")
        else:
            print("\n❌ La clonación falló")
    else:
        print("❌ Uso:")
        print("  Para grabar audio: python app/voice_cloning_coqui.py --record")
        print("  Para clonar voz: python app/voice_cloning_coqui.py --audio <archivo> --text 'texto'")
        print("\n💡 Ejemplo:")
        print("  python app/voice_cloning_coqui.py --audio static/audio_referencia.wav --text 'Hola, esta es mi voz clonada'") 