# 🚀 Diana - Quick Start Guide

## Setup Rápido (5 minutos)

### 1. Configurar API Keys

```powershell
# 1. Crear archivo .env desde el ejemplo
Copy-Item .env.example .env

# 2. Editar .env y agregar tus claves:
# - GOOGLE_API_KEY: obtén en https://makersuite.google.com/app/apikey
# - ELEVENLABS_API_KEY: obtén en https://elevenlabs.io
```

### 2. Instalar Dependencias

```powershell
# Activar virtual environment (si no está activo)
.\.venv\Scripts\Activate.ps1

# Instalar/actualizar paquetes
pip install -r requirements.txt
```

### 3. Ejecutar Diana

```powershell
# Ejecución normal
python src/main.py

# Probar configuración
python src/main.py --test
```

---

## 💬 Ejemplos de Uso

### Preguntar el Nombre de Diana

```
You: What is your name?
[Detected: English (98%)]
Diana: My name is D-I-03367. I am a virtual assistant powered by Google Gemini and ElevenLabs. 
       You can change my name anytime by saying 'call me [new name]'.

You: ¿Cuál es tu nombre?
[Detected: Spanish (99%)]
Diana: My name is D-I-03367. I am a virtual assistant powered by Google Gemini and ElevenLabs. 
       You can change my name anytime by saying 'call me [new name]'.
```

### Cambiar el Nombre de Diana

```
You: Call me ALEXA
[Detected: English (97%)]
ALEXA: Thank you! You can now call me ALEXA. I will remember this name. 
       My previous name was D-I-03367.

You: Llámame ASISTENTE
[Detected: Spanish (98%)]
ASISTENTE: Thank you! You can now call me ASISTENTE. I will remember this name. 
           My previous name was D-I-03367.
```

**Nota:** El cambio de nombre se guarda automáticamente en el archivo `.env` y persistirá en futuras sesiones.

### Entrada en Español → Respuesta en Inglés

```
You: ¿Cuál es la capital de Francia?
[Detected: Spanish (95%)]
Diana: The capital of France is Paris, a beautiful city located in north-central France. 
       It's known for iconic landmarks like the Eiffel Tower and the Louvre Museum.
```

### Entrada en Inglés → Respuesta en Inglés

```
You: What is the weather like?
[Detected: English (98%)]
Diana: I don't have access to real-time weather data, but I can help you find weather 
       information online or guide you to a weather service.
```

### Comandos Disponibles

```
You: open notepad
[Detected: English (99%)]
Diana: Opened Text editor

You: help
Diana: Available Commands:
       - open <app>: Open an application
       - close <app>: Close an application
       - list: List available applications
       - help: Show help message
       - exit: Close the assistant

You: exit
Diana: Goodbye! Have a great day!
```

---

## 📋 Características

✅ **Multi-Language Input** - Detecta automáticamente español e inglés
✅ **English Output** - Todas las respuestas en inglés
✅ **Google Gemini AI** - Procesa lenguaje natural con IA
✅ **ElevenLabs Voice** - Síntesis de voz con 5+ voces disponibles
✅ **Command Execution** - Abre/cierra aplicaciones
✅ **Conversation History** - Mantiene contexto de la conversación
✅ **Logging** - Registro completo de operaciones

---

## 🔧 Configuración Personalizada

Editar `src/config/config.py` para:

### Habilitar síntesis de voz
```python
USE_VOICE_OUTPUT = True  # Cambiar a True
ELEVENLABS_VOICE_ID = "nPczCjzI2devNBz1zQrb"  # Brian (male voice)
```

### Cambiar idiomas soportados
```python
INPUT_LANGUAGES = ["es", "en", "fr"]  # Agregar más idiomas
```

### Agregar aplicaciones
```python
ALLOWED_APPS = {
    "mi_app": {
        "paths": [r"C:\Ruta\a\mi_app.exe"],
        "aliases": ["app", "myapp"],
        "description": "Mi aplicación"
    }
}
```

### Voces disponibles en ElevenLabs

```python
ELEVENLABS_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Rachel (Female - American)
ELEVENLABS_VOICE_ID = "nPczCjzI2devNBz1zQrb"  # Brian (Male - American)
ELEVENLABS_VOICE_ID = "9BWtsMINqrJLrRacOk9Q"  # Aria (Female - American)
ELEVENLABS_VOICE_ID = "LFSE5hU29RdP8lSMZYdP"  # Bella (Female - American)
```

---

## 📁 Estructura del Proyecto

```
DIANA/
├── src/
│   ├── main.py                      # Punto de entrada
│   ├── config/
│   │   └── config.py                # Configuración centralizada
│   └── modules/
│       ├── language_detector.py     # Detección de idioma
│       ├── ai_processor.py          # Procesamiento con Google Gemini
│       ├── voice_handler.py         # Síntesis de voz con ElevenLabs
│       └── command_processor.py     # Procesamiento de comandos
├── logs/                            # Archivos de log
├── data/                            # Historial de conversaciones
├── requirements.txt                 # Dependencias
├── .env                             # API Keys (no commit)
└── README.md                        # Esta guía
```

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'google.generativeai'"

```powershell
pip install --upgrade google-genai
```

### Error: "GOOGLE_API_KEY not configured"

Asegúrate de:
1. Copiar `.env.example` a `.env`
2. Agregar tu API key en el archivo `.env`
3. Reiniciar el programa

### Error al usar ElevenLabs

```powershell
pip install --upgrade elevenlabs
```

### Ver logs en tiempo real

```powershell
Get-Content logs/diana.log -Wait -Tail 20
```

---

## 💡 Casos de Uso

- **Asistente Personal**: Responder preguntas en cualquier idioma
- **Automatización**: Abrir/cerrar aplicaciones con comandos en español o inglés
- **Aprendizaje**: Hacer preguntas sobre cualquier tema
- **Accesibilidad**: Síntesis de voz en inglés para todas las respuestas

---

## 📞 Support

Para más información:
- [Documentación de Google Gemini](https://ai.google.dev)
- [Documentación de ElevenLabs](https://elevenlabs.io/docs)
- [GitHub Repository](https://github.com/your-repo/diana)

---

**¡Disfruta usando Diana! 🎉**
