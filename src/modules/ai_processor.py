"""
AI Processing module for Diana
Handles Groq API integration for natural language processing
"""
import json
import logging
import time
from datetime import datetime
from groq import Groq

logger = logging.getLogger(__name__)

class AIProcessor:
    """Process natural language using Groq"""
    
    def __init__(self, api_key, model="llama-3.1-8b-instant", system_prompt=""):
        """
        Initialize AI Processor
        
        Args:
            api_key (str): Groq API key
            model (str): Model to use
            system_prompt (str): System prompt for the AI
        """
        self.api_key = api_key
        self.model_name = model
        self.system_prompt = system_prompt
        self.conversation_history = []
        self.max_history = 10
        
        # Configure Groq client
        self.client = Groq(api_key=api_key)
        
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
            
            # Build messages for Groq API
            messages = self._build_messages(language)
            
            # Call Groq API with retry logic
            response_text = self._call_groq_api(messages)
            
            if not response_text:
                return {
                    "success": False,
                    "content": "No response generated",
                    "error": "Empty response from API"
                }
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text,
                "timestamp": datetime.now().isoformat()
            })
            
            logger.info(f"AI response generated for input in {language}")
            
            return {
                "success": True,
                "content": response_text,
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
    
    def _build_messages(self, language):
        """Build messages list for Groq chat completions API"""
        messages = []
        
        # Add system prompt
        system_content = self.system_prompt
        if language:
            system_content += f"\n\nThe user is writing in {language}. Respond in English only."
        
        messages.append({
            "role": "system",
            "content": system_content
        })
        
        # Add conversation history (only role and content for API)
        for msg in self.conversation_history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        return messages
    
    def _call_groq_api(self, messages, max_retries=3):
        """
        Call Groq API with retry logic
        
        Args:
            messages (list): List of message dicts for the API
            max_retries (int): Maximum number of retry attempts
            
        Returns:
            str: Generated response text
        """
        last_exception = None
        
        for attempt in range(1, max_retries + 1):
            try:
                logger.debug(f"Groq API call attempt {attempt}/{max_retries}")
                
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    temperature=0.7,
                    max_tokens=2048,
                    timeout=30
                )
                
                if response.choices and len(response.choices) > 0:
                    content = response.choices[0].message.content
                    if content:
                        return content.strip()
                
                logger.warning("Empty response from Groq API")
                return ""
                
            except Exception as e:
                last_exception = e
                logger.warning(f"Groq API attempt {attempt} failed: {e}")
                
                if attempt < max_retries:
                    wait_time = 2 ** attempt  # Exponential backoff: 2, 4, 8 seconds
                    logger.info(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"All {max_retries} attempts failed. Last error: {e}")
        
        # If we get here, all retries failed
        raise last_exception if last_exception else Exception("Unknown API error")
    
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

