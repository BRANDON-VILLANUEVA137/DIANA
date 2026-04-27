# 🤖 Diana - Virtual Assistant with Multi-Language Support

Un asistente de IA inteligente que entiende español e inglés y responde siempre en inglés, impulsado por Google Gemini y ElevenLabs.

### ✨ Características Principales
- 🌐 **Multi-Idioma**: Entiende español e inglés automáticamente
- 🎯 **IA Avanzada**: Usa Google Gemini 2.0 Flash para procesamiento natural
- 🎙️ **Síntesis de Voz**: ElevenLabs para respuestas de audio realistas
- ⚡ **Comandos**: Abre/cierra aplicaciones con órdenes naturales
- 📚 **Contexto**: Mantiene memoria de conversaciones
- 📝 **Historial**: Guarda conversaciones para análisis

## 🚀 Inicio Rápido

### 1. Clonar y Configurar
```powershell
# Navegar al proyecto
cd c:\Users\USUARIO\Desktop\DIANA

# Copiar configuración
Copy-Item .env.example .env

# Editar .env con tus API keys (Google Gemini + ElevenLabs)
```

### 2. Instalar Dependencias
```powershell
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Instalar paquetes
pip install -r requirements.txt
```

### 3. Ejecutar Diana
```powershell
# Ejecución normal
python src/main.py

# Test de configuración
python src/main.py --test

# Test completo
python test_diana.py
```

### 4. Ejemplos de Uso
```
You: ¿Cuál es la capital de Francia?
[Detected: Spanish (95%)]
Diana: The capital of France is Paris, a beautiful city in north-central France...

You: open notepad
[Detected: English (99%)]
Diana: Opened Text editor

You: help
Diana: Available Commands: open, close, list, help, exit
```

---

## 📂 Estructura del Proyecto

```
DIANA/
├── src/
│   ├── main.py                              # Punto de entrada principal
│   ├── config/
│   │   └── config.py                        # Configuración centralizada
│   └── modules/
│       ├── language_detector.py             # Detección de idioma
│       ├── ai_processor.py                  # Google Gemini integration
│       ├── voice_handler.py                 # ElevenLabs voice synthesis
│       └── command_processor.py             # Command parsing & execution
│
├── logs/                                    # Archivos de log
├── data/                                    # Historial de conversaciones
│
├── requirements.txt                         # Dependencias Python
├── .env.example                             # Configuración de ejemplo
├── README.md                                # Este archivo
├── QUICK_START.md                           # Guía rápida
├── DOCUMENTATION.md                         # Documentación completa
├── test_diana.py                            # Suite de pruebas
└── .gitignore                               # Archivos a ignorar en git
```

---

## ⚙️ Configuración

### Variables de Entorno (.env)
```env
# Google Gemini API
GOOGLE_API_KEY=your_api_key_here

# ElevenLabs API (opcional, para síntesis de voz)
ELEVENLABS_API_KEY=your_api_key_here
```

### Opciones en config.py

#### Idiomas de Entrada
```python
INPUT_LANGUAGES = ["es", "en"]  # Spanish and English
OUTPUT_LANGUAGE = "en"           # Always English output
```

#### Síntesis de Voz
```python
USE_VOICE_OUTPUT = False         # Set to True to enable
ELEVENLABS_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"  # Rachel (default)
```

#### Aplicaciones Permitidas
```python
ALLOWED_APPS = {
    "notepad": {
        "paths": [r"C:\Windows\System32\notepad.exe"],
        "aliases": ["block", "editor"],
        "description": "Text editor"
    },
    ...
}
```

---

## 🎮 Comandos Disponibles

| Comando | Ejemplo | Descripción |
|---------|---------|-------------|
| `open` | `open chrome` / `abre navegador` | Abre una aplicación |
| `close` | `close calculator` / `cierra calculadora` | Cierra una aplicación |
| `list` | `list` / `lista` | Lista aplicaciones disponibles |
| `help` | `help` / `ayuda` | Muestra comandos disponibles |
| `exit` | `exit` / `salir` | Cierra Diana |

### Consultas Naturales

Diana también responde preguntas en español o inglés:

```
You: ¿Qué es machine learning?
Diana: Machine learning is a subset of artificial intelligence (AI) 
       that focuses on developing algorithms...

You: How do I learn Python?
Diana: Here are some effective ways to learn Python:
       1. Start with basics through online courses
       2. Practice with small projects...
```

---

## 🔌 Módulos y Componentes

### 1. Language Detector (`language_detector.py`)
Detecta automáticamente el idioma de entrada usando `langdetect`.

```python
detector = LanguageDetector()
lang, confidence = detector.detect_language("Hola")
# Resultado: ("es", 0.98)
```

### 2. AI Processor (`ai_processor.py`)
Procesa consultas naturales con Google Gemini, manteniendo contexto.

```python
processor = AIProcessor(api_key="...", model="gemini-2.0-flash")
response = processor.process_input("Tell me about AI", "en")
```

### 3. Voice Handler (`voice_handler.py`)
Convierte texto a voz usando ElevenLabs con múltiples voces.

```python
handler = VoiceHandler(api_key="...")
handler.speak("Hello, I am Diana")
```

### 4. Command Processor (`command_processor.py`)
Analiza y ejecuta comandos del sistema.

```python
processor = CommandProcessor(allowed_apps={...})
result = processor.execute_command({"type": "open", "target": "notepad"})
```

---

## 📖 Documentación Adicional

- **[QUICK_START.md](QUICK_START.md)** - Guía rápida para empezar
- **[DOCUMENTATION.md](DOCUMENTATION.md)** - Documentación completa y avanzada
- **[test_diana.py](test_diana.py)** - Suite de pruebas para verificar funcionamiento

---

## 🔑 API Keys Requeridas

### Google Gemini
1. Ir a https://makersuite.google.com/app/apikey
2. Crear nueva API key
3. Copiar en el archivo `.env`

### ElevenLabs (Opcional)
1. Registrarse en https://elevenlabs.io
2. Ir a API keys
3. Copiar en el archivo `.env`
4. Habilitar `USE_VOICE_OUTPUT = True` en config.py

### Acceder a Módulos Directamente (Programáticamente)

```python
from src.modules.app_launcher import AppLauncher
from src.config.config import BASE_COMMANDS

launcher = AppLauncher(config)
success, message = launcher.open_app("chrome")
```

### Agregar Comando Personalizado

```python
assistant.command_processor.add_custom_command(
    cmd_name="screenshot",
    handler="custom_module.take_screenshot",
    aliases=["captura", "foto"]
)
```

---

## 📝 Logs

Los logs se guardan en `logs/assistant.log`:

```bash
# Ver logs en tiempo real (Windows)
type logs\assistant.log

# Ver logs en tiempo real (Linux/macOS)
tail -f logs/assistant.log
```

---

## 🔒 Seguridad

- ✅ Whitelist de aplicaciones permitidas (en `config.py`)
- ✅ Validación de entrada con regex
- ✅ Uso de `subprocess.Popen()` sin `shell=True`
- ✅ Auditoría de comandos ejecutados
- ✅ Manejo de permisos del sistema

---

## 🚀 Próximos Pasos

### Fase 1: Mejoras Locales
- [ ] Agregar más aplicaciones a whitelist
- [ ] Implementar gestos del mouse
- [ ] Agregar comandos de sistema (shutdown, lock, etc.)
- [ ] Mejorar parser de comandos con NLP

### Fase 2: Interfaz Gráfica
- [ ] Crear GUI con PyQt5 / Tkinter
- [ ] Dashboard de estado
- [ ] Personalización de temas

### Fase 3: IA Avanzada
- [ ] Integración con OpenAI API
- [ ] Fine-tuning de modelos locales
- [ ] Learning de patrones de uso

### Fase 4: Escalado
- [ ] REST API para acceso remoto
- [ ] Sincronización entre dispositivos
- [ ] Integración con servicios web
- [ ] Dockerización

---

## 🐛 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'win32gui'"
```bash
pip install pywin32
python -m pip install --upgrade pywin32
```

### Error: "Application not found"
- Verificar que la ruta en `config.py` es correcta
- Usar comillas si la ruta tiene espacios
- En Windows: Usar `r"C:\ruta\app.exe"` (raw string)

### Error: "Speech Recognition not working"
- Asegurar que el micrófono está conectado y funciona
- Instalar: `pip install SpeechRecognition pydub`
- Requerir conexión a Internet (usa Google Speech API)

### El asistente se congela
- Aumentar `LISTENING_TIMEOUT` en `config.py`
- Verificar los logs en `logs/assistant.log`

---

## 📚 Documentación Completa

Ver [docs/ARQUITECTURA.md](docs/ARQUITECTURA.md) para:
- Arquitectura detallada del sistema
- Flujo de datos completo
- Requisitos técnicos por SO
- Guía de extensibilidad
- Consideraciones de seguridad

---

## 📄 Licencia

Libre para uso personal y educativo.

---

## 👨‍💻 Autor

Desarrollado como asistente técnico especializado en arquitectura de IA.

**Versión**: 1.0.0  
**Estado**: Beta Funcional (MVP Local)  
**Última actualización**: Abril 2026
