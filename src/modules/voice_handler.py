"""
Voice handling module for Diana
Manages text-to-speech with ElevenLabs API
"""
import logging

logger = logging.getLogger(__name__)

# Try to import elevenlabs, but make it optional
try:
    from elevenlabs.client import ElevenLabs
    ELEVENLABS_AVAILABLE = True
except Exception as e:
    logger.warning(f"ElevenLabs not available: {e}")
    ELEVENLABS_AVAILABLE = False
    ElevenLabs = None

class VoiceHandler:
    """Handle voice input/output with ElevenLabs"""
    
    def __init__(self, api_key, voice_id="EXAVITQu4vr4xnSDxMaL"):
        """
        Initialize Voice Handler
        
        Args:
            api_key (str): ElevenLabs API key
            voice_id (str): ElevenLabs voice ID to use
        """
        if not ELEVENLABS_AVAILABLE:
            logger.warning("ElevenLabs library not available. Voice synthesis disabled.")
            self.client = None
            self.api_key = None
            self.voice_id = None
            return
        
        try:
            self.api_key = api_key
            self.voice_id = voice_id
            self.client = ElevenLabs(api_key=api_key)
            logger.info(f"Voice Handler initialized with voice ID: {voice_id}")
        except Exception as e:
            logger.warning(f"Failed to initialize ElevenLabs client: {e}")
            self.client = None
    
    def speak(self, text, auto_play=True):
        """
        Convert text to speech using ElevenLabs
        
        Args:
            text (str): Text to convert to speech
            auto_play (bool): Whether to auto-play the audio
            
        Returns:
            dict: Audio data and metadata
        """
        if not self.client:
            logger.debug("Voice handler not available, skipping speech synthesis")
            return {
                "success": False,
                "error": "Voice handler not initialized"
            }
        
        try:
            if not text or len(text.strip()) == 0:
                logger.warning("Empty text provided for speech")
                return {
                    "success": False,
                    "error": "Empty text"
                }
            
            logger.info(f"Converting text to speech: {text[:50]}...")
            
            # Generate audio
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=self.voice_id,
                model_id="eleven_monolingual_v1"
            )
            
            # Convert audio stream to bytes
            audio_bytes = b"".join(audio)
            
            # Auto-play if requested
            if auto_play:
                self.play_audio(audio_bytes)
            
            logger.info("Speech generated successfully")
            
            return {
                "success": True,
                "audio_bytes": audio_bytes,
                "text": text
            }
            
        except Exception as e:
            logger.error(f"Error generating speech: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def play_audio(self, audio_bytes):
        """
        Play audio bytes
        
        Args:
            audio_bytes (bytes): Audio data to play
        """
        try:
            # Note: The play function from elevenlabs expects a generator
            # We need to convert bytes back to a generator-like format
            logger.info("Playing audio...")
            # In practice, you might want to use a library like pydub or pygame
            # For now, this is a placeholder for audio playback
            
        except Exception as e:
            logger.error(f"Error playing audio: {e}")
    
    def set_voice(self, voice_id):
        """Change the voice"""
        self.voice_id = voice_id
        logger.info(f"Voice changed to: {voice_id}")
    
    def test_voice(self):
        """Test voice output with a sample phrase"""
        test_text = "Hello! I am Diana, your virtual assistant. I'm ready to help you."
        return self.speak(test_text)
    
    @staticmethod
    def get_available_voices():
        """Get list of available ElevenLabs voices"""
        voices = {
            "EXAVITQu4vr4xnSDxMaL": {"name": "Rachel", "gender": "Female", "accent": "American"},
            "nPczCjzI2devNBz1zQrb": {"name": "Brian", "gender": "Male", "accent": "American"},
            "9BWtsMINqrJLrRacOk9Q": {"name": "Aria", "gender": "Female", "accent": "American"},
            "XB0fDUnXU5powFXDhCwa": {"name": "Sarah", "gender": "Female", "accent": "British"},
            "LFSE5hU29RdP8lSMZYdP": {"name": "Bella", "gender": "Female", "accent": "American"}
        }
        return voices
