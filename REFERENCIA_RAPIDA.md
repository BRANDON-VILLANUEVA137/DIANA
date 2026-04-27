# Guía Rápida de Referencia - Asistente Diana

## 🚀 INICIO RÁPIDO (2 minutos)

```powershell
# 1. Ir a la carpeta
cd c:\DESCKTOP\DIANA\ai-assistant

# 2. Crear entorno (primera vez)
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Instalar (primera vez)
pip install -r requirements.txt

# 4. Ejecutar
python src/main.py

# 5. Probar un comando
> abre notepad
```

---

## 📋 LISTA DE COMANDOS DISPONIBLES

### Aplicaciones
```
abre <app>          → Abre una aplicación (ej: "abre chrome")
cierra <app>        → Cierra una aplicación
lista aplicaciones  → Lista apps disponibles
```

### Ventanas
```
ventanas                    → Lista ventanas abiertas
trae <ventana>             → Trae ventana al frente
minimiza <ventana>         → Minimiza una ventana
maximiza <ventana>         → Maximiza una ventana
cierra ventana <ventana>   → Cierra una ventana
```

### Sistema
```
ayuda           → Muestra esta ayuda
salir / exit    → Cierra el asistente
```

---

## 🛠️ TAREAS COMUNES

### Cambiar aplicaciones permitidas
**Archivo:** `src/config/config.py`

```python
ALLOWED_APPS = {
    "miapp": {
        "paths": [r"C:\Ruta\App\miapp.exe"],
        "aliases": ["app", "favorita"],
        "description": "Mi app favorita"
    }
}
```

### Habilitar reconocimiento de voz
**Archivo:** `src/config/config.py`

```python
USE_VOICE_INPUT = True   # Cambiar a True
USE_VOICE_OUTPUT = True  # Cambiar a True
```

### Agregar comando personalizado
**Editar:** `src/main.py`

```python
# En __init__ de AIAssistant:
self.action_handlers["my_action"] = self.my_action_handler

# Luego definir la función:
def my_action_handler(self, param=None):
    # Tu código aquí
    return True, "Completado"
```

### Ver logs
```powershell
# Windows
type logs\assistant.log

# Linux/macOS
tail -f logs/assistant.log
```

---

## 📁 ESTRUCTURA RÁPIDA

```
ai-assistant/
├── src/
│   ├── main.py                    ← Ejecutar esto
│   ├── config/config.py           ← Personalizar aquí
│   └── modules/                   ← Los 4 módulos core
│
├── docs/ARQUITECTURA.md           ← Documentación completa
├── IMPLEMENTACION.md              ← Pasos paso a paso
├── EJEMPLOS.py                    ← Script de ejemplos
├── UTILS.py                       ← Script de utilidades
└── logs/                          ← Logs de ejecución
```

---

## 🔧 UTILIDADES

### Ejecutar el script de utilidades
```powershell
python UTILS.py
```

**Opciones:**
1. Crear entorno virtual
2. Instalar dependencias
3. Actualizar dependencias
4. Verificar instalación
5. **Ejecutar asistente**
6. Ejecutar ejemplos
7. Ejecutar tests
8. Limpiar cache
9. Resetear entorno
10. Ver configuración
11. Ver estructura
12. Ver logs

---

## 🔌 MÓDULOS (USO AVANZADO)

### AppLauncher
```python
from src.modules.app_launcher import AppLauncher
from src.config import config

launcher = AppLauncher(config)

# Abrir app
success, msg = launcher.open_app("chrome")
print(msg)

# Cerrar app
success, msg = launcher.close_app("chrome")

# Listar apps
apps = launcher.list_available_apps()
```

### WindowManager
```python
from src.modules.window_manager import WindowManager

manager = WindowManager(config)

# Listar ventanas
windows = manager.list_windows()

# Traer al frente
success, msg = manager.bring_to_front("Notepad")

# Minimizar
manager.minimize("Chrome")

# Maximizar
manager.maximize("Excel")
```

### CommandProcessor
```python
from src.modules.command_processor import CommandProcessor

processor = CommandProcessor(config)

# Parsear comando
parsed = processor.parse_command("abre chrome")
print(parsed)
# Output: {'success': True, 'intent': 'open', 'params': ['chrome'], ...}

# Ver historial
history = processor.get_history()

# Agregar comando custom
processor.add_custom_command("backup", "system.backup", ["bak", "copia"])
```

### InputHandler
```python
from src.modules.input_handler import InputHandler

handler = InputHandler(config)

# Obtener input
success, text = handler.get_input()

# Enviar respuesta
handler.respond("Comando completado")

# Solo texto
success, text = handler.get_text_input()

# Solo voz (si está habilitada)
success, text = handler.get_voice_input()
```

---

## ⚙️ CONFIGURACIÓN ESENCIAL

**Archivo:** `src/config/config.py`

```python
# Nombre del asistente
ASSISTANT_NAME = "Diana"

# Entrada/Salida
USE_VOICE_INPUT = False   # True para usar micrófono
USE_VOICE_OUTPUT = False  # True para usar altavoz
USE_TEXT_INPUT = True     # Entrada por teclado
USE_TEXT_OUTPUT = True    # Salida por pantalla

# Voz (si la habilitas)
VOICE_LANGUAGE = "es-ES"  # Idioma
VOICE_RATE = 150          # Velocidad (palabras/min)

# Aplicaciones permitidas (WHITELIST)
ALLOWED_APPS = {
    "notepad": {...},
    "chrome": {...},
    ...
}

# Comandos base
BASE_COMMANDS = {
    "open": {...},
    "close": {...},
    ...
}

# Logging
DEBUG = True
LOG_LEVEL = "INFO"
LOG_FILE = "logs/assistant.log"
```

---

## 🆘 PROBLEMAS COMUNES

### "ModuleNotFoundError: No module named 'win32gui'"
```powershell
pip install --upgrade pywin32
python -m pip install --upgrade pywin32
```

### "SpeechRecognition requires..._"
```powershell
pip install SpeechRecognition pydub
pip install pyaudio  # Si falla en Windows, descargar wheel manualmente
```

### "Application not found"
```python
# 1. Verificar ruta en config.py
# 2. Ejecutar como Admin (Windows)
# 3. Probar con comandos simples (notepad, calculator)
```

### "No permission to execute"
```powershell
# En Windows, ejecutar como Administrador
# Para PowerShell:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📊 FLUJO DE COMANDO TÍPICO

```
Usuario escribe/dice:  "abre chrome"
          ↓
Input Handler captura: "abre chrome"
          ↓
Command Processor parsea: {intent: "open", params: ["chrome"]}
          ↓
Router busca handler:  "app_launcher.open_app"
          ↓
AppLauncher ejecuta:   Chrome se abre
          ↓
Respuesta: "Abierto: chrome"
```

---

## 🎯 ROADMAP DE IMPLEMENTACIÓN

### Semana 1: Setup ✅
- [x] Instalar dependencias
- [x] Ejecutar asistente
- [x] Probar comandos básicos
- [ ] Agregar 3+ aplicaciones custom

### Semana 2: Voz
- [ ] Habilitar reconocimiento de voz
- [ ] Habilitar síntesis de voz
- [ ] Probar con frases naturales
- [ ] Mejorar detección de intención

### Semana 3: Expansión
- [ ] Agregar 5+ comandos nuevos
- [ ] Crear módulos personalizados
- [ ] Integración con APIs
- [ ] Base de datos de preferencias

### Semana 4: UI
- [ ] GUI básica (Tkinter/PyQt)
- [ ] Dashboard
- [ ] Configurador visual
- [ ] Temas y personalización

### Semana 5+: IA
- [ ] Integración con OpenAI/LLaMA
- [ ] NLP mejorado
- [ ] Learning de patrones
- [ ] Automatización inteligente

---

## 🚀 PRÓXIMO PASO

Ejecuta esto para empezar:

```powershell
cd c:\DESCKTOP\DIANA\ai-assistant
python UTILS.py
# Selecciona opción 1, 2, 4, 5
```

O ejecuta directamente:

```powershell
cd c:\DESCKTOP\DIANA\ai-assistant
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/main.py
```

---

## 📖 RECURSOS

- [Documentación Completa](docs/ARQUITECTURA.md)
- [Guía de Implementación](IMPLEMENTACION.md)
- [Ejemplos de Código](EJEMPLOS.py)
- [Script de Utilidades](UTILS.py)

---

**¡Listo para comenzar! 🚀**

Cualquier pregunta, revisa los logs o la documentación completa.
