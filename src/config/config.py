"""
Configuration module for Diana Virtual Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ==================== API KEYS ====================
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")

# ==================== LANGUAGE SETTINGS ====================
SUPPORTED_LANGUAGES = ["es", "en"]  # Spanish and English
OUTPUT_LANGUAGE = "en"  # Always output in English
INPUT_LANGUAGES = ["es", "en"]  # Accept both languages as input

# ==================== VOICE SETTINGS ====================
USE_VOICE_INPUT = False  # Set to True to enable voice input
USE_VOICE_OUTPUT = True  # Set to True to enable voice output
VOICE_SPEED = 0.1  # Voice speed (0.5 - 2.0)
ELEVENLABS_VOICE_ID = os.getenv("VOICE_ID", "XJ2fW4ybq7HouelYYGcL")  # Default voice ID

# Alternative voice IDs from ElevenLabs:
# - "EXAVITQu4vr4xnSDxMaL" - Rachel (female)
# - "nPczCjzI2devNBz1zQrb" - Brian (male)
# - "9BWtsMINqrJLrRacOk9Q" - Aria (female)

# ==================== AI SETTINGS ====================
AI_MODEL = "llama-3.1-8b-instant"  # Groq model
AI_TEMPERATURE = 0.7  # Creativity level (0.0 - 1.0)
MAX_HISTORY = 10  # Keep last N messages in context

# ==================== SYSTEM SETTINGS ====================
ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "D-I-03367")  # Assistant name (can be changed)
ASSISTANT_VERSION = "2.0"
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FILE = "logs/diana.log"
DATA_FILE = "data/conversation_history.json"

# ==================== APPLICATION SETTINGS ====================
ALLOWED_APPS = {
    "notepad": {
        "paths": [r"C:\Windows\System32\notepad.exe"],
        "aliases": ["block", "editor"],
        "description": "Text editor"
    },
    "calculator": {
        "paths": [r"C:\Windows\System32\calc.exe"],
        "aliases": ["calc", "calculadora"],
        "description": "Calculator"
    },
    "chrome": {
        "paths": [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ],
        "aliases": ["navegador", "browser", "google"],
        "description": "Google Chrome"
    },
    "edge": {
        "paths": [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
        ],
        "aliases": ["microsoft edge", "explorer"],
        "description": "Microsoft Edge"
    }
}

# ==================== SYSTEM PROMPT ====================
SYSTEM_PROMPT = f"""
You are {ASSISTANT_NAME}, a helpful PRAGMATA.

Your name is STRICTLY {ASSISTANT_NAME}.
You must ALWAYS introduce yourself using this exact name.

You always respond in English, even if the user speaks in Spanish or English.
Be concise, friendly, and helpful. Focus on assisting with computer tasks and answering questions.

When the user gives a command like 'open notepad' or 'show windows', acknowledge it clearly.
Format your responses in a clear and organized way.
"""

def validate_api_keys():
    """Validate that required API keys are configured"""
    if not GROQ_API_KEY:
        print("⚠️  WARNING: GROQ_API_KEY not set. Set it in .env file")
        return False
    if USE_VOICE_OUTPUT and not ELEVENLABS_API_KEY:
        print("⚠️  WARNING: ELEVENLABS_API_KEY not set. Voice output disabled.")
        return False
    return True


def update_env_variable(variable_name, value):
    """
    Update or create an environment variable in .env file
    
    Args:
        variable_name (str): Name of the variable
        value (str): New value for the variable
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        from pathlib import Path
        
        # Get the path to .env file (parent directory of this config file)
        env_path = Path(__file__).parent.parent.parent / ".env"
        
        # Read current .env content
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        else:
            lines = []
        
        # Update or add the variable
        variable_found = False
        updated_lines = []
        
        for line in lines:
            if line.startswith(f"{variable_name}="):
                updated_lines.append(f"{variable_name}={value}\n")
                variable_found = True
            else:
                updated_lines.append(line)
        
        # Add variable if it doesn't exist
        if not variable_found:
            updated_lines.append(f"\n{variable_name}={value}\n")
        
        # Write updated content back to .env
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        
        return True
        
    except Exception as e:
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error updating .env file: {e}")
        return False
