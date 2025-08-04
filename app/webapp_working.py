#!/usr/bin/env python3
import os
import sys
import subprocess
from flask import Flask, render_template, request, send_from_directory, flash
from werkzeug.utils import secure_filename

def create_app():
    # Configurar Flask para encontrar las plantillas
    template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
    static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    
    print(f"📁 Carpeta de plantillas: {template_dir}")
    print(f"📁 Carpeta estática: {static_dir}")
    
    # Verificar que las carpetas existen
    if not os.path.exists(template_dir):
        print(f"❌ Carpeta de plantillas no encontrada: {template_dir}")
        return None
    
    if not os.path.exists(static_dir):
        print(f"📁 Creando carpeta estática: {static_dir}")
        os.makedirs(static_dir)
    
    app = Flask(__name__, 
               template_folder=template_dir,
               static_folder=static_dir)
    app.secret_key = 'demo_secret_key'
    
    def safe_import():
        """Importa módulos de forma segura"""
        try:
            from tts import text_to_speech
            from voice_cloning import clone_voice
            return text_to_speech, clone_voice
        except ImportError as e:
            print(f"⚠️  Error importando módulos: {e}")
            return None, None
    
    def run_coqui_tts(text, output_path):
        """Ejecuta TTS con Coqui"""
        try:
            venv_python = os.path.join(os.path.dirname(__file__), '..', 'venv-coqui', 'bin', 'python')
            script_path = os.path.join(os.path.dirname(__file__), 'tts_coqui.py')
            
            if not os.path.exists(venv_python):
                return False, "Entorno virtual de Coqui no encontrado"
            
            if not os.path.exists(script_path):
                return False, "Script tts_coqui.py no encontrado"
            
            # Asegurar que el directorio de salida existe
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            print(f"🔊 Ejecutando TTS Coqui: {text} -> {output_path}")
            cmd = [venv_python, script_path, '--text', text, '--output', output_path]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Verificar que el archivo se creó
            if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
                print(f"✅ TTS Coqui exitoso: {output_path}")
                return True, result.stdout
            else:
                return False, "No se pudo generar el archivo de audio"
                
        except subprocess.CalledProcessError as e:
            error_msg = f"Error ejecutando script: {e.stderr if e.stderr else str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
        except Exception as e:
            error_msg = f"Error inesperado: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def run_coqui_voice_cloning(audio_path, text, output_path):
        """Ejecuta clonación de voz con Coqui"""
        try:
            venv_python = os.path.join(os.path.dirname(__file__), '..', 'venv-coqui', 'bin', 'python')
            script_path = os.path.join(os.path.dirname(__file__), 'voice_cloning_coqui.py')
            if not os.path.exists(venv_python):
                return False, "Entorno virtual de Coqui no encontrado"
            cmd = [venv_python, script_path, '--audio', audio_path, '--text', text, '--output', output_path]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True, result.stdout
        except Exception as e:
            return False, str(e)
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        tts_audio = None
        clone_audio = None
        error_message = None
        
        # Importar módulos de forma segura
        text_to_speech, clone_voice = safe_import()
        
        if request.method == 'POST':
            # TTS
            if 'tts_text' in request.form:
                text = request.form['tts_text']
                engine = request.form.get('engine', 'elevenlabs')
                
                if text.strip():
                    if engine == 'coqui':
                        output_path = os.path.join(static_dir, 'coqui_tts_output.wav')
                        success, message = run_coqui_tts(text, output_path)
                        if success:
                            tts_audio = 'coqui_tts_output.wav'
                            flash('TTS generado exitosamente con Coqui', 'success')
                        else:
                            error_message = f"Error en TTS Coqui: {message}"
                            flash(error_message, 'error')
                    else:
                        if text_to_speech:
                            try:
                                output_path = os.path.join(static_dir, 'tts_output.wav')
                                text_to_speech(text, output_path)
                                tts_audio = 'tts_output.wav'
                                flash('TTS generado exitosamente con ElevenLabs', 'success')
                            except Exception as e:
                                error_message = f"Error en TTS ElevenLabs: {str(e)}"
                                flash(error_message, 'error')
                        else:
                            flash('ElevenLabs no disponible. Verifica la API key.', 'error')
            
            # Clonación de voz
            elif 'clone_text' in request.form and 'clone_audio' in request.files:
                text = request.form['clone_text']
                audio_file = request.files['clone_audio']
                engine = request.form.get('engine', 'elevenlabs')
                
                if audio_file and audio_file.filename and text.strip():
                    filename = secure_filename(audio_file.filename)
                    audio_path = os.path.join(static_dir, filename)
                    audio_file.save(audio_path)
                    
                    if engine == 'coqui':
                        output_path = os.path.join(static_dir, 'coqui_clone_output.wav')
                        success, message = run_coqui_voice_cloning(audio_path, text, output_path)
                        if success:
                            clone_audio = 'coqui_clone_output.wav'
                            flash('Voz clonada exitosamente con Coqui', 'success')
                        else:
                            error_message = f"Error en clonación Coqui: {message}"
                            flash(error_message, 'error')
                    else:
                        if clone_voice:
                            try:
                                output_path = os.path.join(static_dir, 'clone_output.wav')
                                clone_voice(audio_path, text, output_path)
                                clone_audio = 'clone_output.wav'
                                flash('Voz clonada exitosamente con ElevenLabs', 'success')
                            except Exception as e:
                                error_message = f"Error en clonación ElevenLabs: {str(e)}"
                                flash(error_message, 'error')
                        else:
                            flash('ElevenLabs no disponible. Verifica la API key.', 'error')
                else:
                    flash('Por favor, sube un archivo de audio válido y proporciona texto', 'error')
        
        return render_template('index.html', 
                             tts_audio=tts_audio, 
                             clone_audio=clone_audio,
                             error_message=error_message)
    
    @app.route('/static/<filename>')
    def static_files(filename):
        return send_from_directory(static_dir, filename)
    
    @app.route('/health')
    def health():
        return 'OK'
    
    return app

if __name__ == '__main__':
    print("🌐 Iniciando aplicación web...")
    
    app = create_app()
    if app is None:
        print("❌ No se pudo crear la aplicación")
        sys.exit(1)
    
    print("✅ Aplicación creada correctamente")
    print("🚀 Iniciando Flask en http://localhost:5000")
    print("💡 Para probar, visita: http://localhost:5000/health")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Error iniciando Flask: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 