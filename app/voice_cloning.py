import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
# Endpoint para crear una voz clonada (IVC)
VOICE_CLONE_URL = "https://api.elevenlabs.io/v1/voices/add"
# Endpoint para TTS con voz clonada
TTS_CLONE_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"


def mostrar_mensaje_error(respuesta):
    try:
        data = respuesta.json()
        detail = data.get("detail", {})
        if isinstance(detail, dict):
            mensaje = detail.get("message", "Error desconocido.")
            status = detail.get("status", "")
            if status == "missing_permissions":
                print("[ERROR] Tu API Key no tiene permisos para clonar voces (voices_write).\nPor favor, revisa tu suscripción o API Key en ElevenLabs.")
            elif status == "can_not_use_instant_voice_cloning":
                print("[ERROR] Tu suscripción no permite el uso de Instant Voice Cloning.\nActualiza tu plan en ElevenLabs para habilitar esta función.")
            else:
                print(f"[ERROR] {mensaje}")
        else:
            print(f"[ERROR] {data}")
    except Exception:
        print("[ERROR] No se pudo interpretar la respuesta de error de la API.")
        print(respuesta.text)

def clone_voice_and_tts(audio_path, text, output_path):
    headers = {
        "xi-api-key": API_KEY
    }
    files = {
        "files": open(audio_path, "rb")
    }
    data = {
        "name": "VozClonadaDemo"
    }
    # Paso 1: Crear la voz clonada
    response = requests.post(VOICE_CLONE_URL, headers=headers, files=files, data=data)
    if response.status_code == 200:
        voice_id = response.json().get("voice_id")
        print(f"Voz clonada creada con voice_id: {voice_id}")
    else:
        mostrar_mensaje_error(response)
        return
    # Paso 2: Usar la voz clonada para TTS
    tts_url = TTS_CLONE_URL.format(voice_id=voice_id)
    headers_tts = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    data_tts = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "output_format": "mp3_44100_128"
    }
    response_tts = requests.post(tts_url, headers=headers_tts, json=data_tts)
    if response_tts.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response_tts.content)
        print(f"Audio clonado guardado en {output_path}")
    else:
        mostrar_mensaje_error(response_tts)

def clone_voice(audio_path, text, output_path):
    return clone_voice_and_tts(audio_path, text, output_path)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Demo ElevenLabs Voice Cloning")
    parser.add_argument('--audio', type=str, required=True, help='Ruta del audio de referencia (WAV/MP3)')
    parser.add_argument('--text', type=str, required=True, help='Texto a sintetizar con la voz clonada')
    parser.add_argument('--output', type=str, default="static/clone_output.mp3", help='Ruta de salida del audio')
    args = parser.parse_args()
    clone_voice(args.audio, args.text, args.output) 