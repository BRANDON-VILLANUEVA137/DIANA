# 📖 Diana Virtual Assistant - Documentación Completa

## Descripción General

**Diana** es un asistente virtual inteligente que:
- ✅ Entiende entrada en **español e inglés**
- ✅ Responde siempre en **inglés**
- ✅ Usa **Google Gemini** para procesamiento de lenguaje natural
- ✅ Integra **ElevenLabs** para síntesis de voz realista
- ✅ Ejecuta comandos para abrir/cerrar aplicaciones
- ✅ Mantiene historial de conversaciones

---

## 🔧 Instalación

### Requisitos
- Python 3.8+
- Windows 10/11 (o Linux/macOS con ajustes)
- Cuentas con API keys:
  - Google Gemini: https://makersuite.google.com/app/apikey
  - ElevenLabs: https://elevenlabs.io

### Paso 1: Configurar API Keys

```powershell
# Copiar archivo de ejemplo
Copy-Item .env.example .env

# Editar .env y agregar tus API keys
# Ejemplo:
# GOOGLE_API_KEY=sk-...tu-clave...
# ELEVENLABS_API_KEY=sk_...tu-clave...
```

### Paso 2: Instalar Dependencias

```powershell
# Activar entorno virtual (si no está activo)
.\.venv\Scripts\Activate.ps1

# Instalar paquetes
pip install -r requirements.txt
```

### Paso 3: Verificar Instalación

```powershell
# Test de configuración
python src/main.py --test
```

**Output esperado:**
```
╔════════════════════════════════════════════════╗
║  Diana - Virtual Assistant v2.0                ║
║  Multi-Language Input | English Output         ║
╚════════════════════════════════════════════════╝

Testing Diana Setup...

1. Testing Language Detection:
   Spanish text: ES (95%) ✓
   English text: EN (98%) ✓

2. Testing AI Processor:
   ✓ AI Response: The capital of France is Paris, a beautiful...

3. Testing Voice Handler:
   ✓ Voice handler ready
   Voice ID: EXAVITQu4vr4xnSDxMaL

4. Testing Command Processor:
   ✓ Parsed command: open → notepad

Setup test complete!
```

---

## 🎯 Uso

### Ejecución Normal

```powershell
python src/main.py
```

### Ejemplos de Interacción

#### Ejemplo 1: Pregunta en Español

```
╔════════════════════════════════════════════════╗
║  Diana - Virtual Assistant v2.0                ║
║  Multi-Language Input | English Output         ║
╚════════════════════════════════════════════════╝

You: ¿Cuál es la capital de España?
[Detected: Spanish (98%)]
Diana: The capital of Spain is Madrid, located in the center of the 
       country. It's the largest city in Spain and serves as the country's 
       administrative and cultural hub.
```

#### Ejemplo 2: Pregunta en Inglés

```
You: Tell me about artificial intelligence
[Detected: English (99%)]
Diana: Artificial intelligence (AI) refers to computer systems designed to 
       perform tasks that typically require human intelligence. This includes 
       learning from experience, recognizing patterns, understanding language, 
       and making decisions...
```

#### Ejemplo 3: Comando para Abrir Aplicación

```
You: abre el navegador
[Detected: Spanish (97%)]
Diana: Opened Google Chrome
```

---

## 📝 Configuración Avanzada

### Archivo: `src/config/config.py`

#### 1. Cambiar Idiomas Soportados

```python
SUPPORTED_LANGUAGES = ["es", "en"]  # Agregar más: "fr", "de", "it"
INPUT_LANGUAGES = ["es", "en"]      # Idiomas de entrada
OUTPUT_LANGUAGE = "en"               # Idioma de salida (siempre inglés)
```

#### 2. Habilitar Síntesis de Voz

```python
USE_VOICE_OUTPUT = True  # Cambiar a True para activar
ELEVENLABS_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Rachel (default)

# Opciones de voces disponibles:
# - "EXAVITQu4vr4xnSDxMaL" → Rachel (Female - American)
# - "nPczCjzI2devNBz1zQrb" → Brian (Male - American)
# - "9BWtsMINqrJLrRacOk9Q" → Aria (Female - American)
# - "LFSE5hU29RdP8lSMZYdP" → Bella (Female - American)
```

#### 3. Configurar Aplicaciones Permitidas

```python
ALLOWED_APPS = {
    "visual_studio_code": {
        "paths": [r"C:\Users\Tu_Usuario\AppData\Local\Programs\Microsoft VS Code\Code.exe"],
        "aliases": ["vscode", "vs", "code"],
        "description": "Visual Studio Code"
    },
    "firefox": {
        "paths": [r"C:\Program Files\Mozilla Firefox\firefox.exe"],
        "aliases": ["firefox", "mozilla"],
        "description": "Mozilla Firefox"
    }
}
```

#### 4. Modelo de IA

```python
AI_MODEL = "gemini-2.0-flash"  # Modelo más rápido y actual
# Alternativas: "gemini-1.5-pro" (más poderoso)
```

#### 5. Configuración del Sistema

```python
ASSISTANT_NAME = "Diana"
ASSISTANT_VERSION = "2.0"
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
MAX_HISTORY = 10    # Mensajes a mantener en contexto
```

---

## 🎙️ Funcionalidades

### 1. Detección Automática de Idioma

Diana detecta automáticamente si escribes en español o inglés usando el módulo `langdetect`.

```python
# Cómo funciona internamente:
from modules.language_detector import LanguageDetector

detector = LanguageDetector()
lang, confidence = detector.detect_language("Hola, ¿cómo estás?")
# Resultado: ("es", 0.98)
```

### 2. Procesamiento con Google Gemini

Las consultas se procesan con Google Gemini 2.0 Flash, manteniendo contexto de conversación.

```python
from modules.ai_processor import AIProcessor

processor = AIProcessor(api_key="...", system_prompt="...")
response = processor.process_input("What is AI?", language="en")
# response["content"] → "Artificial Intelligence (AI) refers to..."
```

### 3. Síntesis de Voz con ElevenLabs

Las respuestas se pueden convertir a audio usando voces de alta calidad.

```python
from modules.voice_handler import VoiceHandler

voice = VoiceHandler(api_key="...", voice_id="...")
voice.speak("Hello! This is Diana speaking.")
```

### 4. Procesamiento de Comandos

Diana puede ejecutar comandos del sistema como abrir/cerrar aplicaciones.

```
Comando de usuario: "open notepad"
↓
parse_command() → {"type": "open", "target": "notepad"}
↓
execute_command() → Abre C:\Windows\System32\notepad.exe
```

---

## 📊 Estructura del Proyecto

```
DIANA/
├── src/
│   ├── main.py                          # Punto de entrada principal
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   └── config.py                    # Configuración centralizada
│   │
│   └── modules/
│       ├── __init__.py
│       ├── language_detector.py         # Detecta idioma (español/inglés)
│       ├── ai_processor.py              # Integración con Google Gemini
│       ├── voice_handler.py             # Integración con ElevenLabs
│       └── command_processor.py         # Procesamiento de comandos
│
├── logs/
│   └── diana.log                        # Archivo de log (generado automáticamente)
│
├── data/
│   └── conversation_history.json        # Historial de conversaciones
│
├── requirements.txt                     # Dependencias Python
├── .env                                 # API Keys (no versionar)
├── .env.example                         # Ejemplo de .env
├── README.md                            # Documentación principal
├── QUICK_START.md                       # Guía rápida
└── DOCUMENTATION.md                     # Esta documentación
```

---

## 🔄 Flujo de Operación

```
Usuario ingresa texto
         ↓
   [Detección de Idioma]
   - ¿Es español? → es
   - ¿Es inglés? → en
         ↓
   [Análisis de Tipo]
   - ¿Es comando? (open, close, etc.) → Procesar comando
   - ¿Es pregunta? → Procesar con IA
         ↓
   [Procesamiento]
   Si es comando:
   - Ejecutar aplicación/acción del sistema
   
   Si es pregunta:
   - Enviar a Google Gemini
   - Mantener contexto de conversación anterior
         ↓
   [Generación de Respuesta]
   - Siempre en inglés
   - Respuesta clara y estructurada
         ↓
   [Salida de Voz (Opcional)]
   - Si está habilitado: ElevenLabs convierte a audio
         ↓
   [Guardar Historial]
   - Guardar en conversation_history.json
```

---

## 🐛 Solución de Problemas

### Problema: "GOOGLE_API_KEY not set"

**Solución:**
```powershell
# 1. Crear archivo .env
cp .env.example .env

# 2. Editar .env y agregar:
GOOGLE_API_KEY=tu_clave_aqui

# 3. Reiniciar Diana
```

### Problema: "ModuleNotFoundError: No module named 'google.generativeai'"

**Solución:**
```powershell
pip install --upgrade google-genai==1.73.1
```

### Problema: Voice output no funciona

**Solución:**
```powershell
# Verificar API key
# Deshabilitar temporalmente
USE_VOICE_OUTPUT = False

# Reinstalar elevenlabs
pip install --upgrade elevenlabs
```

### Problema: Language detection siempre devuelve "en"

**Solución:**
```python
# Aumentar longitud mínima de texto para análisis
# En language_detector.py, cambiar:
if len(text.strip()) < 2:  # Cambiar a 3 o 5 caracteres mínimo
```

### Ver Logs en Tiempo Real

```powershell
# Windows
Get-Content logs/diana.log -Wait -Tail 20

# Linux/macOS
tail -f logs/diana.log
```

---

## 🚀 Ejemplos de Uso Avanzado

### Ejemplo 1: Conversación Multi-Turno

```
You: Tell me about machine learning
[Detected: English (99%)]
Diana: Machine learning is a subset of artificial intelligence (AI) 
       that focuses on developing algorithms and statistical models...

You: ¿Cuáles son sus aplicaciones?
[Detected: Spanish (97%)]
Diana: Machine learning applications are vast and diverse across many 
       industries:
       1. Healthcare: Diagnosis assistance and drug discovery
       2. Finance: Fraud detection and risk analysis
       3. Retail: Recommendation systems and customer behavior prediction
       ...
```

### Ejemplo 2: Uso en Batch/Scripts

```python
from src.modules.language_detector import LanguageDetector
from src.modules.ai_processor import AIProcessor

# Inicializar
detector = LanguageDetector()
processor = AIProcessor(api_key="...", system_prompt="...")

# Procesar múltiples inputs
queries = [
    "¿Qué es Python?",
    "What is JavaScript?",
    "Explique las redes neuronales"
]

for query in queries:
    lang, _ = detector.detect_language(query)
    response = processor.process_input(query, lang)
    print(f"Q ({lang}): {query}")
    print(f"A: {response['content']}\n")
```

### Ejemplo 3: Guardar/Cargar Historial

```python
# Guardar conversación
assistant.ai_processor.save_history("data/conversation_2024.json")

# Cargar conversación anterior
assistant.ai_processor.load_history("data/conversation_2024.json")

# Ver historial
history = assistant.ai_processor.get_history()
for msg in history:
    print(f"[{msg['role'].upper()}] {msg['content']}")
```

---

## 📈 Rendimiento

### Tiempos de Respuesta (Aproximado)

| Operación | Tiempo |
|-----------|--------|
| Detección de idioma | 50-100ms |
| Consulta a Gemini | 1-3 segundos |
| Síntesis de voz | 1-2 segundos |
| Ejecución de comando | <100ms |

### Uso de Recursos

| Recurso | Consumo |
|---------|---------|
| RAM | 150-300 MB |
| CPU | 5-15% en espera |
| Almacenamiento | ~2MB (sin historial) |

---

## 🔐 Seguridad

### Recomendaciones

1. **Nunca commits .env**: Ya está en .gitignore
2. **Usa API keys con límites**: Configura cuotas en Google Cloud
3. **Rotación de keys**: Cambia tus API keys periódicamente
4. **Logs**: Los logs contienen información sensible, protégelos

### Protección de Datos

```python
# Los logs NO incluyen conversaciones completas por defecto
# Para desactivar logging de mensajes:
LOG_LEVEL = "WARNING"  # Solo errores y avisos
```

---

## 🤝 Contribuciones

Para contribuir:

1. Fork el repositorio
2. Crea rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m "Add nueva funcionalidad"`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Pull Request

---

## 📜 Licencia

MIT License - Ver LICENSE.md

---

## 📞 Soporte

- **Issues**: Reporta problemas en GitHub
- **Docs**: https://ai.google.dev (Google Gemini)
- **API**: https://elevenlabs.io/docs (ElevenLabs)

---

**¡Gracias por usar Diana! 🎉**
