import sys
import os
from TTS.api import TTS
import argparse

def tts_coqui(text, output_path, model_name="tts_models/es/mai/tacotron2-DDC"):
    """
    Convierte texto a voz usando Coqui TTS y guarda el resultado como WAV.
    :param text: Texto a convertir
    :param output_path: Ruta de salida WAV
    :param model_name: Modelo de Coqui TTS (por defecto español)
    """
    tts = TTS(model_name)
    tts.tts_to_file(text=text, file_path=output_path)
    print(f"Audio generado con Coqui TTS en {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demo TTS con Coqui (open source)")
    parser.add_argument('--text', type=str, required=True, help='Texto a convertir en voz')
    parser.add_argument('--output', type=str, default="static/tts_coqui_output.wav", help='Ruta de salida del audio WAV')
    parser.add_argument('--model', type=str, default="tts_models/es/mai/tacotron2-DDC", help='Nombre del modelo Coqui TTS')
    args = parser.parse_args()
    tts_coqui(args.text, args.output, args.model) 