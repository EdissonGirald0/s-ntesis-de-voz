#!/usr/bin/env python3
"""
Sistema de configuración centralizado para la aplicación de síntesis de voz
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import json
from dataclasses import dataclass, asdict
from dotenv import load_dotenv


@dataclass
class ElevenLabsConfig:
    """Configuración para ElevenLabs"""
    api_key: str = ""
    default_voice_id: str = "EXAVITQu4vr4xnSDxMaL"  # Sarah
    model_id: str = "eleven_multilingual_v2"
    output_format: str = "mp3_44100_128"
    stability: float = 0.5
    similarity_boost: float = 0.75
    timeout: int = 30
    max_retries: int = 3


@dataclass
class CoquiConfig:
    """Configuración para Coqui TTS"""
    default_model: str = "tts_models/es/mai/tacotron2-DDC"
    voice_cloning_model: str = "tts_models/multilingual/multi-dataset/your_tts"
    sample_rate: int = 22050
    cache_dir: str = "models_cache"
    use_gpu: bool = False
    models_preload: bool = True


@dataclass
class WebConfig:
    """Configuración para la aplicación web"""
    host: str = "0.0.0.0"
    port: int = 8080
    debug: bool = False
    secret_key: str = "demo_secret_key_change_in_production"
    max_content_length: int = 16 * 1024 * 1024  # 16MB
    upload_folder: str = "static/uploads"
    allowed_extensions: tuple = ("wav", "mp3", "m4a", "flac")
    session_timeout: int = 3600  # 1 hora


@dataclass
class SecurityConfig:
    """Configuración de seguridad"""
    rate_limit_per_minute: int = 60
    max_text_length: int = 1000
    max_audio_duration: int = 300  # 5 minutos
    allowed_origins: list = None
    enable_cors: bool = True
    csrf_protection: bool = True


@dataclass
class LoggingConfig:
    """Configuración de logging"""
    level: str = "INFO"
    log_dir: str = "logs"
    max_log_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    log_format: str = "%(asctime)s | %(name)s | %(levelname)s | %(module)s:%(lineno)d | %(message)s"
    enable_metrics: bool = True
    metrics_retention_days: int = 30


@dataclass
class PerformanceConfig:
    """Configuración de rendimiento"""
    async_processing: bool = True
    max_concurrent_requests: int = 10
    request_timeout: int = 120
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hora
    preload_models: bool = False


@dataclass
class AppConfig:
    """Configuración principal de la aplicación"""
    # Configuraciones específicas
    elevenlabs: ElevenLabsConfig
    coqui: CoquiConfig
    web: WebConfig
    security: SecurityConfig
    logging: LoggingConfig
    performance: PerformanceConfig
    
    # Metadatos
    app_name: str = "Voice Synthesis Demo"
    version: str = "1.0.0"
    environment: str = "development"
    timezone: str = "UTC"
    
    @classmethod
    def from_env(cls, env_file: str = ".env") -> "AppConfig":
        """Crear configuración desde variables de entorno"""
        
        # Cargar archivo .env si existe
        env_path = Path(env_file)
        if env_path.exists():
            load_dotenv(env_path)
        
        return cls(
            elevenlabs=ElevenLabsConfig(
                api_key=os.getenv("ELEVENLABS_API_KEY", ""),
                default_voice_id=os.getenv("ELEVENLABS_VOICE_ID", "EXAVITQu4vr4xnSDxMaL"),
                model_id=os.getenv("ELEVENLABS_MODEL_ID", "eleven_multilingual_v2"),
                output_format=os.getenv("ELEVENLABS_OUTPUT_FORMAT", "mp3_44100_128"),
                stability=float(os.getenv("ELEVENLABS_STABILITY", "0.5")),
                similarity_boost=float(os.getenv("ELEVENLABS_SIMILARITY_BOOST", "0.75")),
                timeout=int(os.getenv("ELEVENLABS_TIMEOUT", "30")),
                max_retries=int(os.getenv("ELEVENLABS_MAX_RETRIES", "3"))
            ),
            coqui=CoquiConfig(
                default_model=os.getenv("COQUI_DEFAULT_MODEL", "tts_models/es/mai/tacotron2-DDC"),
                voice_cloning_model=os.getenv("COQUI_VOICE_CLONING_MODEL", "tts_models/multilingual/multi-dataset/your_tts"),
                sample_rate=int(os.getenv("COQUI_SAMPLE_RATE", "22050")),
                cache_dir=os.getenv("COQUI_CACHE_DIR", "models_cache"),
                use_gpu=os.getenv("COQUI_USE_GPU", "False").lower() == "true",
                models_preload=os.getenv("COQUI_MODELS_PRELOAD", "True").lower() == "true"
            ),
            web=WebConfig(
                host=os.getenv("FLASK_HOST", "0.0.0.0"),
                port=int(os.getenv("FLASK_PORT", "8080")),
                debug=os.getenv("FLASK_DEBUG", "False").lower() == "true",
                secret_key=os.getenv("FLASK_SECRET_KEY", "demo_secret_key_change_in_production"),
                max_content_length=int(os.getenv("MAX_CONTENT_LENGTH", str(16 * 1024 * 1024))),
                upload_folder=os.getenv("UPLOAD_FOLDER", "static/uploads"),
                session_timeout=int(os.getenv("SESSION_TIMEOUT", "3600"))
            ),
            security=SecurityConfig(
                rate_limit_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "60")),
                max_text_length=int(os.getenv("MAX_TEXT_LENGTH", "1000")),
                max_audio_duration=int(os.getenv("MAX_AUDIO_DURATION", "300")),
                allowed_origins=os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else None,
                enable_cors=os.getenv("ENABLE_CORS", "True").lower() == "true",
                csrf_protection=os.getenv("CSRF_PROTECTION", "True").lower() == "true"
            ),
            logging=LoggingConfig(
                level=os.getenv("LOG_LEVEL", "INFO"),
                log_dir=os.getenv("LOG_DIR", "logs"),
                max_log_size=int(os.getenv("MAX_LOG_SIZE", str(10 * 1024 * 1024))),
                backup_count=int(os.getenv("LOG_BACKUP_COUNT", "5")),
                enable_metrics=os.getenv("ENABLE_METRICS", "True").lower() == "true",
                metrics_retention_days=int(os.getenv("METRICS_RETENTION_DAYS", "30"))
            ),
            performance=PerformanceConfig(
                async_processing=os.getenv("ASYNC_PROCESSING", "True").lower() == "true",
                max_concurrent_requests=int(os.getenv("MAX_CONCURRENT_REQUESTS", "10")),
                request_timeout=int(os.getenv("REQUEST_TIMEOUT", "120")),
                cache_enabled=os.getenv("CACHE_ENABLED", "True").lower() == "true",
                cache_ttl=int(os.getenv("CACHE_TTL", "3600")),
                preload_models=os.getenv("PRELOAD_MODELS", "False").lower() == "true"
            ),
            app_name=os.getenv("APP_NAME", "Voice Synthesis Demo"),
            version=os.getenv("APP_VERSION", "1.0.0"),
            environment=os.getenv("ENVIRONMENT", "development"),
            timezone=os.getenv("TIMEZONE", "UTC")
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convertir configuración a diccionario"""
        return asdict(self)
    
    def to_json(self, indent: int = 2) -> str:
        """Convertir configuración a JSON"""
        return json.dumps(self.to_dict(), indent=indent, default=str)
    
    def save_to_file(self, filepath: str) -> None:
        """Guardar configuración a archivo JSON"""
        with open(filepath, 'w') as f:
            f.write(self.to_json())
    
    @classmethod
    def from_file(cls, filepath: str) -> "AppConfig":
        """Cargar configuración desde archivo JSON"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        return cls(
            elevenlabs=ElevenLabsConfig(**data['elevenlabs']),
            coqui=CoquiConfig(**data['coqui']),
            web=WebConfig(**data['web']),
            security=SecurityConfig(**data['security']),
            logging=LoggingConfig(**data['logging']),
            performance=PerformanceConfig(**data['performance']),
            app_name=data.get('app_name', 'Voice Synthesis Demo'),
            version=data.get('version', '1.0.0'),
            environment=data.get('environment', 'development'),
            timezone=data.get('timezone', 'UTC')
        )
    
    def validate(self) -> tuple[bool, list[str]]:
        """Validar configuración"""
        errors = []
        
        # Validar ElevenLabs
        if self.environment == "production" and not self.elevenlabs.api_key:
            errors.append("ElevenLabs API key is required in production")
        
        # Validar Web
        if not (1 <= self.web.port <= 65535):
            errors.append(f"Invalid port: {self.web.port}")
        
        if len(self.web.secret_key) < 16:
            errors.append("Secret key should be at least 16 characters")
        
        # Validar Security
        if self.security.max_text_length <= 0:
            errors.append("Max text length must be positive")
        
        if self.security.max_audio_duration <= 0:
            errors.append("Max audio duration must be positive")
        
        # Validar Performance
        if self.performance.max_concurrent_requests <= 0:
            errors.append("Max concurrent requests must be positive")
        
        return len(errors) == 0, errors
    
    def is_production(self) -> bool:
        """Verificar si está en modo producción"""
        return self.environment.lower() == "production"
    
    def is_development(self) -> bool:
        """Verificar si está en modo desarrollo"""
        return self.environment.lower() == "development"
    
    def get_elevenlabs_headers(self) -> Dict[str, str]:
        """Obtener headers para ElevenLabs API"""
        return {
            "xi-api-key": self.elevenlabs.api_key,
            "Content-Type": "application/json"
        }
    
    def get_allowed_file_extensions(self) -> set:
        """Obtener extensiones de archivo permitidas"""
        return set(self.web.allowed_extensions)
    
    def get_upload_path(self) -> Path:
        """Obtener ruta de uploads"""
        return Path(self.web.upload_folder)
    
    def ensure_directories(self) -> None:
        """Crear directorios necesarios"""
        directories = [
            self.web.upload_folder,
            self.logging.log_dir,
            self.coqui.cache_dir,
            "static/audio",
            "static/css",
            "static/js"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)


class ConfigManager:
    """Gestor de configuración singleton"""
    
    _instance: Optional[AppConfig] = None
    _config_file: Optional[str] = None
    
    @classmethod
    def get_config(cls, reload: bool = False) -> AppConfig:
        """Obtener instancia de configuración"""
        if cls._instance is None or reload:
            cls._instance = AppConfig.from_env()
            cls._instance.ensure_directories()
        
        return cls._instance
    
    @classmethod
    def load_from_file(cls, filepath: str) -> AppConfig:
        """Cargar configuración desde archivo"""
        cls._config_file = filepath
        cls._instance = AppConfig.from_file(filepath)
        cls._instance.ensure_directories()
        return cls._instance
    
    @classmethod
    def save_current_config(cls, filepath: str) -> None:
        """Guardar configuración actual"""
        if cls._instance:
            cls._instance.save_to_file(filepath)
    
    @classmethod
    def validate_current_config(cls) -> tuple[bool, list[str]]:
        """Validar configuración actual"""
        if cls._instance:
            return cls._instance.validate()
        return False, ["No configuration loaded"]


# Instancia global de configuración
config = ConfigManager.get_config()


def get_config() -> AppConfig:
    """Función de conveniencia para obtener configuración"""
    return ConfigManager.get_config()


def reload_config() -> AppConfig:
    """Función de conveniencia para recargar configuración"""
    return ConfigManager.get_config(reload=True)


if __name__ == "__main__":
    # Demo del sistema de configuración
    print("⚙️ Demo del sistema de configuración...")
    
    # Cargar configuración
    config = get_config()
    print(f"✅ Configuración cargada: {config.app_name} v{config.version}")
    print(f"🌍 Entorno: {config.environment}")
    
    # Validar configuración
    is_valid, errors = config.validate()
    if is_valid:
        print("✅ Configuración válida")
    else:
        print("❌ Errores de configuración:")
        for error in errors:
            print(f"   - {error}")
    
    # Mostrar configuración
    print("\n📋 Configuración actual:")
    print(f"   ElevenLabs API Key: {'Configurada' if config.elevenlabs.api_key else 'No configurada'}")
    print(f"   Puerto web: {config.web.port}")
    print(f"   Debug: {config.web.debug}")
    print(f"   Modelo Coqui: {config.coqui.default_model}")
    
    # Guardar configuración de ejemplo
    config.save_to_file("config_example.json")
    print("💾 Configuración de ejemplo guardada en 'config_example.json'")
    
    print("✅ Demo completado")
