import sounddevice as sd
import numpy as np
import wave
import argparse


def grabar_audio(nombre_archivo, duracion=5, fs=44100):
    print(f"Grabando {duracion} segundos... Hable ahora.")
    audio = sd.rec(int(duracion * fs), samplerate=fs, channels=1, dtype=np.int16)
    sd.wait()
    with wave.open(nombre_archivo, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16 bits
        wf.setframerate(fs)
        wf.writeframes(audio.tobytes())
    print(f"Audio guardado en {nombre_archivo}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Graba audio desde el micrófono y guarda como WAV.")
    parser.add_argument('--output', type=str, default='static/audio_referencia.wav', help='Archivo de salida WAV')
    parser.add_argument('--duration', type=int, default=5, help='Duración de la grabación en segundos')
    args = parser.parse_args()
    grabar_audio(args.output, args.duration) 