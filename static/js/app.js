// JavaScript mejorado para la aplicación de síntesis de voz
class VoiceSynthesisApp {
    constructor() {
        this.init();
        this.setupEventListeners();
        this.setupFormValidation();
        this.setupAudioControls();
    }

    init() {
        console.log('🎤 Inicializando aplicación de síntesis de voz...');
        this.showNotification('Aplicación cargada correctamente', 'success');
        this.checkBrowserCompatibility();
    }

    checkBrowserCompatibility() {
        // Verificar soporte para File API
        if (!window.File || !window.FileReader) {
            this.showNotification('Tu navegador no soporta la carga de archivos', 'warning');
        }

        // Verificar soporte para Web Audio API
        if (!window.AudioContext && !window.webkitAudioContext) {
            this.showNotification('Tu navegador tiene soporte limitado para audio', 'warning');
        }
    }

    setupEventListeners() {
        // Botones de envío de formularios
        const ttsForm = document.querySelector('form[method="post"]');
        if (ttsForm) {
            ttsForm.addEventListener('submit', (e) => this.handleFormSubmit(e, 'tts'));
        }

        // File input para clonación de voz
        const audioInput = document.getElementById('clone_audio');
        if (audioInput) {
            audioInput.addEventListener('change', (e) => this.handleFileUpload(e));
        }

        // Selectores de motor
        const engineSelects = document.querySelectorAll('select[name="engine"]');
        engineSelects.forEach(select => {
            select.addEventListener('change', (e) => this.handleEngineChange(e));
        });

        // Botones de descarga
        const downloadLinks = document.querySelectorAll('a[download]');
        downloadLinks.forEach(link => {
            link.addEventListener('click', (e) => this.handleDownload(e));
        });
    }

    setupFormValidation() {
        // Validación de texto
        const textAreas = document.querySelectorAll('textarea[required]');
        textAreas.forEach(textarea => {
            textarea.addEventListener('input', (e) => this.validateText(e.target));
            textarea.addEventListener('blur', (e) => this.validateText(e.target));
        });

        // Validación de archivos
        const fileInputs = document.querySelectorAll('input[type="file"]');
        fileInputs.forEach(input => {
            input.addEventListener('change', (e) => this.validateFile(e.target));
        });
    }

    setupAudioControls() {
        // Controles de audio personalizados
        const audioElements = document.querySelectorAll('audio');
        audioElements.forEach(audio => {
            this.enhanceAudioPlayer(audio);
        });
    }

    handleFormSubmit(event, formType) {
        console.log(`📝 Enviando formulario: ${formType}`);
        
        const form = event.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        
        // Validar formulario antes de enviar
        if (!this.validateForm(form)) {
            event.preventDefault();
            return false;
        }

        // Mostrar estado de carga
        this.showLoadingState(submitBtn, true);
        this.showNotification('Procesando solicitud...', 'info');

        // Simular progreso (se puede conectar con backend real)
        this.showProgress(0);
        const progressInterval = setInterval(() => {
            const current = parseInt(document.querySelector('.progress-bar')?.style.width || '0');
            if (current < 90) {
                this.showProgress(current + 10);
            } else {
                clearInterval(progressInterval);
            }
        }, 500);

        return true;
    }

    validateForm(form) {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                this.showFieldError(field, 'Este campo es obligatorio');
                isValid = false;
            } else {
                this.clearFieldError(field);
            }
        });

        return isValid;
    }

    validateText(textarea) {
        const text = textarea.value.trim();
        const minLength = 3;
        const maxLength = 1000;

        if (text.length < minLength) {
            this.showFieldError(textarea, `Mínimo ${minLength} caracteres`);
            return false;
        }

        if (text.length > maxLength) {
            this.showFieldError(textarea, `Máximo ${maxLength} caracteres`);
            return false;
        }

        this.clearFieldError(textarea);
        this.updateCharacterCount(textarea, text.length, maxLength);
        return true;
    }

    validateFile(fileInput) {
        const file = fileInput.files[0];
        if (!file) return false;

        const allowedTypes = ['audio/wav', 'audio/mp3', 'audio/mpeg'];
        const maxSize = 10 * 1024 * 1024; // 10MB

        if (!allowedTypes.includes(file.type)) {
            this.showFieldError(fileInput, 'Solo se permiten archivos WAV y MP3');
            return false;
        }

        if (file.size > maxSize) {
            this.showFieldError(fileInput, 'El archivo no debe superar 10MB');
            return false;
        }

        this.clearFieldError(fileInput);
        this.showFileInfo(fileInput, file);
        return true;
    }

    handleFileUpload(event) {
        const file = event.target.files[0];
        if (!file) return;

        console.log('📁 Archivo seleccionado:', file.name);

        // Mostrar preview del archivo
        this.showFilePreview(file, event.target);

        // Validar archivo
        if (!this.validateFile(event.target)) {
            event.target.value = '';
            return;
        }

        this.showNotification(`Archivo "${file.name}" cargado correctamente`, 'success');
    }

    handleEngineChange(event) {
        const engine = event.target.value;
        console.log('🔧 Motor cambiado a:', engine);
        
        // Mostrar información específica del motor
        this.showEngineInfo(engine, event.target);
        
        // Actualizar UI según el motor seleccionado
        this.updateUIForEngine(engine);
    }

    handleDownload(event) {
        const link = event.target;
        const filename = link.getAttribute('href').split('/').pop();
        
        console.log('⬇️ Descargando archivo:', filename);
        this.showNotification(`Descargando ${filename}...`, 'info');
        
        // Analytics o tracking si es necesario
        this.trackDownload(filename);
    }

    showLoadingState(button, loading) {
        if (loading) {
            button.classList.add('loading');
            button.disabled = true;
            button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Procesando...';
        } else {
            button.classList.remove('loading');
            button.disabled = false;
            button.innerHTML = button.getAttribute('data-original-text') || 'Procesar';
        }
    }

    showProgress(percentage) {
        let progressContainer = document.querySelector('.progress-container');
        
        if (!progressContainer) {
            progressContainer = document.createElement('div');
            progressContainer.className = 'progress-container';
            progressContainer.innerHTML = `
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span>Procesando...</span>
                    <span class="progress-percentage">${percentage}%</span>
                </div>
                <div class="progress">
                    <div class="progress-bar" style="width: ${percentage}%"></div>
                </div>
            `;
            
            const firstCard = document.querySelector('.feature-card');
            if (firstCard) {
                firstCard.parentNode.insertBefore(progressContainer, firstCard);
            }
        } else {
            const progressBar = progressContainer.querySelector('.progress-bar');
            const progressText = progressContainer.querySelector('.progress-percentage');
            
            progressBar.style.width = `${percentage}%`;
            progressText.textContent = `${percentage}%`;
        }

        if (percentage >= 100) {
            setTimeout(() => {
                progressContainer.remove();
            }, 1000);
        }
    }

    showNotification(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
        alertDiv.innerHTML = `
            <i class="fas fa-${this.getIconForType(type)}"></i>
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        const container = document.querySelector('.main-container');
        const firstChild = container.firstElementChild;
        container.insertBefore(alertDiv, firstChild);

        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }

    getIconForType(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'exclamation-triangle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }

    showFieldError(field, message) {
        this.clearFieldError(field);
        
        field.classList.add('is-invalid');
        
        const errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        errorDiv.textContent = message;
        
        field.parentNode.appendChild(errorDiv);
    }

    clearFieldError(field) {
        field.classList.remove('is-invalid');
        
        const existingError = field.parentNode.querySelector('.invalid-feedback');
        if (existingError) {
            existingError.remove();
        }
    }

    updateCharacterCount(textarea, current, max) {
        let counter = textarea.parentNode.querySelector('.character-count');
        
        if (!counter) {
            counter = document.createElement('small');
            counter.className = 'character-count text-muted';
            textarea.parentNode.appendChild(counter);
        }
        
        counter.textContent = `${current}/${max} caracteres`;
        
        if (current > max * 0.9) {
            counter.className = 'character-count text-warning';
        } else {
            counter.className = 'character-count text-muted';
        }
    }

    showFileInfo(fileInput, file) {
        const infoDiv = document.createElement('div');
        infoDiv.className = 'file-info mt-2 text-muted';
        infoDiv.innerHTML = `
            <small>
                <i class="fas fa-file-audio"></i>
                ${file.name} (${this.formatFileSize(file.size)})
            </small>
        `;
        
        // Remover info anterior si existe
        const existingInfo = fileInput.parentNode.querySelector('.file-info');
        if (existingInfo) {
            existingInfo.remove();
        }
        
        fileInput.parentNode.appendChild(infoDiv);
    }

    showFilePreview(file, fileInput) {
        if (file.type.startsWith('audio/')) {
            const audio = document.createElement('audio');
            audio.controls = true;
            audio.className = 'audio-player mt-2';
            audio.src = URL.createObjectURL(file);
            
            // Remover preview anterior si existe
            const existingPreview = fileInput.parentNode.querySelector('.file-preview');
            if (existingPreview) {
                existingPreview.remove();
            }
            
            const previewDiv = document.createElement('div');
            previewDiv.className = 'file-preview';
            previewDiv.appendChild(audio);
            
            fileInput.parentNode.appendChild(previewDiv);
        }
    }

    showEngineInfo(engine, select) {
        const infoMessages = {
            'elevenlabs': 'Motor comercial - Alta calidad, requiere API key',
            'coqui': 'Motor open source - Gratuito, procesamiento local'
        };
        
        const message = infoMessages[engine] || '';
        
        // Remover info anterior
        const existingInfo = select.parentNode.querySelector('.engine-info');
        if (existingInfo) {
            existingInfo.remove();
        }
        
        if (message) {
            const infoDiv = document.createElement('small');
            infoDiv.className = 'engine-info text-muted d-block mt-1';
            infoDiv.textContent = message;
            
            select.parentNode.appendChild(infoDiv);
        }
    }

    updateUIForEngine(engine) {
        // Personalizar UI según el motor seleccionado
        const cards = document.querySelectorAll('.feature-card');
        
        cards.forEach(card => {
            const engineSelect = card.querySelector('select[name="engine"]');
            if (engineSelect && engineSelect.value === engine) {
                // Agregar clase CSS específica del motor
                card.classList.remove('engine-elevenlabs', 'engine-coqui');
                card.classList.add(`engine-${engine}`);
            }
        });
    }

    enhanceAudioPlayer(audio) {
        // Agregar controles personalizados
        audio.addEventListener('loadstart', () => {
            console.log('🎵 Cargando audio...');
        });
        
        audio.addEventListener('canplay', () => {
            console.log('▶️ Audio listo para reproducir');
        });
        
        audio.addEventListener('error', (e) => {
            console.error('❌ Error reproduciendo audio:', e);
            this.showNotification('Error reproduciendo el audio', 'error');
        });
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    trackDownload(filename) {
        // Implementar tracking/analytics si es necesario
        console.log('📊 Tracking download:', filename);
    }
}

// Utilidades adicionales
class AudioUtils {
    static async getAudioDuration(file) {
        return new Promise((resolve) => {
            const audio = new Audio();
            audio.addEventListener('loadedmetadata', () => {
                resolve(audio.duration);
            });
            audio.src = URL.createObjectURL(file);
        });
    }

    static async analyzeAudioFile(file) {
        const duration = await this.getAudioDuration(file);
        
        return {
            name: file.name,
            size: file.size,
            type: file.type,
            duration: duration,
            quality: this.assessAudioQuality(file)
        };
    }

    static assessAudioQuality(file) {
        // Evaluación básica basada en tamaño y tipo
        const sizePerSecond = file.size / 1000; // Aproximado
        
        if (sizePerSecond > 100) return 'alta';
        if (sizePerSecond > 50) return 'media';
        return 'baja';
    }
}

// Inicializar la aplicación cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    window.voiceApp = new VoiceSynthesisApp();
});

// Manejar errores globales
window.addEventListener('error', (e) => {
    console.error('Error global:', e.error);
    if (window.voiceApp) {
        window.voiceApp.showNotification('Ha ocurrido un error inesperado', 'error');
    }
});

// Manejar promesas rechazadas
window.addEventListener('unhandledrejection', (e) => {
    console.error('Promesa rechazada:', e.reason);
    if (window.voiceApp) {
        window.voiceApp.showNotification('Error de procesamiento', 'error');
    }
});
