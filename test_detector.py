import sys
sys.path.insert(0, 'src')
from modules.language_detector import LanguageDetector

detector = LanguageDetector()

test_cases = [
    "Hola, ¿cómo estás?",
    "Hello, how are you?",
    "¿Cuál es tu nombre?"
]

for text in test_cases:
    lang, conf = detector.detect_language(text)
    print(f"'{text}' -> {lang.upper()} ({conf:.0%})")
