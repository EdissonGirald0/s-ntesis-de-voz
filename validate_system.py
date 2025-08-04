#!/usr/bin/env python3
"""
Script de validación y diagnóstico del sistema de síntesis de voz
"""

import sys
import os
import subprocess
import importlib
import json
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any
import urllib.request
import socket
from datetime import datetime


class SystemValidator:
    """Validador del sistema de síntesis de voz"""
    
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'overall_status': 'unknown',
            'checks': {},
            'warnings': [],
            'errors': [],
            'recommendations': []
        }
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Ejecutar todas las validaciones"""
        print("🔍 Iniciando validación del sistema...")
        print("=" * 60)
        
        checks = [
            ("Python Environment", self.check_python_environment),
            ("System Resources", self.check_system_resources),
            ("Required Directories", self.check_directories),
            ("Virtual Environments", self.check_virtual_environments),
            ("Python Dependencies", self.check_dependencies),
            ("Configuration Files", self.check_configuration),
            ("ElevenLabs API", self.check_elevenlabs_api),
            ("Coqui TTS", self.check_coqui_tts),
            ("Web Application", self.check_web_application),
            ("Audio Capabilities", self.check_audio_capabilities),
            ("Network Connectivity", self.check_network),
            ("File Permissions", self.check_permissions)
        ]
        
        for check_name, check_function in checks:
            print(f"\n📋 {check_name}...")
            try:
                result = check_function()
                self.results['checks'][check_name] = result
                status_icon = "✅" if result['status'] == 'pass' else "❌" if result['status'] == 'fail' else "⚠️"
                print(f"   {status_icon} {result['message']}")
                
                if result.get('details'):
                    for detail in result['details']:
                        print(f"     • {detail}")
                
            except Exception as e:
                self.results['checks'][check_name] = {
                    'status': 'error',
                    'message': f"Error during check: {str(e)}",
                    'details': []
                }
                print(f"   ❌ Error: {str(e)}")
        
        self._calculate_overall_status()
        self._generate_recommendations()
        
        print("\n" + "=" * 60)
        print(f"🎯 Estado general: {self.results['overall_status'].upper()}")
        
        if self.results['warnings']:
            print(f"\n⚠️  Advertencias ({len(self.results['warnings'])}):")
            for warning in self.results['warnings']:
                print(f"   • {warning}")
        
        if self.results['errors']:
            print(f"\n❌ Errores ({len(self.results['errors'])}):")
            for error in self.results['errors']:
                print(f"   • {error}")
        
        if self.results['recommendations']:
            print(f"\n💡 Recomendaciones:")
            for rec in self.results['recommendations']:
                print(f"   • {rec}")
        
        return self.results
    
    def check_python_environment(self) -> Dict[str, Any]:
        """Verificar entorno Python"""
        details = []
        warnings = []
        
        # Versión de Python
        python_version = sys.version_info
        details.append(f"Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        if python_version < (3, 8):
            warnings.append("Python 3.8+ recomendado")
        
        # Información del sistema
        details.append(f"Plataforma: {sys.platform}")
        details.append(f"Ejecutable: {sys.executable}")
        
        return {
            'status': 'pass' if python_version >= (3, 8) else 'warning',
            'message': f"Python {python_version.major}.{python_version.minor} detectado",
            'details': details
        }
    
    def check_system_resources(self) -> Dict[str, Any]:
        """Verificar recursos del sistema"""
        details = []
        warnings = []
        
        try:
            import psutil
            
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            details.append(f"CPU: {cpu_percent}% utilizada")
            
            # Memoria
            memory = psutil.virtual_memory()
            memory_gb = memory.total / (1024**3)
            memory_percent = memory.percent
            details.append(f"Memoria: {memory_gb:.1f}GB total, {memory_percent}% utilizada")
            
            # Disco
            disk = psutil.disk_usage('/')
            disk_gb = disk.total / (1024**3)
            disk_percent = (disk.used / disk.total) * 100
            details.append(f"Disco: {disk_gb:.1f}GB total, {disk_percent:.1f}% utilizado")
            
            # Advertencias
            if memory_gb < 4:
                warnings.append("Se recomienda al menos 4GB de RAM")
            if disk_percent > 90:
                warnings.append("Espacio en disco bajo")
            
            status = 'warning' if warnings else 'pass'
            
        except ImportError:
            status = 'warning'
            details.append("psutil no disponible - información limitada")
        
        return {
            'status': status,
            'message': "Recursos del sistema verificados",
            'details': details
        }
    
    def check_directories(self) -> Dict[str, Any]:
        """Verificar directorios necesarios"""
        required_dirs = [
            'app',
            'templates',
            'static',
            'static/audio',
            'static/css',
            'static/js',
            'logs'
        ]
        
        missing_dirs = []
        for directory in required_dirs:
            if not Path(directory).exists():
                missing_dirs.append(directory)
        
        if missing_dirs:
            return {
                'status': 'fail',
                'message': f"{len(missing_dirs)} directorios faltantes",
                'details': [f"Falta: {d}" for d in missing_dirs]
            }
        
        return {
            'status': 'pass',
            'message': "Todos los directorios necesarios existen",
            'details': [f"✓ {d}" for d in required_dirs]
        }
    
    def check_virtual_environments(self) -> Dict[str, Any]:
        """Verificar entornos virtuales"""
        venvs = ['venv-elevenlabs', 'venv-coqui']
        details = []
        missing = []
        
        for venv in venvs:
            venv_path = Path(venv)
            if venv_path.exists():
                python_path = venv_path / 'bin' / 'python'
                if python_path.exists():
                    details.append(f"✓ {venv} - OK")
                else:
                    details.append(f"⚠ {venv} - Python ejecutable faltante")
                    missing.append(f"{venv}/bin/python")
            else:
                details.append(f"❌ {venv} - No existe")
                missing.append(venv)
        
        if missing:
            return {
                'status': 'fail',
                'message': f"Entornos virtuales incompletos",
                'details': details
            }
        
        return {
            'status': 'pass',
            'message': "Entornos virtuales configurados correctamente",
            'details': details
        }
    
    def check_dependencies(self) -> Dict[str, Any]:
        """Verificar dependencias Python"""
        dependencies = {
            'elevenlabs': ['flask', 'requests', 'python-dotenv'],
            'coqui': ['TTS', 'torch', 'torchaudio']
        }
        
        details = []
        errors = []
        
        for env_name, packages in dependencies.items():
            venv_python = Path(f'venv-{env_name}') / 'bin' / 'python'
            
            if not venv_python.exists():
                errors.append(f"Entorno {env_name} no encontrado")
                continue
            
            for package in packages:
                try:
                    result = subprocess.run(
                        [str(venv_python), '-c', f'import {package}; print({package}.__version__)'],
                        capture_output=True,
                        text=True,
                        timeout=10
                    )
                    
                    if result.returncode == 0:
                        version = result.stdout.strip()
                        details.append(f"✓ {env_name}: {package} v{version}")
                    else:
                        details.append(f"❌ {env_name}: {package} - Error de importación")
                        errors.append(f"{package} no funciona en {env_name}")
                
                except subprocess.TimeoutExpired:
                    details.append(f"⚠ {env_name}: {package} - Timeout")
                    errors.append(f"{package} timeout en {env_name}")
                except Exception as e:
                    details.append(f"❌ {env_name}: {package} - {str(e)}")
                    errors.append(f"{package} error en {env_name}")
        
        status = 'fail' if errors else 'pass'
        
        return {
            'status': status,
            'message': f"Dependencias verificadas ({'con errores' if errors else 'todas OK'})",
            'details': details
        }
    
    def check_configuration(self) -> Dict[str, Any]:
        """Verificar archivos de configuración"""
        config_files = {
            '.env': 'Configuración principal',
            'env.example': 'Plantilla de configuración',
            'requirements.txt': 'Dependencias Python',
            'setup_environments.py': 'Script de configuración'
        }
        
        details = []
        missing = []
        
        for filename, description in config_files.items():
            filepath = Path(filename)
            if filepath.exists():
                size = filepath.stat().st_size
                details.append(f"✓ {filename} ({size} bytes) - {description}")
            else:
                details.append(f"❌ {filename} - {description}")
                missing.append(filename)
        
        # Verificar configuración en .env si existe
        env_path = Path('.env')
        if env_path.exists():
            with open(env_path) as f:
                content = f.read()
                if 'ELEVENLABS_API_KEY' in content:
                    details.append("✓ Variable ELEVENLABS_API_KEY encontrada")
                else:
                    details.append("⚠ Variable ELEVENLABS_API_KEY no configurada")
        
        status = 'warning' if missing else 'pass'
        
        return {
            'status': status,
            'message': f"Configuración {'incompleta' if missing else 'completa'}",
            'details': details
        }
    
    def check_elevenlabs_api(self) -> Dict[str, Any]:
        """Verificar conectividad con ElevenLabs API"""
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            api_key = os.getenv('ELEVENLABS_API_KEY')
            
            if not api_key:
                return {
                    'status': 'warning',
                    'message': "API key de ElevenLabs no configurada",
                    'details': ["Configura ELEVENLABS_API_KEY en .env para usar ElevenLabs"]
                }
            
            # Test básico de conectividad
            try:
                import requests
                response = requests.get(
                    "https://api.elevenlabs.io/v1/voices",
                    headers={"xi-api-key": api_key},
                    timeout=10
                )
                
                if response.status_code == 200:
                    voices = response.json()
                    return {
                        'status': 'pass',
                        'message': "ElevenLabs API conectada correctamente",
                        'details': [f"✓ {len(voices.get('voices', []))} voces disponibles"]
                    }
                else:
                    return {
                        'status': 'fail',
                        'message': f"Error ElevenLabs API: {response.status_code}",
                        'details': [response.text[:200]]
                    }
            
            except requests.RequestException as e:
                return {
                    'status': 'fail',
                    'message': f"Error de conectividad ElevenLabs: {str(e)}",
                    'details': ["Verifica tu conexión a internet"]
                }
        
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error verificando ElevenLabs: {str(e)}",
                'details': []
            }
    
    def check_coqui_tts(self) -> Dict[str, Any]:
        """Verificar Coqui TTS"""
        venv_python = Path('venv-coqui/bin/python')
        
        if not venv_python.exists():
            return {
                'status': 'fail',
                'message': "Entorno Coqui no encontrado",
                'details': ["Ejecuta setup_environments.py para configurar Coqui"]
            }
        
        try:
            # Test de importación
            result = subprocess.run([
                str(venv_python), '-c',
                'from TTS.api import TTS; print("TTS importado correctamente")'
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                return {
                    'status': 'pass',
                    'message': "Coqui TTS funcional",
                    'details': ["✓ TTS se importa correctamente"]
                }
            else:
                return {
                    'status': 'fail',
                    'message': "Error en Coqui TTS",
                    'details': [result.stderr[:200] if result.stderr else "Error desconocido"]
                }
        
        except subprocess.TimeoutExpired:
            return {
                'status': 'warning',
                'message': "Coqui TTS timeout (puede ser lento la primera vez)",
                'details': ["Los modelos se descargan en el primer uso"]
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Error verificando Coqui: {str(e)}",
                'details': []
            }
    
    def check_web_application(self) -> Dict[str, Any]:
        """Verificar aplicación web"""
        webapp_path = Path('app/webapp_working.py')
        
        if not webapp_path.exists():
            return {
                'status': 'fail',
                'message': "Aplicación web no encontrada",
                'details': ["app/webapp_working.py faltante"]
            }
        
        # Verificar templates
        template_path = Path('templates/index.html')
        if not template_path.exists():
            return {
                'status': 'fail',
                'message': "Template principal faltante",
                'details': ["templates/index.html no encontrado"]
            }
        
        # Test de sintaxis
        try:
            with open(webapp_path) as f:
                compile(f.read(), webapp_path, 'exec')
            
            return {
                'status': 'pass',
                'message': "Aplicación web OK",
                'details': ["✓ Sintaxis correcta", "✓ Template principal existe"]
            }
        
        except SyntaxError as e:
            return {
                'status': 'fail',
                'message': f"Error de sintaxis en webapp: {str(e)}",
                'details': [f"Línea {e.lineno}: {e.text}"]
            }
    
    def check_audio_capabilities(self) -> Dict[str, Any]:
        """Verificar capacidades de audio"""
        details = []
        
        # Verificar librerías de audio
        audio_libs = ['sounddevice', 'soundfile', 'librosa', 'numpy']
        missing = []
        
        for lib in audio_libs:
            try:
                __import__(lib)
                details.append(f"✓ {lib} disponible")
            except ImportError:
                details.append(f"❌ {lib} faltante")
                missing.append(lib)
        
        if missing:
            return {
                'status': 'warning',
                'message': f"Librerías de audio faltantes: {', '.join(missing)}",
                'details': details
            }
        
        return {
            'status': 'pass',
            'message': "Capacidades de audio completas",
            'details': details
        }
    
    def check_network(self) -> Dict[str, Any]:
        """Verificar conectividad de red"""
        details = []
        
        # Test de conectividad básica
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=5)
            details.append("✓ Conectividad a internet")
        except OSError:
            details.append("❌ Sin conectividad a internet")
            return {
                'status': 'fail',
                'message': "Sin conectividad a internet",
                'details': details
            }
        
        # Test de ElevenLabs
        try:
            response = urllib.request.urlopen("https://api.elevenlabs.io", timeout=10)
            details.append("✓ ElevenLabs API accesible")
        except Exception:
            details.append("❌ ElevenLabs API no accesible")
        
        return {
            'status': 'pass',
            'message': "Conectividad de red verificada",
            'details': details
        }
    
    def check_permissions(self) -> Dict[str, Any]:
        """Verificar permisos de archivos"""
        details = []
        issues = []
        
        # Verificar permisos de escritura en directorios importantes
        write_dirs = ['static', 'logs', '.']
        
        for directory in write_dirs:
            dir_path = Path(directory)
            if dir_path.exists():
                if os.access(directory, os.W_OK):
                    details.append(f"✓ Escritura en {directory}")
                else:
                    details.append(f"❌ Sin permisos de escritura en {directory}")
                    issues.append(directory)
        
        # Verificar permisos de ejecución
        exec_files = ['setup_environments.py']
        for filename in exec_files:
            filepath = Path(filename)
            if filepath.exists():
                if os.access(filename, os.X_OK):
                    details.append(f"✓ Ejecución en {filename}")
                else:
                    details.append(f"⚠ Sin permisos de ejecución en {filename}")
        
        status = 'fail' if issues else 'pass'
        
        return {
            'status': status,
            'message': f"Permisos {'OK' if not issues else 'con problemas'}",
            'details': details
        }
    
    def _calculate_overall_status(self):
        """Calcular estado general"""
        statuses = [check['status'] for check in self.results['checks'].values()]
        
        if 'fail' in statuses or 'error' in statuses:
            self.results['overall_status'] = 'fail'
        elif 'warning' in statuses:
            self.results['overall_status'] = 'warning'
        else:
            self.results['overall_status'] = 'pass'
    
    def _generate_recommendations(self):
        """Generar recomendaciones basadas en los resultados"""
        recommendations = []
        
        # Análisis de errores comunes
        for check_name, result in self.results['checks'].items():
            if result['status'] in ['fail', 'error']:
                if 'virtual' in check_name.lower():
                    recommendations.append("Ejecuta 'python3 setup_environments.py' para configurar entornos virtuales")
                elif 'dependencies' in check_name.lower():
                    recommendations.append("Instala las dependencias faltantes en los entornos virtuales correspondientes")
                elif 'elevenlabs' in check_name.lower():
                    recommendations.append("Configura tu API key de ElevenLabs en el archivo .env")
                elif 'directories' in check_name.lower():
                    recommendations.append("Crea los directorios faltantes: mkdir -p static/audio static/css static/js logs")
        
        # Recomendaciones generales
        if self.results['overall_status'] == 'warning':
            recommendations.append("Revisa las advertencias y considera aplicar las mejoras sugeridas")
        
        if self.results['overall_status'] == 'pass':
            recommendations.append("¡Sistema listo! Puedes iniciar la aplicación con 'python app/webapp_working.py'")
        
        self.results['recommendations'] = list(set(recommendations))  # Eliminar duplicados
    
    def save_report(self, filename: str = None):
        """Guardar reporte de validación"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"system_validation_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\n💾 Reporte guardado en: {filename}")


def main():
    """Función principal"""
    validator = SystemValidator()
    results = validator.run_all_checks()
    
    # Guardar reporte
    validator.save_report()
    
    # Código de salida basado en el estado
    if results['overall_status'] == 'fail':
        sys.exit(1)
    elif results['overall_status'] == 'warning':
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
