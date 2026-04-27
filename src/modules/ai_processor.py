"""
AI Processing module for Diana
Handles Google Gemini API integration for natural language processing
"""
import json
import logging
from datetime import datetime
import google.generativeai as genai

logger = logging.getLogger(__name__)

class AIProcessor:
    """Process natural language using Google Gemini"""
    
    def __init__(self, api_key, model="gemini-2.0-flash", system_prompt=""):
        """
        Initialize AI Processor
        
        Args:
            api_key (str): Google API key
            model (str): Model to use
            system_prompt (str): System prompt for the AI
        """
        self.api_key = api_key
        self.model_name = model
        self.system_prompt = system_prompt
        self.conversation_history = []
        self.max_history = 10
        
        # Configure Gemini API
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        
        logger.info(f"AI Processor initialized with model: {model}")
    
    def process_input(self, user_input, language="en"):
        """
        Process user input with context
        
        Args:
            user_input (str): User's input text
            language (str): Detected language of input
            
        Returns:
            dict: Response with content and metadata
        """
        try:
            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": user_input,
                "language": language,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep conversation history manageable
            if len(self.conversation_history) > self.max_history:
                self.conversation_history = self.conversation_history[-self.max_history:]
            
            # Prepare context from history
            context = self._build_context()
            
            # Create full prompt
            full_prompt = f"{self.system_prompt}\n\nUser message (in {language}): {user_input}\n\nRespond in English only."
            
            if context:
                full_prompt = f"{context}\n\n{full_prompt}"
            
            # Call Gemini API
            response = self.model.generate_content(full_prompt)
            
            if not response.text:
                return {
                    "success": False,
                    "content": "No response generated",
                    "error": "Empty response from API"
                }
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response.text,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"AI response generated for input in {language}")
            
            return {
                "success": True,
                "content": response.text,
                "input_language": language,
                "output_language": "en"
            }
            
        except Exception as e:
            logger.error(f"Error processing input: {e}")
            return {
                "success": False,
                "content": f"Error: {str(e)}",
                "error": str(e)
            }
    
    def _build_context(self):
        """Build context from conversation history"""
        if len(self.conversation_history) < 2:
            return ""
        
        # Get last few messages for context
        recent_messages = self.conversation_history[-4:-1]  # Exclude current user message
        
        context = "Previous conversation context:"
        for msg in recent_messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            context += f"\n{role}: {msg['content'][:100]}..."  # Truncate for brevity
        
        return context
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def get_history(self):
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def save_history(self, filepath):
        """Save conversation history to file"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, ensure_ascii=False, indent=2)
            logger.info(f"History saved to {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error saving history: {e}")
            return False
    
    def load_history(self, filepath):
        """Load conversation history from file"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                self.conversation_history = json.load(f)
            logger.info(f"History loaded from {filepath}")
            return True
        except Exception as e:
            logger.error(f"Error loading history: {e}")
            return False
