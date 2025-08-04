#!/usr/bin/env python3
"""
Sistema de logging centralizado para la aplicación de síntesis de voz
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
import json
import traceback


class VoiceSynthesisLogger:
    """Logger personalizado para la aplicación de síntesis de voz"""
    
    def __init__(self, name="voice_synthesis", log_dir="logs"):
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        
        # Configurar logger principal
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Evitar duplicar handlers
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """Configurar diferentes handlers para logging"""
        
        # Formatter personalizado
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s | %(levelname)s | %(module)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Handler para consola (desarrollo)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        
        # Handler para archivo general con rotación
        file_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / "app.log",
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        
        # Handler para errores críticos
        error_handler = logging.handlers.RotatingFileHandler(
            self.log_dir / "errors.log",
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        
        # Handler para métricas y analytics
        metrics_formatter = logging.Formatter('%(asctime)s | %(message)s')
        metrics_handler = logging.handlers.TimedRotatingFileHandler(
            self.log_dir / "metrics.log",
            when='midnight',
            backupCount=30
        )
        metrics_handler.setLevel(logging.INFO)
        metrics_handler.setFormatter(metrics_formatter)
        
        # Agregar handlers al logger
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(error_handler)
        
        # Logger separado para métricas
        self.metrics_logger = logging.getLogger(f"{self.name}.metrics")
        self.metrics_logger.setLevel(logging.INFO)
        self.metrics_logger.addHandler(metrics_handler)
        self.metrics_logger.propagate = False
    
    def info(self, message, **kwargs):
        """Log mensaje informativo"""
        self.logger.info(self._format_message(message, **kwargs))
    
    def debug(self, message, **kwargs):
        """Log mensaje de debug"""
        self.logger.debug(self._format_message(message, **kwargs))
    
    def warning(self, message, **kwargs):
        """Log mensaje de advertencia"""
        self.logger.warning(self._format_message(message, **kwargs))
    
    def error(self, message, exception=None, **kwargs):
        """Log mensaje de error"""
        if exception:
            self.logger.error(
                f"{self._format_message(message, **kwargs)} | Exception: {str(exception)}"
            )
            self.logger.debug(traceback.format_exc())
        else:
            self.logger.error(self._format_message(message, **kwargs))
    
    def critical(self, message, exception=None, **kwargs):
        """Log mensaje crítico"""
        if exception:
            self.logger.critical(
                f"{self._format_message(message, **kwargs)} | Exception: {str(exception)}"
            )
            self.logger.debug(traceback.format_exc())
        else:
            self.logger.critical(self._format_message(message, **kwargs))
    
    def metric(self, event, data=None, **kwargs):
        """Log métrica o evento de analytics"""
        metric_data = {
            'timestamp': datetime.now().isoformat(),
            'event': event,
            'data': data or {},
            **kwargs
        }
        self.metrics_logger.info(json.dumps(metric_data))
    
    def tts_request(self, engine, text_length, success=True, duration=None, **kwargs):
        """Log específico para solicitudes TTS"""
        self.metric('tts_request', {
            'engine': engine,
            'text_length': text_length,
            'success': success,
            'duration_seconds': duration,
            **kwargs
        })
    
    def voice_cloning_request(self, engine, audio_file_size, text_length, success=True, duration=None, **kwargs):
        """Log específico para clonación de voz"""
        self.metric('voice_cloning_request', {
            'engine': engine,
            'audio_file_size': audio_file_size,
            'text_length': text_length,
            'success': success,
            'duration_seconds': duration,
            **kwargs
        })
    
    def api_error(self, api_name, status_code, error_message, **kwargs):
        """Log específico para errores de API"""
        self.error(f"API Error - {api_name}", **{
            'status_code': status_code,
            'error_message': error_message,
            **kwargs
        })
    
    def user_action(self, action, user_agent=None, ip=None, **kwargs):
        """Log acción del usuario"""
        self.metric('user_action', {
            'action': action,
            'user_agent': user_agent,
            'ip': ip,
            **kwargs
        })
    
    def system_health(self, **kwargs):
        """Log estado del sistema"""
        self.metric('system_health', kwargs)
    
    def _format_message(self, message, **kwargs):
        """Formatear mensaje con contexto adicional"""
        if kwargs:
            context = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
            return f"{message} | {context}"
        return message


# Instancia global del logger
logger = VoiceSynthesisLogger()

# Funciones de conveniencia
def log_info(message, **kwargs):
    logger.info(message, **kwargs)

def log_debug(message, **kwargs):
    logger.debug(message, **kwargs)

def log_warning(message, **kwargs):
    logger.warning(message, **kwargs)

def log_error(message, exception=None, **kwargs):
    logger.error(message, exception=exception, **kwargs)

def log_critical(message, exception=None, **kwargs):
    logger.critical(message, exception=exception, **kwargs)

def log_metric(event, data=None, **kwargs):
    logger.metric(event, data, **kwargs)

def log_tts_request(engine, text_length, success=True, duration=None, **kwargs):
    logger.tts_request(engine, text_length, success, duration, **kwargs)

def log_voice_cloning_request(engine, audio_file_size, text_length, success=True, duration=None, **kwargs):
    logger.voice_cloning_request(engine, audio_file_size, text_length, success, duration, **kwargs)

def log_api_error(api_name, status_code, error_message, **kwargs):
    logger.api_error(api_name, status_code, error_message, **kwargs)

def log_user_action(action, user_agent=None, ip=None, **kwargs):
    logger.user_action(action, user_agent, ip, **kwargs)

def log_system_health(**kwargs):
    logger.system_health(**kwargs)


class LoggingMiddleware:
    """Middleware para logging automático de requests"""
    
    def __init__(self, app):
        self.app = app
        self.logger = VoiceSynthesisLogger("middleware")
    
    def __call__(self, environ, start_response):
        # Log request
        method = environ.get('REQUEST_METHOD')
        path = environ.get('PATH_INFO')
        user_agent = environ.get('HTTP_USER_AGENT', 'Unknown')
        remote_addr = environ.get('REMOTE_ADDR', 'Unknown')
        
        start_time = datetime.now()
        
        self.logger.info(f"Request started: {method} {path}", **{
            'user_agent': user_agent,
            'remote_addr': remote_addr
        })
        
        def new_start_response(status, response_headers, exc_info=None):
            # Log response
            duration = (datetime.now() - start_time).total_seconds()
            status_code = int(status.split(' ')[0])
            
            self.logger.info(f"Request completed: {method} {path}", **{
                'status_code': status_code,
                'duration_seconds': duration,
                'remote_addr': remote_addr
            })
            
            # Log métrica
            self.logger.metric('http_request', {
                'method': method,
                'path': path,
                'status_code': status_code,
                'duration_seconds': duration,
                'user_agent': user_agent,
                'remote_addr': remote_addr
            })
            
            return start_response(status, response_headers, exc_info)
        
        return self.app(environ, new_start_response)


def setup_error_handling(app):
    """Configurar manejo de errores global para Flask"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        log_warning("Page not found", path=request.path if 'request' in globals() else 'unknown')
        return "Página no encontrada", 404
    
    @app.errorhandler(500)
    def internal_error(error):
        log_error("Internal server error", exception=error)
        return "Error interno del servidor", 500
    
    @app.errorhandler(Exception)
    def unhandled_exception(error):
        log_critical("Unhandled exception", exception=error)
        return "Error inesperado", 500


if __name__ == "__main__":
    # Demo del sistema de logging
    print("🔍 Demo del sistema de logging...")
    
    # Logging básico
    log_info("Aplicación iniciada", version="1.0.0")
    log_debug("Modo debug activado")
    log_warning("Configuración de prueba detectada")
    
    # Logging de métricas
    log_tts_request("elevenlabs", 50, success=True, duration=2.5)
    log_voice_cloning_request("coqui", 1024000, 30, success=False)
    
    # Logging de errores
    try:
        raise ValueError("Error de prueba")
    except Exception as e:
        log_error("Error en procesamiento", exception=e, module="test")
    
    # Métricas personalizadas
    log_metric("user_registration", {"user_id": "123", "plan": "free"})
    log_system_health(cpu_usage=45.2, memory_usage=67.8, disk_usage=23.1)
    
    print("✅ Demo completado. Revisa los archivos en la carpeta 'logs/'")
