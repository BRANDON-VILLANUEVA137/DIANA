"""
Language detection module for Diana
Detects input language and handles multi-language processing
"""
from langdetect import detect, DetectorFactory
import logging

# Set seed for consistent results
DetectorFactory.seed = 0

logger = logging.getLogger(__name__)

class LanguageDetector:
    """Detect and manage language for user input"""
    
    def __init__(self, supported_languages=None):
        self.supported_languages = supported_languages or ["es", "en"]
        self.language_names = {
            "es": "Spanish",
            "en": "English"
        }
    
    def detect_language(self, text):
        """
        Detect the language of the input text
        
        Args:
            text (str): Input text to analyze
            
        Returns:
            tuple: (language_code, confidence)
        """
        try:
            # Ensure text is not empty
            if not text or len(text.strip()) < 2:
                logger.warning("Input text too short for reliable detection")
                return "en", 0.5
            
            # Detect language
            detected_lang = detect(text)
            
            # Validate against supported languages
            if detected_lang in self.supported_languages:
                logger.info(f"Detected language: {detected_lang} ({self.language_names.get(detected_lang, 'Unknown')})")
                return detected_lang, 0.95
            else:
                logger.warning(f"Detected {detected_lang}, not in supported languages. Defaulting to English")
                return "en", 0.5
                
        except Exception as e:
            logger.error(f"Error detecting language: {e}")
            return "en", 0.5  # Default to English
    
    def get_language_name(self, language_code):
        """Get human-readable language name"""
        return self.language_names.get(language_code, "Unknown")
    
    def is_spanish(self, text):
        """Check if text is in Spanish"""
        lang, _ = self.detect_language(text)
        return lang == "es"
    
    def is_english(self, text):
        """Check if text is in English"""
        lang, _ = self.detect_language(text)
        return lang == "en"
