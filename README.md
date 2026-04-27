# Asistente de IA Local - Diana

Un asistente de IA funcional, local y extensible para automatizar tareas en Windows, Linux y macOS.

## 🚀 Inicio Rápido

### 1. Instalación de Dependencias
```bash
cd ai-assistant
pip install -r requirements.txt
```

### 2. Ejecución Inicial
```bash
python src/main.py
```

### 3. Prueba Básica
Una vez ejecutado, prueba estos comandos:
- `abre block` → Abre el Notepad
- `abre calculadora` → Abre la Calculadora
- `ventanas` → Lista ventanas abiertas
- `ayuda` → Muestra comandos disponibles
- `salir` → Cierra el asistente

---

## 📂 Estructura del Proyecto

```
ai-assistant/
│
├── docs/
│   └── ARQUITECTURA.md          # Documentación completa de arquitectura
│
├── src/
│   ├── main.py                  # Script principal (punto de entrada)
│   │
│   ├── config/
│   │   └── config.py            # Configuración centralizada
│   │
│   └── modules/
│       ├── app_launcher.py      # Búsqueda y ejecución de apps
│       ├── window_manager.py    # Gestión de ventanas
│       ├── command_processor.py # Parse de comandos
│       └── input_handler.py     # Entrada de voz/texto
│
├── logs/                         # Logs de ejecución (generado automáticamente)
├── data/                         # Datos y historial (generado automáticamente)
│
├── requirements.txt             # Dependencias Python
└── README.md                    # Este archivo
```

---

## ⚙️ Configuración

Editar `src/config/config.py` para:

### Habilitar Input de Voz
```python
USE_VOICE_INPUT = True   # Cambiar a True
```

### Habilitar Output de Voz
```python
USE_VOICE_OUTPUT = True  # Cambiar a True
VOICE_LANGUAGE = "es-ES" # Idioma
```

### Agregar Aplicaciones Permitidas
```python
ALLOWED_APPS = {
    "mi_app": {
        "paths": [r"C:\Ruta\a\mi_app.exe"],
        "aliases": ["app"],
        "description": "Mi aplicación"
    },
    ...
}
```

---

## 🎮 Comandos Disponibles

| Comando | Alias | Descripción | Ejemplo |
|---------|-------|-------------|---------|
| `open` | abre, abrir | Abre una aplicación | `abre microsoft edge` |
| `close` | cierra, cerrar | Cierra una aplicación | `cierra block` |
| `window_list` | ventanas | Lista ventanas abiertas | `ventanas` |
| `bring_to_front` | trae, muestra | Trae ventana al frente | `trae microsoft edge` |
| `minimize` | minimiza | Minimiza una ventana | `minimiza calculadora` |
| `help` | ayuda | Muestra ayuda | `ayuda` |

---

## 🔌 Integración de Módulos

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
