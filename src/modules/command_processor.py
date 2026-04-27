"""
Command processing module for Diana
Handles command parsing and execution
"""
import logging
import subprocess
import os
from pathlib import Path

logger = logging.getLogger(__name__)

class CommandProcessor:
    """Process and execute commands"""
    
    def __init__(self, allowed_apps=None):
        """
        Initialize Command Processor
        
        Args:
            allowed_apps (dict): Dictionary of allowed applications
        """
        self.allowed_apps = allowed_apps or {}
        self.command_history = []
    
    def parse_command(self, text, language="en"):
        """
        Parse user input to extract command intent
        
        Args:
            text (str): User input text
            language (str): Language of input
            
        Returns:
            dict: Parsed command information
        """
        # Normalize text
        normalized = text.lower().strip()
        
        # Define command keywords
        open_keywords = ["open", "abre", "abrir", "launch", "ejecuta"]
        close_keywords = ["close", "cierra", "cerrar", "quit"]
        help_keywords = ["help", "ayuda", "commands", "comandos"]
        exit_keywords = ["exit", "salir", "quit"]
        list_keywords = ["list", "lista", "show", "muestra"]
        
        # Check for command type
        for keyword in open_keywords:
            if keyword in normalized:
                return {
                    "type": "open",
                    "target": self._extract_target(normalized, keyword),
                    "language": language
                }
        
        for keyword in close_keywords:
            if keyword in normalized:
                return {
                    "type": "close",
                    "target": self._extract_target(normalized, keyword),
                    "language": language
                }
        
        for keyword in help_keywords:
            if keyword in normalized:
                return {"type": "help", "language": language}
        
        for keyword in exit_keywords:
            if keyword in normalized:
                return {"type": "exit", "language": language}
        
        for keyword in list_keywords:
            if keyword in normalized:
                return {
                    "type": "list",
                    "language": language
                }
        
        # Default: treat as general query
        return {
            "type": "query",
            "text": text,
            "language": language
        }
    
    def _extract_target(self, text, keyword):
        """Extract target application/item from text"""
        # Find the keyword and get text after it
        idx = text.find(keyword)
        if idx != -1:
            target = text[idx + len(keyword):].strip()
            return target
        return ""
    
    def execute_command(self, command):
        """
        Execute a parsed command
        
        Args:
            command (dict): Parsed command
            
        Returns:
            dict: Execution result
        """
        try:
            cmd_type = command.get("type")
            
            if cmd_type == "open":
                return self._execute_open(command.get("target"))
            elif cmd_type == "close":
                return self._execute_close(command.get("target"))
            elif cmd_type == "help":
                return self._execute_help()
            elif cmd_type == "exit":
                return {"type": "exit", "message": "Goodbye!"}
            elif cmd_type == "list":
                return self._execute_list()
            else:
                return {"type": "query", "command": command}
            
        except Exception as e:
            logger.error(f"Error executing command: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _execute_open(self, app_name):
        """Open an application"""
        if not app_name:
            return {"success": False, "message": "No application specified"}
        
        # Find the application
        app_name_lower = app_name.lower().strip()
        
        for app_key, app_info in self.allowed_apps.items():
            # Check by name
            if app_key in app_name_lower:
                return self._launch_app(app_info)
            
            # Check by aliases
            for alias in app_info.get("aliases", []):
                if alias.lower() in app_name_lower:
                    return self._launch_app(app_info)
        
        return {
            "success": False,
            "message": f"Application '{app_name}' not found in allowed apps"
        }
    
    def _launch_app(self, app_info):
        """Launch an application"""
        paths = app_info.get("paths", [])
        
        for path in paths:
            if os.path.exists(path):
                try:
                    subprocess.Popen(path)
                    logger.info(f"Launched: {path}")
                    return {
                        "success": True,
                        "message": f"Opened {app_info.get('description', 'application')}"
                    }
                except Exception as e:
                    logger.error(f"Error launching {path}: {e}")
                    continue
        
        return {
            "success": False,
            "message": f"Could not launch application: {app_info.get('description')}"
        }
    
    def _execute_close(self, app_name):
        """Close an application (placeholder)"""
        return {
            "success": True,
            "message": f"Close command for '{app_name}' would be executed"
        }
    
    def _execute_help(self):
        """Show help information"""
        help_text = """
Available Commands:
- open <app>: Open an application (e.g., "open notepad")
- close <app>: Close an application
- list: List available applications
- help: Show this help message
- exit: Close the assistant

Supported Applications:
"""
        for app_key, app_info in self.allowed_apps.items():
            help_text += f"\n  - {app_info['description']}: {app_key}, {', '.join(app_info['aliases'])}"
        
        return {
            "success": True,
            "message": help_text
        }
    
    def _execute_list(self):
        """List available applications"""
        apps_list = "Available applications:\n"
        for app_key, app_info in self.allowed_apps.items():
            apps_list += f"  - {app_info['description']}\n"
        
        return {
            "success": True,
            "message": apps_list
        }
