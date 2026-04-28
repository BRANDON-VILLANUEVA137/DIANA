#!/usr/bin/env python3
"""
Diana - Virtual Assistant with Multi-Language Support
Supports Spanish and English input, responds in English
"""

import os
import sys
import logging
from pathlib import Path
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from config.config import (
    GROQ_API_KEY, ELEVENLABS_API_KEY, SYSTEM_PROMPT,
    USE_VOICE_INPUT, USE_VOICE_OUTPUT, ALLOWED_APPS,
    LOG_FILE, LOG_LEVEL, AI_MODEL, ASSISTANT_NAME, ASSISTANT_VERSION,
    DATA_FILE, ELEVENLABS_VOICE_ID, validate_api_keys, update_env_variable
)
from modules.language_detector import LanguageDetector
from modules.ai_processor import AIProcessor
from modules.voice_handler import VoiceHandler
from modules.command_processor import CommandProcessor

# Configure logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class DianaAssistant:
    """Main Diana Virtual Assistant class"""
    
    def __init__(self):
        """Initialize the assistant"""
        # Store dynamic assistant name
        self.assistant_name = ASSISTANT_NAME
        
        logger.info(f"Initializing {self.assistant_name} v{ASSISTANT_VERSION}")
        
        # Validate API keys
        if not validate_api_keys():
            print(f"{Fore.YELLOW}Some features may not work without proper API keys.{Style.RESET_ALL}")
        
        # Initialize components
        self.language_detector = LanguageDetector()
        self.ai_processor = AIProcessor(
            api_key=GROQ_API_KEY,
            model=AI_MODEL,
            system_prompt=SYSTEM_PROMPT
        )
        self.command_processor = CommandProcessor(allowed_apps=ALLOWED_APPS)
        
        # Initialize voice if API key is available
        self.voice_handler = None
        if USE_VOICE_OUTPUT and ELEVENLABS_API_KEY:
            try:
                self.voice_handler = VoiceHandler(
                    api_key=ELEVENLABS_API_KEY,
                    voice_id=ELEVENLABS_VOICE_ID
                )
                # Check if voice handler was initialized successfully
                if self.voice_handler.client is None:
                    logger.warning("Voice handler not fully initialized, voice output disabled")
                    self.voice_handler = None
            except Exception as e:
                logger.warning(f"Voice handler initialization failed: {e}")
                self.voice_handler = None
        
        self.running = True
        logger.info(f"{self.assistant_name} initialized successfully")
    
    def print_header(self):
        """Print welcome header"""
        print(f"\n{Fore.CYAN}╔════════════════════════════════════════════════════════════════╗{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║  {self.assistant_name} - Virtual Assistant v{ASSISTANT_VERSION:<20} ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}║  Multi-Language Input | English Output                         ║{Style.RESET_ALL}")
        print(f"{Fore.CYAN}╚════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}\n")
    
    def get_user_input(self):
        """Get input from user"""
        try:
            user_input = input(f"{Fore.GREEN}You: {Style.RESET_ALL}").strip()
            return user_input
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Interrupted by user{Style.RESET_ALL}")
            self.running = False
            return None
        except EOFError:
            self.running = False
            return None
    
    def process_user_input(self, user_input):
        """Process user input through language detection and AI"""
        if not user_input:
            return
        
        # Detect language
        detected_lang, confidence = self.language_detector.detect_language(user_input)
        lang_name = self.language_detector.get_language_name(detected_lang)
        
        print(f"{Fore.BLUE}[Detected: {lang_name} ({confidence:.0%})]{Style.RESET_ALL}")
        
        user_lower = user_input.lower().strip()
        
        # ==================== CHECK FOR NAME-RELATED QUERIES ====================
        # Keywords for asking about the assistant's name
        name_question_keywords = [
            # English
            "what is your name", "what's your name", "who are you", "who am i talking to",
            "tell me your name", "your name", "what do you call yourself", "what name do you have",
            # Spanish
            "cuál es tu nombre", "cual es tu nombre", "quién eres", "quien eres", 
            "cómo te llamas", "como te llamas", "dime tu nombre", "tu nombre",
            "cuál es mi nombre", "cual es mi nombre"
        ]
        
        # Check if asking for name
        if any(keyword in user_lower for keyword in name_question_keywords):
            response = f"My name is {self.assistant_name}. I am a virtual assistant powered by Groq and ElevenLabs. You can change my name anytime by saying 'call me [new name]'."
            print(f"{Fore.CYAN}{self.assistant_name}: {response}{Style.RESET_ALL}")
            if USE_VOICE_OUTPUT and self.voice_handler:
                self.voice_handler.speak(response)
            return
        
        # ==================== CHECK FOR NAME CHANGE COMMANDS ====================
        # Keywords for changing the assistant's name
        change_name_keywords = [
             # English
            "i want to call you", "rename yourself", "your name is now",
            "i will call you", "you are now called",

            # Spanish
            "quiero llamarte", "te voy a llamar", "tu nombre ahora es",
            "ahora te llamas", "te llamaré"
        ]
        
        change_name_match = None
        for keyword in change_name_keywords:
            if keyword in user_lower:
                change_name_match = keyword
                break
        
        if change_name_match:
            # Extract new name from user input
            idx = user_lower.find(change_name_match)
            potential_name = user_input[idx + len(change_name_match):].strip()
            
            # Clean up the name
            if potential_name:
                # Remove trailing punctuation
                potential_name = potential_name.rstrip('.!?,;:')
                
                # Remove common words at the beginning
                common_prefixes = ["the ", "a ", "my ", "your ", "the name ", "you ", "me "]
                for prefix in common_prefixes:
                    if potential_name.lower().startswith(prefix):
                        potential_name = potential_name[len(prefix):].strip()
                
                # Ensure name is not empty and reasonable length (2-50 characters)
                if potential_name and 2 <= len(potential_name) <= 50:
                    old_name = self.assistant_name
                    self.assistant_name = potential_name
                    
                    # Update .env file
                    success = update_env_variable("ASSISTANT_NAME", self.assistant_name)
                    
                    if success:
                        response = f"Thank you! You can now call me {self.assistant_name}. I will remember this name. My previous name was {old_name}."
                        logger.info(f"Assistant name changed from '{old_name}' to '{self.assistant_name}' (saved to .env)")
                    else:
                        response = f"I've updated my name to {self.assistant_name} in this session, but I couldn't save it permanently. Please try again."
                        logger.warning(f"Failed to save new name '{self.assistant_name}' to .env file")
                    
                    print(f"{Fore.CYAN}{self.assistant_name}: {response}{Style.RESET_ALL}")
                    if USE_VOICE_OUTPUT and self.voice_handler:
                        self.voice_handler.speak(response)
                    return
                else:
                    response = "The name you provided is too short or too long. Please try again with a name between 2 and 50 characters."
                    print(f"{Fore.CYAN}{self.assistant_name}: {response}{Style.RESET_ALL}")
                    return
            
            # If no valid name extracted
            response = "I didn't catch your new name. Please try again with 'call me [new name]' or 'rename me to [new name]'"
            print(f"{Fore.CYAN}{self.assistant_name}: {response}{Style.RESET_ALL}")
            return
        
        # Check if it's a command
        parsed_command = self.command_processor.parse_command(user_input, detected_lang)
        
        if parsed_command["type"] == "open":
            # Execute application open command
            result = self.command_processor.execute_command(parsed_command)
            if result.get("success"):
                response = result.get("message", "Command executed")
                print(f"{Fore.CYAN}{self.assistant_name}: {response}{Style.RESET_ALL}")
            else:
                response = result.get("message", "Could not execute command")
                print(f"{Fore.RED}{self.assistant_name}: {response}{Style.RESET_ALL}")
        
        elif parsed_command["type"] == "close":
            result = self.command_processor.execute_command(parsed_command)
            response = result.get("message", "Command executed")
            print(f"{Fore.CYAN}{self.assistant_name}: {response}{Style.RESET_ALL}")
        
        elif parsed_command["type"] == "help":
            result = self.command_processor.execute_command(parsed_command)
            print(f"{Fore.CYAN}{self.assistant_name}: {result.get('message')}{Style.RESET_ALL}")
        
        elif parsed_command["type"] == "list":
            result = self.command_processor.execute_command(parsed_command)
            print(f"{Fore.CYAN}{self.assistant_name}: {result.get('message')}{Style.RESET_ALL}")
        
        elif parsed_command["type"] == "exit":
            self.running = False
            print(f"{Fore.CYAN}{self.assistant_name}: Goodbye! Have a great day!{Style.RESET_ALL}")
        
        else:
            # Process as natural language query with AI
            ai_response = self.ai_processor.process_input(user_input, detected_lang)
            
            if ai_response["success"]:
                response_text = ai_response["content"]
                print(f"{Fore.CYAN}{self.assistant_name}: {response_text}{Style.RESET_ALL}")
                
                # Speak response if voice output is enabled
                if USE_VOICE_OUTPUT and self.voice_handler:
                    self.voice_handler.speak(response_text)
            else:
                error_msg = ai_response.get("error", "Unknown error")
                print(f"{Fore.RED}{self.assistant_name}: Error processing request: {error_msg}{Style.RESET_ALL}")
    
    def run(self):
        """Main run loop"""
        self.print_header()
        
        print(f"{Fore.GREEN}Type 'help' for commands or 'exit' to quit.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}You can speak in Spanish or English!\n{Style.RESET_ALL}")
        
        while self.running:
            try:
                user_input = self.get_user_input()
                
                if user_input:
                    self.process_user_input(user_input)
                
            except Exception as e:
                logger.error(f"Error in main loop: {e}")
                print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        
        # Save conversation history
        if self.ai_processor.conversation_history:
            self.ai_processor.save_history(DATA_FILE)
        
        logger.info("Diana assistant stopped")
        print(f"\n{Fore.YELLOW}Thank you for using {self.assistant_name}!{Style.RESET_ALL}")
    
    def test_setup(self):
        """Test the assistant setup"""
        print(f"\n{Fore.CYAN}Testing {ASSISTANT_NAME} Setup...{Style.RESET_ALL}\n")
        
        # Test language detection
        print(f"{Fore.YELLOW}1. Testing Language Detection:{Style.RESET_ALL}")
        test_spanish = "Hola, ¿cómo estás?"
        test_english = "Hello, how are you?"
        
        lang_es, conf_es = self.language_detector.detect_language(test_spanish)
        lang_en, conf_en = self.language_detector.detect_language(test_english)
        
        print(f"   Spanish text: {lang_es.upper()} ({conf_es:.0%}) ✓")
        print(f"   English text: {lang_en.upper()} ({conf_en:.0%}) ✓")
        
        # Test AI processor
        print(f"\n{Fore.YELLOW}2. Testing AI Processor:{Style.RESET_ALL}")
        if GROQ_API_KEY:
            test_response = self.ai_processor.process_input("Hello, who are you?", "en")
            if test_response["success"]:
                print(f"   ✓ AI Response: {test_response['content'][:50]}...")
            else:
                print(f"   ✗ AI Error: {test_response.get('error')}")
        else:
            print(f"   ✗ Groq API key not configured")
        
        # Test voice handler
        print(f"\n{Fore.YELLOW}3. Testing Voice Handler:{Style.RESET_ALL}")
        if self.voice_handler:
            print(f"   ✓ Voice handler ready")
            print(f"   Voice ID: {ELEVENLABS_VOICE_ID}")
        else:
            print(f"   ✗ Voice handler not available")
        
        # Test command processor
        print(f"\n{Fore.YELLOW}4. Testing Command Processor:{Style.RESET_ALL}")
        test_cmd = self.command_processor.parse_command("open notepad", "en")
        print(f"   ✓ Parsed command: {test_cmd['type']} → {test_cmd.get('target', 'N/A')}")
        
        print(f"\n{Fore.GREEN}Setup test complete!{Style.RESET_ALL}\n")

def main():
    """Main entry point"""
    try:
        # Check for test flag
        if len(sys.argv) > 1 and sys.argv[1] == "--test":
            assistant = DianaAssistant()
            assistant.test_setup()
        else:
            assistant = DianaAssistant()
            assistant.run()
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Interrupted by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"{Fore.RED}Fatal error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
