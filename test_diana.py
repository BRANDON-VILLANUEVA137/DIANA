#!/usr/bin/env python3
"""
Test script for Diana Virtual Assistant
Verifies all components are working correctly
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from config.config import (
    GROQ_API_KEY, ELEVENLABS_API_KEY, ALLOWED_APPS,
    validate_api_keys
)
from modules.language_detector import LanguageDetector
from modules.ai_processor import AIProcessor
from modules.voice_handler import VoiceHandler
from modules.command_processor import CommandProcessor

def test_language_detection():
    """Test language detection module"""
    print("\n" + "="*50)
    print("TEST 1: Language Detection")
    print("="*50)
    
    detector = LanguageDetector()
    
    test_cases = [
        ("Hola, ¿cómo estás?", "es"),
        ("Hello, how are you?", "en"),
        ("¿Cuál es tu nombre?", "es"),
        ("What is your name?", "en"),
        ("Buenos días", "es"),
        ("Good morning", "en"),
    ]
    
    passed = 0
    for text, expected_lang in test_cases:
        detected_lang, confidence = detector.detect_language(text)
        status = "✓" if detected_lang == expected_lang else "✗"
        print(f"{status} '{text}' → {detected_lang.upper()} ({confidence:.0%})")
        if detected_lang == expected_lang:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)

def test_command_processor():
    """Test command processing module"""
    print("\n" + "="*50)
    print("TEST 2: Command Processing")
    print("="*50)
    
    processor = CommandProcessor(allowed_apps=ALLOWED_APPS)
    
    test_cases = [
        ("open notepad", "open", "notepad"),
        ("abre notepad", "open", "notepad"),
        ("close calculator", "close", "calculator"),
        ("help", "help", None),
        ("list", "list", None),
        ("exit", "exit", None),
    ]
    
    passed = 0
    for text, expected_type, expected_target in test_cases:
        parsed = processor.parse_command(text, "en")
        type_match = parsed.get("type") == expected_type
        target_match = parsed.get("target", "") == expected_target if expected_target else True
        status = "✓" if type_match and target_match else "✗"
        print(f"{status} '{text}' → type={parsed['type']}, target={parsed.get('target', 'N/A')}")
        if type_match and target_match:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(test_cases)}")
    return passed == len(test_cases)

def test_ai_processor():
    """Test AI processor module"""
    print("\n" + "="*50)
    print("TEST 3: AI Processor (Groq)")
    print("="*50)
    
    if not GROQ_API_KEY:
        print("✗ GROQ_API_KEY not configured")
        return False
    
    try:
        processor = AIProcessor(api_key=GROQ_API_KEY)
        
        # Test simple query
        test_input = "What is 2+2?"
        response = processor.process_input(test_input, "en")
        
        if response["success"]:
            print(f"✓ Query: '{test_input}'")
            print(f"  Response: {response['content'][:100]}...")
            return True
        else:
            print(f"✗ Error: {response.get('error')}")
            return False
    
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False

def test_voice_handler():
    """Test voice handler module"""
    print("\n" + "="*50)
    print("TEST 4: Voice Handler (ElevenLabs)")
    print("="*50)
    
    if not ELEVENLABS_API_KEY:
        print("✗ ELEVENLABS_API_KEY not configured")
        return False
    
    try:
        handler = VoiceHandler(api_key=ELEVENLABS_API_KEY)
        print("✓ Voice handler initialized successfully")
        print(f"  Default voice ID: {handler.voice_id}")
        return True
    
    except Exception as e:
        print(f"✗ Exception: {e}")
        return False

def test_configuration():
    """Test configuration"""
    print("\n" + "="*50)
    print("TEST 5: Configuration")
    print("="*50)
    
    print(f"✓ GROQ_API_KEY: {'SET' if GROQ_API_KEY else 'NOT SET'}")
    print(f"✓ ELEVENLABS_API_KEY: {'SET' if ELEVENLABS_API_KEY else 'NOT SET'}")
    print(f"✓ Allowed apps configured: {len(ALLOWED_APPS)}")
    
    for app_name, app_info in ALLOWED_APPS.items():
        print(f"  - {app_info['description']} ({app_name})")
    
    return validate_api_keys()

def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("DIANA VIRTUAL ASSISTANT - TEST SUITE")
    print("="*60)
    
    results = {
        "Language Detection": test_language_detection(),
        "Command Processing": test_command_processor(),
        "AI Processor": test_ai_processor(),
        "Voice Handler": test_voice_handler(),
        "Configuration": test_configuration(),
    }
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ All tests passed! Diana is ready to use.")
        return 0
    else:
        print(f"\n✗ {total - passed} test(s) failed. Check configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(run_all_tests())
