import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
# Usamos el voice_id de "Sarah" (es compatible con español):
VOICE_ID = "EXAVITQu4vr4xnSDxMaL"
API_URL = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"


def text_to_speech(text, output_path):
    headers = {
        "xi-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "output_format": "mp3_44100_128"
    }
    response = requests.post(API_URL, headers=headers, json=data)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Audio guardado en {output_path}")
    else:
        print("Error:", response.text)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Demo ElevenLabs TTS")
    parser.add_argument('--text', type=str, required=True, help='Texto a convertir en voz')
    parser.add_argument('--output', type=str, default="static/tts_output.mp3", help='Ruta de salida del audio')
    args = parser.parse_args()
    text_to_speech(args.text, args.output) 