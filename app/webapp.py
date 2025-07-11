import os
from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
from dotenv import load_dotenv
from tts import text_to_speech
from voice_cloning import clone_voice

app = Flask(__name__)
app.secret_key = 'demo_secret_key'

STATIC_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static')

@app.route('/', methods=['GET', 'POST'])
def index():
    tts_audio = None
    clone_audio = None
    if request.method == 'POST':
        if 'tts_text' in request.form:
            text = request.form['tts_text']
            output_path = os.path.join(STATIC_FOLDER, 'tts_output.wav')
            text_to_speech(text, output_path)
            tts_audio = 'tts_output.wav'
        elif 'clone_text' in request.form and 'clone_audio' in request.files:
            text = request.form['clone_text']
            audio_file = request.files['clone_audio']
            audio_path = os.path.join(STATIC_FOLDER, audio_file.filename)
            audio_file.save(audio_path)
            output_path = os.path.join(STATIC_FOLDER, 'clone_output.wav')
            clone_voice(audio_path, text, output_path)
            clone_audio = 'clone_output.wav'
    return render_template('index.html', tts_audio=tts_audio, clone_audio=clone_audio)

@app.route('/static/<filename>')
def static_files(filename):
    return send_from_directory(STATIC_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True) 