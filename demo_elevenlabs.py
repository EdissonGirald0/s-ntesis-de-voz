#!/usr/bin/env python3
"""
Demo ElevenLabs TTS
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ELEVENLABS_API_KEY")
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
        print(f"✅ Audio de ElevenLabs guardado en {output_path}")
        return True
    else:
        print(f"❌ Error en ElevenLabs: {response.text}")
        return False

if __name__ == "__main__":
    print("🎤 Demo ElevenLabs TTS")
    print("=" * 40)
    
    text = "Hola, esta es una prueba de ElevenLabs usando la API comercial."
    output_file = "static/elevenlabs_demo.mp3"
    
    success = text_to_speech(text, output_file)
    if success:
        print(f"📁 Archivo generado: {output_file}")
        print(f"📏 Tamaño: {os.path.getsize(output_file)} bytes") 