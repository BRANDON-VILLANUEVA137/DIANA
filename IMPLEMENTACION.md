# Guía de Implementación y Próximos Pasos

## 📌 GUÍA PASO A PASO PARA COMENZAR

### **PASO 1: Instalación del Entorno (5 minutos)**

#### Windows (Recomendado)
```powershell
# Abrir PowerShell como Administrador

# 1. Navegar a la carpeta del proyecto
cd "c:\DESCKTOP\DIANA\ai-assistant"

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
.\venv\Scripts\Activate.ps1

# Si hay error de permisos, ejecutar:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Instalar pywin32 correctamente (Windows)
pip install pywin32
python -m pip install --upgrade pywin32
python Scripts/pywin32_postinstall.py -install
```

#### Linux/macOS
```bash
cd ~/DIANA/ai-assistant

# Crear entorno virtual
python3 -m venv venv

# Activar
source venv/bin/activate

# Instalar
pip install -r requirements.txt
```

---

### **PASO 2: Verificación Inicial (2 minutos)**

```powershell
# Activar entorno (si no lo está)
.\venv\Scripts\Activate.ps1

# Probar que Python funciona
python --version

# Probar imports
python -c "import win32gui; import pyautogui; print('✓ Dependencias OK')"
```

Si obtienes errores aquí, ejecutar:
```powershell
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

### **PASO 3: Primera Ejecución (1 minuto)**

```powershell
# Desde la carpeta ai-assistant con venv activado
python src/main.py
```

**Esperado:**
```
╔════════════════════════════════════════╗
║   Configuración: Diana v1.0.0
╚════════════════════════════════════════╝

Sistema Operativo: Windows 10
Python: 3.11.x
...
Diana listo.
>
```

---

### **PASO 4: Pruebas Básicas (5 minutos)**

En la consola interactiva que aparece, escribe:

```
> abre notepad
```

**Esperado:** Se abre Notepad y ves:
```
Abierto: notepad (PID: 12345)
```

Otras pruebas:
```
> abre calculator
> ventanas
> ayuda
> trae notepad
> minimiza calculator
> salir
```

---

### **PASO 5: Configuración Personalizada (10 minutos)**

Editar `src/config/config.py`:

**5.1 Agregar tu aplicación favorita:**
```python
ALLOWED_APPS = {
    ...existentes...
    "miapp": {
        "paths": [r"C:\Ruta\Exacta\miapp.exe"],
        "aliases": ["mi", "favorita"],
        "description": "Mi aplicación favorita"
    },
}
```

**5.2 Habilitar entrada de voz (opcional):**
```python
USE_VOICE_INPUT = True    # Cambiar de False a True
USE_VOICE_OUTPUT = True   # Para respuestas habladas
VOICE_LANGUAGE = "es-ES"  # Español
```

Guardar y ejecutar nuevamente:
```powershell
python src/main.py
```

---

### **PASO 6: Exploración de Logs (3 minutos)**

```powershell
# Ver últimas 20 líneas del log
Get-Content "logs\assistant.log" -Tail 20

# O para seguimiento en vivo (Windows PowerShell):
Get-Content "logs\assistant.log" -Wait
```

---

## 🎯 PRÓXIMOS PASOS DE DESARROLLO

### **Semana 1: Estabilización y Pruebas**

- [ ] Probar con 5+ aplicaciones diferentes
- [ ] Verificar gestión de ventanas funciona
- [ ] Revisar logs para errores
- [ ] Documentar aplicaciones que funcionan

**Comando para ejecutar:**
```powershell
python src/main.py 2>&1 | Tee-Object logs\test_run.log
```

### **Semana 2: Extensión Básica**

**Agregar reconocimiento de voz:**
```powershell
# En la consola con venv activado
pip install SpeechRecognition pydub

# Editar config.py
# USE_VOICE_INPUT = True

# Ejecutar
python src/main.py
```

**Probar:**
```
[Micrófono escuchando...]
(Di: "abre chrome")
[Reconocido: "abre chrome"]
Abierto: chrome...
```

### **Semana 3: Comandos Personalizados**

Crear archivo `src/modules/custom_commands.py`:

```python
"""Módulo de comandos personalizados"""

def take_screenshot():
    import pyautogui
    import time
    filename = f"screenshot_{int(time.time())}.png"
    pyautogui.screenshot(filename)
    return True, f"Captura guardada: {filename}"

def open_website(url):
    import subprocess
    subprocess.Popen(f"start {url}", shell=True)
    return True, f"Abriendo {url}"
```

Luego agregar en `main.py`:

```python
# En la sección de action_handlers
self.action_handlers = {
    ...existentes...
    "custom_commands.take_screenshot": self.take_screenshot,
    "custom_commands.open_website": self.open_website,
}
```

Y en `config.py`:

```python
BASE_COMMANDS = {
    ...existentes...
    "screenshot": {
        "aliases": ["captura", "foto"],
        "description": "Toma una captura de pantalla",
        "handler": "custom_commands.take_screenshot",
        "requires_param": False
    }
}
```

### **Semana 4: GUI Simple**

Crear `src/gui.py`:

```python
"""GUI simple con Tkinter"""
import tkinter as tk
from modules.app_launcher import AppLauncher
from config import config

class GUIDiana:
    def __init__(self, root):
        self.launcher = AppLauncher(config)
        
        root.title("Diana Assistant")
        root.geometry("400x300")
        
        # Input
        tk.Label(root, text="Comando:").pack()
        self.input = tk.Entry(root, width=50)
        self.input.pack()
        
        # Botón
        tk.Button(
            root, 
            text="Ejecutar",
            command=self.execute
        ).pack()
        
        # Output
        self.output = tk.Text(root, height=10, width=50)
        self.output.pack()
    
    def execute(self):
        cmd = self.input.get()
        # Procesar comando...
        self.output.insert(tk.END, f"Ejecutado: {cmd}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIDiana(root)
    root.mainloop()
```

Ejecutar:
```powershell
python src/gui.py
```

### **Semana 5+: Integración con IA**

Reemplazar parser simple con OpenAI:

```python
# En command_processor.py
import openai

def parse_with_gpt(user_input):
    openai.api_key = "tu_api_key"
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"Parse this command: '{user_input}'. Return JSON with intent and params."
        }]
    )
    
    return json.loads(response.choices[0].message.content)
```

---

## 🔧 COMANDOS ÚTILES DURANTE DESARROLLO

### Instalar paquetes adicionales
```powershell
pip install pyobjc              # Para macOS
pip install wmctrl xdotool      # Para Linux
pip install openai              # Para GPT
pip install flask               # Para API
pip install pytest              # Para tests
```

### Crear scripts de prueba
```powershell
# Test de módulo individual
python -m pytest tests/test_app_launcher.py -v

# Profiling de rendimiento
python -m cProfile -s cumulative src/main.py
```

### Generar ejecutable (Windows)
```powershell
pip install pyinstaller

# Crear .exe
pyinstaller --onefile --windowed --name Diana src/main.py
```

---

## 📊 CHECKLIST DE IMPLEMENTACIÓN

### ✅ MVP Local (Semana 1)
- [x] Arquitectura definida
- [x] Módulos base implementados
- [x] Búsqueda de aplicaciones funcional
- [x] Gestión de ventanas funcional
- [x] Parser de comandos básico
- [ ] Todas las aplicaciones probadas

### ✅ Voz (Semana 2)
- [ ] Reconocimiento de voz configurado
- [ ] Síntesis de voz funcional
- [ ] Test con frases naturales

### ✅ Extensibilidad (Semana 3)
- [ ] Módulo de comandos personalizados
- [ ] Sistema de plugins
- [ ] Base de datos de comandos

### ✅ UI (Semana 4)
- [ ] GUI básica con Tkinter
- [ ] Dashboard de estado
- [ ] Gestor de configuración visual

### ✅ IA (Semana 5+)
- [ ] Integración OpenAI/API
- [ ] NLP mejorado
- [ ] Learning de patrones

---

## 🆘 SOPORTE RÁPIDO

### "El asistente no inicia"
```powershell
# 1. Verificar Python
python --version

# 2. Verificar imports
python -c "from src.config import config; print('OK')"

# 3. Ver error completo
python src/main.py 2>&1 | more

# 4. Limpiar y reinstalar
Remove-Item -Recurse venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### "Aplicación no se abre"
```powershell
# 1. Verificar ruta exacta
Get-Command notepad  # Para una app
dir "C:\Program Files\Google\Chrome\Application\chrome.exe"

# 2. Actualizar config.py con ruta correcta

# 3. Probar directamente
python -c "
from src.modules.app_launcher import AppLauncher
from src.config import config
launcher = AppLauncher(config)
success, msg = launcher.open_app('notepad')
print(msg)
"
```

### "Voz no funciona"
```powershell
# 1. Verificar micrófono
pip install sounddevice numpy
python -c "import sounddevice as sd; print(sd.query_devices())"

# 2. Instalar requerimientos de voz
pip install SpeechRecognition pydub pyaudio

# 3. Verificar idioma
# Cambiar en config.py: VOICE_LANGUAGE = "es-ES"
```

---

**¡Listo para comenzar!** Ejecuta el Paso 1 y reporta cualquier error.
