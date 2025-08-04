# 🔌 API Documentation - Sistema de Síntesis de Voz

<div align="center">

![API](https://img.shields.io/badge/API-REST-blue?style=for-the-badge&logo=fastapi)
![Version](https://img.shields.io/badge/Version-1.0-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

**Documentación completa de la API REST**

[🚀 Inicio Rápido](#-inicio-rápido) • [📋 Endpoints](#-endpoints) • [🔑 Autenticación](#-autenticación) • [📊 Ejemplos](#-ejemplos)

</div>

---

## 📊 Visión General de la API

```mermaid
graph TB
    subgraph "🌐 API Endpoints"
        A[🏠 Health Check<br/>/health]
        B[🎤 Text-to-Speech<br/>/api/tts]
        C[🎭 Voice Cloning<br/>/api/clone]
        D[📁 File Management<br/>/api/files]
        E[⚙️ Configuration<br/>/api/config]
    end
    
    subgraph "🔧 HTTP Methods"
        F[GET - Read Operations]
        G[POST - Create Operations]
        H[PUT - Update Operations]
        I[DELETE - Delete Operations]
    end
    
    subgraph "📝 Response Formats"
        J[JSON - Data Responses]
        K[Binary - Audio Files]
        L[Multipart - File Uploads]
    end
    
    A --> F
    B --> G
    C --> G
    D --> F
    D --> G
    D --> I
    E --> F
    E --> H
    
    B --> J
    B --> K
    C --> J
    C --> K
    C --> L
    
    style A fill:#e8f5e8
    style B fill:#e3f2fd
    style C fill:#f3e5f5
    style D fill:#fff3e0
    style E fill:#f1f8e9
```

## 🚀 Inicio Rápido

### 🔗 **Base URL**
```
http://localhost:5000
```

### 📋 **Headers Requeridos**
```http
Content-Type: application/json
Accept: application/json
```

### 🔑 **Autenticación** (Futuro)
```http
Authorization: Bearer <api_key>
```

---

## 📋 Endpoints

### 🏠 **Health Check**

#### `GET /health`
Verifica el estado del servicio.

**Request:**
```http
GET /health HTTP/1.1
Host: localhost:5000
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: text/plain

OK
```

**Códigos de respuesta:**
- `200` - Servicio operativo
- `503` - Servicio no disponible

---

### 🎤 **Text-to-Speech**

#### `POST /api/tts`
Convierte texto a audio usando el motor especificado.

**Request:**
```http
POST /api/tts HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "text": "Hola mundo, esto es una prueba de síntesis de voz",
  "engine": "elevenlabs",
  "voice_id": "EXAVITQu4vr4xnSDxMaL",
  "output_format": "wav",
  "options": {
    "stability": 0.5,
    "similarity_boost": 0.75,
    "style": 0.0
  }
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `text` | string | ✅ | Texto a sintetizar (max 1000 chars) |
| `engine` | string | ❌ | Motor TTS (`elevenlabs`, `espeak`, `pyttsx3`) |
| `voice_id` | string | ❌ | ID de voz (solo ElevenLabs) |
| `output_format` | string | ❌ | Formato de salida (`wav`, `mp3`) |
| `options` | object | ❌ | Opciones específicas del motor |

**Response (Success):**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "message": "Audio generado exitosamente",
  "data": {
    "audio_url": "/static/audio/tts_output_1691234567.wav",
    "file_size": 245760,
    "duration": 3.5,
    "engine_used": "elevenlabs",
    "processing_time": 2.3
  },
  "metadata": {
    "text_length": 45,
    "voice_id": "EXAVITQu4vr4xnSDxMaL",
    "generated_at": "2025-08-04T20:30:45Z"
  }
}
```

**Response (Error):**
```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "success": false,
  "error": {
    "code": "INVALID_TEXT",
    "message": "Texto demasiado largo (máximo 1000 caracteres)",
    "details": {
      "text_length": 1250,
      "max_length": 1000
    }
  }
}
```

**Códigos de respuesta:**
- `200` - Audio generado exitosamente
- `400` - Parámetros inválidos
- `429` - Límite de rate excedido
- `500` - Error interno del servidor
- `503` - Motor TTS no disponible

---

### 🎭 **Voice Cloning**

#### `POST /api/clone`
Clona una voz usando una muestra de audio y genera nueva síntesis.

**Request:**
```http
POST /api/clone HTTP/1.1
Host: localhost:5000
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="audio_file"; filename="voice_sample.wav"
Content-Type: audio/wav

[binary audio data]
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="text"

Este es el texto que quiero sintetizar con la voz clonada
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="engine"

elevenlabs
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `audio_file` | file | ✅ | Archivo de audio de muestra (WAV, MP3) |
| `text` | string | ✅ | Texto a sintetizar con la voz clonada |
| `engine` | string | ❌ | Motor de clonación (`elevenlabs`, `coqui`) |
| `options` | object | ❌ | Opciones específicas del motor |

**Response (Success):**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "message": "Voz clonada exitosamente",
  "data": {
    "audio_url": "/static/audio/clone_output_1691234567.wav",
    "file_size": 387264,
    "duration": 4.2,
    "engine_used": "elevenlabs",
    "processing_time": 8.7
  },
  "metadata": {
    "original_file": "voice_sample.wav",
    "original_duration": 5.1,
    "text_length": 58,
    "similarity_score": 0.92,
    "generated_at": "2025-08-04T20:35:12Z"
  }
}
```

**Códigos de respuesta:**
- `200` - Voz clonada exitosamente
- `400` - Archivo o parámetros inválidos
- `413` - Archivo demasiado grande
- `415` - Formato de archivo no soportado
- `500` - Error en el procesamiento

---

### 📁 **File Management**

#### `GET /api/files`
Lista archivos de audio generados.

**Request:**
```http
GET /api/files?limit=10&offset=0&type=tts HTTP/1.1
Host: localhost:5000
```

**Query Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | integer | Número de archivos a retornar (default: 10) |
| `offset` | integer | Número de archivos a omitir (default: 0) |
| `type` | string | Tipo de archivo (`tts`, `clone`, `all`) |

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "data": {
    "files": [
      {
        "id": "tts_output_1691234567",
        "filename": "tts_output_1691234567.wav",
        "url": "/static/audio/tts_output_1691234567.wav",
        "type": "tts",
        "size": 245760,
        "duration": 3.5,
        "created_at": "2025-08-04T20:30:45Z",
        "metadata": {
          "text": "Hola mundo...",
          "engine": "elevenlabs"
        }
      }
    ],
    "pagination": {
      "total": 25,
      "limit": 10,
      "offset": 0,
      "has_more": true
    }
  }
}
```

#### `DELETE /api/files/{file_id}`
Elimina un archivo específico.

**Request:**
```http
DELETE /api/files/tts_output_1691234567 HTTP/1.1
Host: localhost:5000
```

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "message": "Archivo eliminado exitosamente"
}
```

---

### ⚙️ **Configuration**

#### `GET /api/config`
Obtiene la configuración actual del sistema.

**Response:**
```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "data": {
    "engines": {
      "available": ["elevenlabs", "espeak", "pyttsx3"],
      "default": "elevenlabs",
      "fallback_order": ["elevenlabs", "espeak", "pyttsx3", "placeholder"]
    },
    "limits": {
      "max_text_length": 1000,
      "max_file_size": 10485760,
      "rate_limit": {
        "requests_per_minute": 60,
        "requests_per_hour": 1000
      }
    },
    "formats": {
      "supported_input": ["wav", "mp3", "flac"],
      "supported_output": ["wav", "mp3"],
      "default_output": "wav"
    }
  }
}
```

#### `PUT /api/config`
Actualiza la configuración del sistema.

**Request:**
```http
PUT /api/config HTTP/1.1
Host: localhost:5000
Content-Type: application/json

{
  "default_engine": "espeak",
  "max_text_length": 1500
}
```

---

## 📊 Ejemplos de Uso

### 🐍 **Python Example**

```python
import requests
import json

# Configuración
BASE_URL = "http://localhost:5000"
headers = {"Content-Type": "application/json"}

# Text-to-Speech
def generate_tts(text, engine="elevenlabs"):
    data = {
        "text": text,
        "engine": engine,
        "output_format": "wav"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/tts",
        headers=headers,
        data=json.dumps(data)
    )
    
    if response.status_code == 200:
        result = response.json()
        audio_url = result["data"]["audio_url"]
        print(f"Audio generado: {BASE_URL}{audio_url}")
        return audio_url
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Voice Cloning
def clone_voice(audio_file_path, text, engine="elevenlabs"):
    files = {
        "audio_file": open(audio_file_path, "rb"),
        "text": (None, text),
        "engine": (None, engine)
    }
    
    response = requests.post(
        f"{BASE_URL}/api/clone",
        files=files
    )
    
    if response.status_code == 200:
        result = response.json()
        audio_url = result["data"]["audio_url"]
        print(f"Voz clonada: {BASE_URL}{audio_url}")
        return audio_url
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

# Uso
if __name__ == "__main__":
    # TTS
    generate_tts("Hola, este es un ejemplo de síntesis de voz")
    
    # Voice Cloning
    clone_voice("voice_sample.wav", "Texto con voz clonada")
```

### 🌐 **JavaScript Example**

```javascript
// Text-to-Speech
async function generateTTS(text, engine = 'elevenlabs') {
    const response = await fetch('/api/tts', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            text: text,
            engine: engine,
            output_format: 'wav'
        })
    });
    
    if (response.ok) {
        const result = await response.json();
        console.log('Audio generado:', result.data.audio_url);
        return result.data.audio_url;
    } else {
        console.error('Error:', response.status, await response.text());
        return null;
    }
}

// Voice Cloning
async function cloneVoice(audioFile, text, engine = 'elevenlabs') {
    const formData = new FormData();
    formData.append('audio_file', audioFile);
    formData.append('text', text);
    formData.append('engine', engine);
    
    const response = await fetch('/api/clone', {
        method: 'POST',
        body: formData
    });
    
    if (response.ok) {
        const result = await response.json();
        console.log('Voz clonada:', result.data.audio_url);
        return result.data.audio_url;
    } else {
        console.error('Error:', response.status, await response.text());
        return null;
    }
}

// Uso
document.addEventListener('DOMContentLoaded', function() {
    // TTS
    generateTTS('Hola desde JavaScript');
    
    // Voice Cloning con file input
    const fileInput = document.getElementById('audioFile');
    if (fileInput && fileInput.files.length > 0) {
        cloneVoice(fileInput.files[0], 'Texto con voz clonada');
    }
});
```

### 📱 **cURL Examples**

```bash
# Health Check
curl -X GET http://localhost:5000/health

# Text-to-Speech
curl -X POST http://localhost:5000/api/tts \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hola mundo desde cURL",
    "engine": "espeak",
    "output_format": "wav"
  }'

# Voice Cloning
curl -X POST http://localhost:5000/api/clone \
  -F "audio_file=@voice_sample.wav" \
  -F "text=Texto con voz clonada desde cURL" \
  -F "engine=elevenlabs"

# List Files
curl -X GET "http://localhost:5000/api/files?limit=5&type=tts"

# Delete File
curl -X DELETE http://localhost:5000/api/files/tts_output_1691234567

# Get Configuration
curl -X GET http://localhost:5000/api/config
```

---

## 🔐 Error Handling

### 📋 **Códigos de Error Comunes**

| Código | Tipo | Descripción |
|--------|------|-------------|
| `400` | Bad Request | Parámetros inválidos o faltantes |
| `401` | Unauthorized | Autenticación requerida |
| `403` | Forbidden | Sin permisos suficientes |
| `404` | Not Found | Recurso no encontrado |
| `413` | Payload Too Large | Archivo demasiado grande |
| `415` | Unsupported Media Type | Formato no soportado |
| `422` | Unprocessable Entity | Datos válidos pero no procesables |
| `429` | Too Many Requests | Límite de rate excedido |
| `500` | Internal Server Error | Error interno del servidor |
| `503` | Service Unavailable | Servicio temporalmente no disponible |

### 🛠️ **Formato de Error Estándar**

```json
{
  "success": false,
  "error": {
    "code": "ERROR_CODE",
    "message": "Descripción del error para el usuario",
    "details": {
      "field": "Información adicional específica",
      "suggestion": "Posible solución"
    }
  },
  "timestamp": "2025-08-04T20:30:45Z",
  "request_id": "req_1691234567"
}
```

---

## 📈 Rate Limiting

### 🚦 **Límites por Defecto**

| Endpoint | Límite | Ventana |
|----------|--------|---------|
| `/health` | 100 req | 1 minuto |
| `/api/tts` | 30 req | 1 minuto |
| `/api/clone` | 10 req | 1 minuto |
| `/api/files` | 60 req | 1 minuto |
| `/api/config` | 20 req | 1 minuto |

### 📊 **Headers de Rate Limiting**

```http
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 25
X-RateLimit-Reset: 1691234567
X-RateLimit-Window: 60
```

---

## 🔒 Autenticación (Futuro)

### 🔑 **API Key Authentication**

```http
Authorization: Bearer sk-1234567890abcdef
```

### 🎫 **JWT Token Authentication**

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 📚 Recursos Adicionales

### 🔗 **Enlaces Útiles**

- [Documentación Principal](README_NEW.md)
- [Arquitectura del Sistema](ARCHITECTURE.md)
- [Guía de Configuración](TODO.md)
- [Ejemplos de Código](examples/)

### 🛠️ **Herramientas Recomendadas**

- **Testing**: [Postman](https://postman.com), [Insomnia](https://insomnia.rest)
- **Documentation**: [Swagger UI](https://swagger.io), [Redoc](https://redocly.com)
- **Monitoring**: [Prometheus](https://prometheus.io), [Grafana](https://grafana.com)

---

<div align="center">

**📋 Esta API está en desarrollo activo**

*Última actualización: Agosto 2025*

---

🔗 **Contacto y Soporte:**  
[Issues](https://github.com/EdissonGirald0/s-ntesis-de-voz/issues) • [Contribuir](CONTRIBUTING.md) • [Licencia](LICENSE)

</div>
