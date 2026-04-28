# Migración Gemini → Groq - TODO

- [x] 1. Analizar archivos relevantes (ai_processor.py, config.py, main.py, requirements.txt)
- [x] 2. Actualizar requirements.txt (eliminar google-genai, agregar groq)
- [x] 3. Actualizar src/config/config.py (GROQ_API_KEY, modelo, validaciones)
- [x] 4. Refactorizar src/modules/ai_processor.py (cliente Groq, chat.completions, historial, reintentos)
- [x] 5. Actualizar src/main.py (imports, referencias a Gemini → Groq)
- [x] 6. Actualizar test_diana.py (imports, referencias a Gemini → Groq)
- [x] 7. Verificar que no queden referencias residuales a Gemini
- [x] 8. Finalizar

