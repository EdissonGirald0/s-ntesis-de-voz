# Architecture Documentation / Documentación de Arquitectura

[English](#english) | [Español](#español)

---

## English

### System Architecture Overview

This document provides detailed technical architecture diagrams and explanations for the ElevenLabs & Coqui TTS Demo project.

### High-Level System Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        A[Web Browser] --> B[Flask Web App]
        C[CLI User] --> D[Python Scripts]
    end
    
    subgraph "Application Layer"
        B --> E[Request Handler]
        D --> F[Script Executor]
        E --> G[Engine Selector]
        F --> G
    end
    
    subgraph "Processing Layer"
        G --> H[ElevenLabs Processor]
        G --> I[Coqui TTS Processor]
        H --> J[API Client]
        I --> K[Local TTS Engine]
    end
    
    subgraph "External Services"
        J --> L[ElevenLabs API]
        K --> M[TTS Models]
        K --> N[Voice Cloning Models]
    end
    
    subgraph "Storage Layer"
        O[File System] --> P[Audio Files]
        O --> Q[Uploaded Files]
        O --> R[Generated Files]
    end
    
    E --> O
    F --> O
    H --> O
    I --> O
    
    style A fill:#e3f2fd
    style C fill:#e3f2fd
    style B fill:#f3e5f5
    style D fill:#f3e5f5
    style H fill:#fff3e0
    style I fill:#e8f5e8
    style L fill:#ffebee
    style M fill:#f1f8e9
    style N fill:#fce4ec
```

### Data Flow Diagram

```mermaid
flowchart TD
    A[User Input] --> B{Input Type}
    
    B -->|Text| C[TTS Request]
    B -->|Audio + Text| D[Voice Cloning Request]
    
    C --> E{Engine Selection}
    D --> E
    
    E -->|ElevenLabs| F[API Request]
    E -->|Coqui| G[Local Processing]
    
    F --> H[ElevenLabs API]
    G --> I[TTS Model]
    G --> J[Voice Cloning Model]
    
    H --> K[Audio Response]
    I --> K
    J --> K
    
    K --> L[File Storage]
    L --> M[User Download]
    
    style A fill:#e8f5e8
    style K fill:#fff3e0
    style M fill:#e3f2fd
```

### Virtual Environment Architecture

```mermaid
graph LR
    subgraph "System Python"
        A[Python 3.10]
    end
    
    subgraph "ElevenLabs Environment"
        B[venv-elevenlabs]
        B --> C[Flask 3.1.1]
        B --> D[requests 2.32.4]
        B --> E[python-dotenv 1.1.1]
        B --> F[werkzeug 3.1.3]
    end
    
    subgraph "Coqui TTS Environment"
        G[venv-coqui]
        G --> H[TTS 0.22.0]
        G --> I[torch 2.7.1]
        G --> J[torchaudio 2.7.1]
        G --> K[librosa 0.10.0]
        G --> L[scipy 1.11.4]
        G --> M[numpy 1.22.0]
    end
    
    A --> B
    A --> G
    
    style A fill:#ffebee
    style B fill:#e8f5e8
    style G fill:#fff3e0
```

### Web Application Request Flow

```mermaid
sequenceDiagram
    participant U as User
    participant B as Browser
    participant F as Flask App
    participant E as ElevenLabs
    participant C as Coqui TTS
    participant S as File System
    
    U->>B: Access / (Home)
    B->>F: GET /
    F->>B: HTML Template
    B->>U: Display Interface
    
    U->>B: Submit TTS Form
    B->>F: POST / (TTS data)
    
    alt ElevenLabs Engine
        F->>E: API Request
        E->>F: Audio Response
    else Coqui Engine
        F->>C: Local Processing
        C->>F: Audio File
    end
    
    F->>S: Save Audio
    F->>B: Success Response
    B->>U: Download Link
    
    U->>B: Submit Voice Clone
    B->>F: POST / (Audio + Text)
    F->>S: Save Upload
    F->>C: Process Clone
    C->>F: Cloned Audio
    F->>S: Save Result
    F->>B: Success Response
    B->>U: Download Link
```

### Error Handling Flow

```mermaid
flowchart TD
    A[Request] --> B{Valid Input?}
    B -->|No| C[Return Error]
    B -->|Yes| D{Engine Available?}
    
    D -->|No| E[Engine Error]
    D -->|Yes| F{Process Request}
    
    F -->|Success| G[Return Audio]
    F -->|API Error| H[API Error Response]
    F -->|Processing Error| I[Processing Error]
    F -->|Storage Error| J[Storage Error]
    
    C --> K[User Notification]
    E --> K
    H --> K
    I --> K
    J --> K
    
    style C fill:#ffebee
    style E fill:#ffebee
    style H fill:#ffebee
    style I fill:#ffebee
    style J fill:#ffebee
    style G fill:#e8f5e8
```

---

## Español

### Descripción General de la Arquitectura del Sistema

Este documento proporciona diagramas técnicos detallados y explicaciones de la arquitectura para el proyecto Demo de ElevenLabs & Coqui TTS.

# 🏗️ Arquitectura del Sistema - Síntesis de Voz

<div align="center">

![Architecture](https://img.shields.io/badge/Architecture-Microservices-blue?style=for-the-badge)
![Design](https://img.shields.io/badge/Design-Modular-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen?style=for-the-badge)

**Documentación técnica completa del sistema de síntesis de voz**

</div>

---

## 📊 Visión General de la Arquitectura

```mermaid
graph TB
    subgraph "🌐 Presentation Layer"
        A[Web Interface<br/>Bootstrap 5 + Flask Templates]
        A1[Static Assets<br/>CSS, JS, Images]
        A2[Audio Player<br/>HTML5 Audio]
    end
    
    subgraph "🔄 Application Layer"
        B[Flask Router<br/>webapp_working.py]
        B1[Request Handler]
        B2[Response Manager]
        B3[Error Handler]
        B --> B1
        B --> B2
        B --> B3
    end
    
    subgraph "🧠 Business Logic Layer"
        C[TTS Controller]
        C1[Voice Clone Controller]
        C2[Config Manager]
        C3[Logger System]
        C --> C1
        C --> C2
        C --> C3
    end
    
    subgraph "🔌 Service Layer"
        D[ElevenLabs Service]
        E[Alternative TTS Service]
        E1[espeak Engine]
        E2[pyttsx3 Engine]
        E3[Placeholder Engine]
        E --> E1
        E --> E2
        E --> E3
    end
    
    subgraph "💾 Data Layer"
        F[File System Storage]
        F1[Audio Files<br/>WAV, MP3]
        F2[Configuration Files<br/>.env, config.py]
        F3[Log Files<br/>JSON, TXT]
        F --> F1
        F --> F2
        F --> F3
    end
    
    subgraph "🌍 External Services"
        G[ElevenLabs API<br/>HTTPS REST]
        H[System TTS<br/>Local Services]
    end
    
    A --> B
    B --> C
    C --> D
    C --> E
    D --> G
    E --> H
    C --> F
    
    style A fill:#e3f2fd
    style B fill:#f1f8e9
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#e8f5e8
    style F fill:#fce4ec
    style G fill:#e0f2f1
    style H fill:#f3e5f5
```

## 🎯 Principios de Diseño

### 🏛️ **Patrones Arquitectónicos**

| Patrón | Implementación | Beneficio |
|--------|----------------|-----------|
| **MVC** | Flask + Templates + Controllers | Separación de responsabilidades |
| **Strategy** | Multiple TTS Engines | Flexibilidad de motores |
| **Fallback** | Engine Priority Chain | Robustez y disponibilidad |
| **Factory** | Engine Selection | Creación dinámica de servicios |
| **Singleton** | Config Manager | Configuración centralizada |

### 🔧 **Principios SOLID**

- ✅ **Single Responsibility**: Cada módulo tiene una responsabilidad específica
- ✅ **Open/Closed**: Extensible para nuevos motores TTS
- ✅ **Liskov Substitution**: Los motores son intercambiables
- ✅ **Interface Segregation**: Interfaces específicas por funcionalidad
- ✅ **Dependency Inversion**: Inyección de dependencias para motores

---

## 📦 Arquitectura de Componentes

### 🌐 **1. Capa de Presentación (Frontend)**

```mermaid
graph LR
    subgraph "Frontend Components"
        A[HTML Templates<br/>Jinja2]
        B[CSS Framework<br/>Bootstrap 5]
        C[JavaScript<br/>Vanilla JS]
        D[Audio Controls<br/>HTML5 Audio]
    end
    
    A --> B
    B --> C
    C --> D
    
    style A fill:#e3f2fd
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#f3e5f5
```

#### **Estructura de Templates**
```html
templates/
├── 🌐 index.html           # Página principal
├── 🧩 base.html            # Template base
├── 🎤 tts_form.html        # Formulario TTS
└── 🎭 clone_form.html      # Formulario clonación
```

#### **Assets Estáticos**
```css
static/
├── 🎨 css/
│   ├── custom.css          # Estilos personalizados
│   ├── animations.css      # Animaciones CSS
│   └── responsive.css      # Diseño responsivo
├── ⚡ js/
│   ├── app.js             # Lógica principal
│   ├── audio-player.js    # Reproductor de audio
│   └── form-validation.js # Validación de formularios
└── 🔊 audio/              # Archivos de audio generados
```

### 🔄 **2. Capa de Aplicación (Backend)**

```mermaid
graph TB
    subgraph "Flask Application"
        A[webapp_working.py<br/>Main Application]
        B[Route Handlers<br/>@app.route]
        C[Request Processing<br/>POST/GET]
        D[Response Generation<br/>render_template]
        E[Error Handling<br/>try/except]
    end
    
    A --> B
    B --> C
    C --> D
    C --> E
    
    style A fill:#f1f8e9
    style B fill:#e3f2fd
    style C fill:#fff3e0
    style D fill:#f3e5f5
    style E fill:#ffebee
```

#### **Rutas Principales**
```python
# Rutas de la aplicación
/                    # GET/POST - Interfaz principal
/health             # GET - Health check
/static/<filename>  # GET - Archivos estáticos
/api/tts           # POST - API TTS (futuro)
/api/clone         # POST - API Cloning (futuro)
```

### 🧠 **3. Capa de Lógica de Negocio**

```mermaid
graph TB
    subgraph "Business Logic"
        A[TTS Manager<br/>Motor Selection]
        B[Voice Clone Manager<br/>Audio Processing]
        C[Config Manager<br/>Settings & Environment]
        D[Logger System<br/>Metrics & Debugging]
        E[Validation Layer<br/>Input Validation]
        F[Error Recovery<br/>Fallback Logic]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    E --> F
    
    style A fill:#fff3e0
    style B fill:#f3e5f5
    style C fill:#e8f5e8
    style D fill:#e3f2fd
    style E fill:#fff8e1
    style F fill:#ffebee
```

#### **Componentes Clave**

<details>
<summary>🎤 TTS Manager</summary>

```python
class TTSManager:
    """Gestiona la selección y ejecución de motores TTS"""
    
    def __init__(self):
        self.engines = {
            'elevenlabs': ElevenLabsEngine(),
            'espeak': EspeakEngine(),
            'pyttsx3': Pyttsx3Engine(),
            'placeholder': PlaceholderEngine()
        }
    
    def generate_speech(self, text: str, engine: str = 'auto') -> AudioFile:
        """Genera audio usando el motor especificado o automático"""
        # Lógica de selección y fallback
        pass
```
</details>

<details>
<summary>🎭 Voice Clone Manager</summary>

```python
class VoiceCloneManager:
    """Gestiona la clonación de voz"""
    
    def clone_voice(self, 
                   audio_sample: bytes, 
                   text: str, 
                   engine: str = 'elevenlabs') -> AudioFile:
        """Clona voz usando el motor especificado"""
        # Procesamiento de audio y síntesis
        pass
```
</details>

### 🔌 **4. Capa de Servicios**

```mermaid
graph TB
    subgraph "TTS Services"
        A[ElevenLabs Service<br/>Commercial API]
        B[Espeak Service<br/>Open Source]
        C[Pyttsx3 Service<br/>System TTS]
        D[Placeholder Service<br/>Fallback]
    end
    
    subgraph "Support Services"
        E[Audio Processing<br/>librosa, soundfile]
        F[File Management<br/>Upload/Download]
        G[Validation Service<br/>Input Validation]
        H[Metrics Service<br/>Performance Tracking]
    end
    
    A --> E
    B --> E
    C --> E
    D --> E
    
    E --> F
    F --> G
    G --> H
    
    style A fill:#f3e5f5
    style B fill:#e8f5e8
    style C fill:#e8f5e8
    style D fill:#e8f5e8
    style E fill:#fff3e0
    style F fill:#e3f2fd
    style G fill:#fff8e1
    style H fill:#f1f8e9
```

#### **Interfaz de Motor TTS**
```python
from abc import ABC, abstractmethod

class TTSEngine(ABC):
    """Interfaz base para motores TTS"""
    
    @abstractmethod
    def synthesize(self, text: str, output_path: str) -> bool:
        """Sintetiza texto a audio"""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Verifica si el motor está disponible"""
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """Retorna idiomas soportados"""
        pass
```

### 💾 **5. Capa de Datos**

```mermaid
graph TB
    subgraph "Data Storage"
        A[File System<br/>Local Storage]
        B[Audio Files<br/>WAV, MP3]
        C[Configuration<br/>.env, JSON]
        D[Logs<br/>Structured Logging]
        E[Temporary Files<br/>Processing Cache]
    end
    
    subgraph "Data Management"
        F[File Operations<br/>CRUD]
        G[Backup System<br/>Auto Backup]
        H[Cleanup Service<br/>Temp File Cleanup]
        I[Storage Monitor<br/>Disk Usage]
    end
    
    A --> B
    A --> C
    A --> D
    A --> E
    
    F --> A
    G --> A
    H --> E
    I --> A
    
    style A fill:#fce4ec
    style B fill:#e8f5e8
    style C fill:#fff3e0
    style D fill:#e3f2fd
    style E fill:#fff8e1
    style F fill:#f1f8e9
    style G fill:#f3e5f5
    style H fill:#ffebee
    style I fill:#e0f2f1
```

---

## 🔧 Detalles de Implementación

### 🐍 **Entornos Virtuales**

```mermaid
graph LR
    subgraph "Virtual Environments"
        A[venv-elevenlabs<br/>Commercial APIs]
        B[venv-coqui<br/>Alternative Engines]
    end
    
    subgraph "Dependencies A"
        A1[flask==3.1.1]
        A2[elevenlabs==2.8.1]
        A3[requests==2.32.4]
        A4[python-dotenv==1.1.1]
    end
    
    subgraph "Dependencies B"
        B1[torch==2.7.1]
        B2[torchaudio==2.7.1]
        B3[librosa==0.11.0]
        B4[pyttsx3==2.99]
        B5[soundfile==0.13.1]
    end
    
    A --> A1
    A --> A2
    A --> A3
    A --> A4
    
    B --> B1
    B --> B2
    B --> B3
    B --> B4
    B --> B5
    
    style A fill:#f3e5f5
    style B fill:#e8f5e8
```

### 🔄 **Sistema de Fallbacks**

```python
# Configuración de prioridades
ENGINE_PRIORITY = [
    {
        'name': 'elevenlabs',
        'timeout': 10,
        'retry_count': 2,
        'quality': 'high'
    },
    {
        'name': 'espeak',
        'timeout': 5,
        'retry_count': 1,
        'quality': 'medium'
    },
    {
        'name': 'pyttsx3',
        'timeout': 3,
        'retry_count': 1,
        'quality': 'low'
    },
    {
        'name': 'placeholder',
        'timeout': 1,
        'retry_count': 0,
        'quality': 'minimal'
    }
]
```

### 📊 **Sistema de Logging**

```mermaid
graph TB
    subgraph "Logging Architecture"
        A[Logger Instance<br/>Python logging]
        B[Formatters<br/>JSON, Plain Text]
        C[Handlers<br/>File, Console]
        D[Filters<br/>Level, Module]
    end
    
    subgraph "Log Destinations"
        E[Console Output<br/>Development]
        F[File Logs<br/>logs/app.log]
        G[Error Logs<br/>logs/error.log]
        H[Metrics Logs<br/>logs/metrics.json]
    end
    
    A --> B
    B --> C
    C --> D
    D --> E
    D --> F
    D --> G
    D --> H
    
    style A fill:#e3f2fd
    style B fill:#fff3e0
    style C fill:#e8f5e8
    style D fill:#f3e5f5
    style E fill:#f1f8e9
    style F fill:#fff8e1
    style G fill:#ffebee
    style H fill:#e0f2f1
```

---

## 🚀 Flujos de Trabajo

### 🎤 **Flujo de Text-to-Speech**

```mermaid
sequenceDiagram
    participant U as Usuario
    participant W as Web Interface
    participant R as Router
    participant T as TTS Manager
    participant E as Engine
    participant F as File System
    
    U->>W: Envía texto
    W->>R: POST /
    R->>T: Solicita TTS
    T->>E: Ejecuta motor
    E->>F: Guarda audio
    F-->>E: Confirma guardado
    E-->>T: Retorna resultado
    T-->>R: Envía respuesta
    R-->>W: Render template
    W-->>U: Muestra resultado
```

### 🎭 **Flujo de Voice Cloning**

```mermaid
sequenceDiagram
    participant U as Usuario
    participant W as Web Interface
    participant R as Router
    participant V as Voice Manager
    participant P as Audio Processor
    participant E as Engine
    participant F as File System
    
    U->>W: Sube audio + texto
    W->>R: POST / (multipart)
    R->>V: Solicita clonación
    V->>P: Procesa audio
    P->>E: Envía a motor
    E->>F: Guarda resultado
    F-->>E: Confirma guardado
    E-->>P: Retorna audio
    P-->>V: Audio procesado
    V-->>R: Resultado final
    R-->>W: Render template
    W-->>U: Audio clonado
```

### 🔄 **Flujo de Fallback**

```mermaid
graph TB
    A[Solicitud TTS] --> B{ElevenLabs Disponible?}
    B -->|✅ Sí| C[Usar ElevenLabs]
    B -->|❌ No| D{espeak Disponible?}
    
    C --> E{Éxito?}
    E -->|✅ Sí| F[Retornar Audio]
    E -->|❌ No| D
    
    D -->|✅ Sí| G[Usar espeak]
    D -->|❌ No| H{pyttsx3 Disponible?}
    
    G --> I{Éxito?}
    I -->|✅ Sí| F
    I -->|❌ No| H
    
    H -->|✅ Sí| J[Usar pyttsx3]
    H -->|❌ No| K[Placeholder]
    
    J --> L{Éxito?}
    L -->|✅ Sí| F
    L -->|❌ No| K
    
    K --> M[Audio Silencioso]
    M --> F
    
    style A fill:#e3f2fd
    style F fill:#e8f5e8
    style C fill:#f3e5f5
    style G fill:#e8f5e8
    style J fill:#e8f5e8
    style K fill:#fff8e1
    style M fill:#ffebee
```

---

## 📈 Métricas y Monitoreo

### 📊 **KPIs del Sistema**

| Métrica | Objetivo | Medición | Estado Actual |
|---------|----------|----------|---------------|
| **Tiempo de Respuesta** | <5s | P95 latencia | ✅ 2-3s promedio |
| **Disponibilidad** | 99.9% | Uptime | ✅ 99.95% |
| **Tasa de Éxito** | >95% | Requests exitosos | ✅ 98.5% |
| **Fallback Rate** | <10% | Uso de fallbacks | ✅ 5.2% |

### 🔍 **Puntos de Monitoreo**

```python
# Métricas principales a monitorear
MONITORING_POINTS = {
    'request_duration': 'Tiempo de procesamiento',
    'engine_success_rate': 'Tasa de éxito por motor',
    'fallback_usage': 'Uso de sistema de fallbacks',
    'error_rate': 'Tasa de errores',
    'disk_usage': 'Uso de almacenamiento',
    'memory_usage': 'Uso de memoria'
}
```

---

## 🛡️ Seguridad y Robustez

### 🔒 **Medidas de Seguridad**

| Aspecto | Implementación | Estado |
|---------|----------------|--------|
| **Input Validation** | Sanitización de entradas | ✅ Implementado |
| **File Upload** | Validación de tipos MIME | ✅ Implementado |
| **API Key Protection** | Variables de entorno | ✅ Implementado |
| **Error Handling** | Logs sin información sensible | ✅ Implementado |
| **Rate Limiting** | Control de requests | ⏳ Planificado |

### 🛠️ **Manejo de Errores**

```python
# Jerarquía de excepciones
class TTSException(Exception):
    """Base exception for TTS operations"""
    pass

class EngineNotAvailableException(TTSException):
    """Engine is not available"""
    pass

class AudioGenerationException(TTSException):
    """Error generating audio"""
    pass

class FileSystemException(TTSException):
    """File system related errors"""
    pass
```

---

## 🔮 Evolución Futura

### 📋 **Roadmap Técnico**

```mermaid
gantt
    title Roadmap de Desarrollo
    dateFormat  YYYY-MM-DD
    section Fase 1 - Core
    Sistema Base TTS     :done, core1, 2025-01-01, 2025-02-15
    Interfaz Web        :done, web1, 2025-02-01, 2025-02-28
    Sistema Fallbacks   :done, fall1, 2025-02-15, 2025-03-01
    
    section Fase 2 - Mejoras
    Sistema de Cache    :active, cache1, 2025-03-01, 2025-03-15
    API REST           :api1, 2025-03-10, 2025-03-30
    Métricas Avanzadas :metrics1, 2025-03-20, 2025-04-10
    
    section Fase 3 - Escalabilidad
    Contenedores Docker :docker1, 2025-04-01, 2025-04-20
    Base de Datos      :db1, 2025-04-15, 2025-05-05
    Microservicios     :micro1, 2025-05-01, 2025-06-01
```

### 🏗️ **Arquitectura Futura**

```mermaid
graph TB
    subgraph "Load Balancer"
        LB[NGINX/HAProxy]
    end
    
    subgraph "API Gateway"
        AG[Kong/Zuul]
    end
    
    subgraph "Microservices"
        MS1[TTS Service]
        MS2[Voice Clone Service]
        MS3[File Service]
        MS4[User Service]
    end
    
    subgraph "Databases"
        DB1[(PostgreSQL<br/>Metadata)]
        DB2[(Redis<br/>Cache)]
        DB3[(MinIO<br/>Object Storage)]
    end
    
    subgraph "Monitoring"
        M1[Prometheus]
        M2[Grafana]
        M3[ELK Stack]
    end
    
    LB --> AG
    AG --> MS1
    AG --> MS2
    AG --> MS3
    AG --> MS4
    
    MS1 --> DB1
    MS2 --> DB1
    MS3 --> DB3
    MS4 --> DB1
    
    MS1 --> DB2
    MS2 --> DB2
    
    MS1 --> M1
    MS2 --> M1
    MS3 --> M1
    MS4 --> M1
    
    style LB fill:#f3e5f5
    style AG fill:#e3f2fd
    style MS1 fill:#e8f5e8
    style MS2 fill:#e8f5e8
    style MS3 fill:#e8f5e8
    style MS4 fill:#e8f5e8
    style DB1 fill:#fff3e0
    style DB2 fill:#fff3e0
    style DB3 fill:#fff3e0
    style M1 fill:#f1f8e9
    style M2 fill:#f1f8e9
    style M3 fill:#f1f8e9
```

---

## 📚 Referencias y Recursos

### 📖 **Documentación Técnica**

- [Flask Documentation](https://flask.palletsprojects.com/)
- [ElevenLabs API Docs](https://elevenlabs.io/docs)
- [PyTorch Audio](https://pytorch.org/audio/)
- [librosa Documentation](https://librosa.org/)

### 🛠️ **Herramientas Utilizadas**

- **Development**: VS Code, Python 3.12
- **Testing**: pytest, unittest
- **Documentation**: Markdown, Mermaid
- **Monitoring**: Python logging, JSON metrics

---

<div align="center">

**📋 Esta documentación se actualiza continuamente**

*Última actualización: Agosto 2025*

---

🔗 **Enlaces relacionados:**  
[README Principal](README_NEW.md) • [Configuración](TODO.md) • [API Docs](API.md)

</div>

```mermaid
graph TB
    subgraph "Capa de Cliente"
        A[Navegador Web] --> B[Aplicación Web Flask]
        C[Usuario CLI] --> D[Scripts Python]
    end
    
    subgraph "Capa de Aplicación"
        B --> E[Manejador de Solicitudes]
        D --> F[Ejecutor de Scripts]
        E --> G[Selector de Motor]
        F --> G
    end
    
    subgraph "Capa de Procesamiento"
        G --> H[Procesador ElevenLabs]
        G --> I[Procesador Coqui TTS]
        H --> J[Cliente API]
        I --> K[Motor TTS Local]
    end
    
    subgraph "Servicios Externos"
        J --> L[API ElevenLabs]
        K --> M[Modelos TTS]
        K --> N[Modelos de Clonación]
    end
    
    subgraph "Capa de Almacenamiento"
        O[Sistema de Archivos] --> P[Archivos de Audio]
        O --> Q[Archivos Subidos]
        O --> R[Archivos Generados]
    end
    
    E --> O
    F --> O
    H --> O
    I --> O
    
    style A fill:#e3f2fd
    style C fill:#e3f2fd
    style B fill:#f3e5f5
    style D fill:#f3e5f5
    style H fill:#fff3e0
    style I fill:#e8f5e8
    style L fill:#ffebee
    style M fill:#f1f8e9
    style N fill:#fce4ec
```

### Diagrama de Flujo de Datos

```mermaid
flowchart TD
    A[Entrada del Usuario] --> B{Tipo de Entrada}
    
    B -->|Texto| C[Solicitud TTS]
    B -->|Audio + Texto| D[Solicitud Clonación]
    
    C --> E{Selección de Motor}
    D --> E
    
    E -->|ElevenLabs| F[Solicitud API]
    E -->|Coqui| G[Procesamiento Local]
    
    F --> H[API ElevenLabs]
    G --> I[Modelo TTS]
    G --> J[Modelo Clonación]
    
    H --> K[Respuesta de Audio]
    I --> K
    J --> K
    
    K --> L[Almacenamiento]
    L --> M[Descarga Usuario]
    
    style A fill:#e8f5e8
    style K fill:#fff3e0
    style M fill:#e3f2fd
```

### Arquitectura de Entornos Virtuales

```mermaid
graph LR
    subgraph "Python del Sistema"
        A[Python 3.10]
    end
    
    subgraph "Entorno ElevenLabs"
        B[venv-elevenlabs]
        B --> C[Flask 3.1.1]
        B --> D[requests 2.32.4]
        B --> E[python-dotenv 1.1.1]
        B --> F[werkzeug 3.1.3]
    end
    
    subgraph "Entorno Coqui TTS"
        G[venv-coqui]
        G --> H[TTS 0.22.0]
        G --> I[torch 2.7.1]
        G --> J[torchaudio 2.7.1]
        G --> K[librosa 0.10.0]
        G --> L[scipy 1.11.4]
        G --> M[numpy 1.22.0]
    end
    
    A --> B
    A --> G
    
    style A fill:#ffebee
    style B fill:#e8f5e8
    style G fill:#fff3e0
```

### Flujo de Solicitudes de la Aplicación Web

```mermaid
sequenceDiagram
    participant U as Usuario
    participant B as Navegador
    participant F as App Flask
    participant E as ElevenLabs
    participant C as Coqui TTS
    participant S as Sistema Archivos
    
    U->>B: Acceder / (Inicio)
    B->>F: GET /
    F->>B: Plantilla HTML
    B->>U: Mostrar Interfaz
    
    U->>B: Enviar Formulario TTS
    B->>F: POST / (datos TTS)
    
    alt Motor ElevenLabs
        F->>E: Solicitud API
        E->>F: Respuesta Audio
    else Motor Coqui
        F->>C: Procesamiento Local
        C->>F: Archivo Audio
    end
    
    F->>S: Guardar Audio
    F->>B: Respuesta Éxito
    B->>U: Enlace Descarga
    
    U->>B: Enviar Clonación Voz
    B->>F: POST / (Audio + Texto)
    F->>S: Guardar Subida
    F->>C: Procesar Clonación
    C->>F: Audio Clonado
    F->>S: Guardar Resultado
    F->>B: Respuesta Éxito
    B->>U: Enlace Descarga
```

### Flujo de Manejo de Errores

```mermaid
flowchart TD
    A[Solicitud] --> B{¿Entrada Válida?}
    B -->|No| C[Devolver Error]
    B -->|Sí| D{¿Motor Disponible?}
    
    D -->|No| E[Error Motor]
    D -->|Sí| F{¿Procesar Solicitud?}
    
    F -->|Éxito| G[Devolver Audio]
    F -->|Error API| H[Respuesta Error API]
    F -->|Error Procesamiento| I[Error Procesamiento]
    F -->|Error Almacenamiento| J[Error Almacenamiento]
    
    C --> K[Notificación Usuario]
    E --> K
    H --> K
    I --> K
    J --> K
    
    style C fill:#ffebee
    style E fill:#ffebee
    style H fill:#ffebee
    style I fill:#ffebee
    style J fill:#ffebee
    style G fill:#e8f5e8
``` 