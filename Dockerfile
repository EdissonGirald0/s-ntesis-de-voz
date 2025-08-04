# 🐳 Multi-stage Dockerfile para Sistema de Síntesis de Voz
# Optimizado para Python 3.12, Flask, y TTS engines

# =====================================
# 🏗️ BUILD STAGE
# =====================================
FROM python:3.12-slim as builder

# Labels para metadatos
LABEL maintainer="EdissonGirald0"
LABEL description="Sistema de Síntesis de Voz con ElevenLabs y fallbacks"
LABEL version="1.0.0"

# Variables de entorno para build
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Instalar dependencias del sistema necesarias para build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    portaudio19-dev \
    espeak \
    espeak-data \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN useradd --create-home --shell /bin/bash app

# Crear directorio de trabajo
WORKDIR /app

# Copiar requirements para aprovechar cache de Docker
COPY requirements.txt .

# Instalar dependencias Python en virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# =====================================
# 🚀 PRODUCTION STAGE
# =====================================
FROM python:3.12-slim as production

# Variables de entorno para producción
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/opt/venv/bin:$PATH" \
    FLASK_ENV=production \
    FLASK_APP=app/webapp_working.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=5000

# Instalar solo dependencias runtime necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    espeak \
    espeak-data \
    portaudio19-dev \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y \
    && apt-get clean

# Crear usuario no-root
RUN useradd --create-home --shell /bin/bash --uid 1000 app

# Copiar virtual environment desde build stage
COPY --from=builder /opt/venv /opt/venv

# Crear directorio de trabajo y cambiar ownership
WORKDIR /app
RUN chown -R app:app /app

# Cambiar a usuario no-root
USER app

# Copiar código de la aplicación
COPY --chown=app:app . .

# Crear directorios necesarios con permisos correctos
RUN mkdir -p uploads output temp_audio logs static/audio && \
    chmod 755 uploads output temp_audio logs static/audio

# Verificar que espeak funciona
RUN echo "Docker build test" | espeak -s 150 -v es > /dev/null 2>&1 || echo "espeak warning: no audio device"

# Exponer puerto
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando por defecto
CMD ["python", "app/webapp_working.py"]

# =====================================
# 🔧 DEVELOPMENT STAGE
# =====================================
FROM production as development

USER root

# Instalar herramientas adicionales para desarrollo
RUN apt-get update && apt-get install -y --no-install-recommends \
    vim \
    git \
    htop \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias de desarrollo
RUN pip install --no-cache-dir \
    pytest \
    pytest-cov \
    black \
    flake8 \
    mypy \
    ipython \
    jupyter

USER app

# Variables de entorno para desarrollo
ENV FLASK_ENV=development \
    FLASK_DEBUG=True \
    LOG_LEVEL=DEBUG

# Comando para desarrollo con hot reload
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]

# =====================================
# 🧪 TESTING STAGE
# =====================================
FROM development as testing

# Copiar archivos de test
COPY --chown=app:app tests/ tests/
COPY --chown=app:app pytest.ini .
COPY --chown=app:app .coverage .

# Ejecutar tests al construir
RUN python -m pytest tests/ --cov=app --cov-report=html --cov-report=term

# Comando para testing continuo
CMD ["python", "-m", "pytest", "tests/", "--cov=app", "-v", "--tb=short"]
