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

### Arquitectura del Sistema de Alto Nivel

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