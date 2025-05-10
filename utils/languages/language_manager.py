"""
Language management module for the application.
This module provides a simple way to load and use translations for all UI strings.
"""
import json
import os
from pathlib import Path

class LanguageManager:
    """Manages translations for the application."""
    
    def __init__(self):
        self.translations = {}
        self.current_language = "tr"  # Default language is Turkish
        self.load_languages()
    
    def load_languages(self):
        """Load all available language files."""
        # Get the directory of this file
        current_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        
        # Load all JSON files in the languages directory
        for file_path in current_dir.glob("*.json"):
            language_code = file_path.stem
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.translations[language_code] = json.load(f)
            except Exception as e:
                print(f"Error loading language file {file_path}: {e}")
    
    def set_language(self, language_code):
        """Set the current language."""
        if language_code in self.translations:
            self.current_language = language_code
            return True
        return False
    
    def get_text(self, key, default=None):
        """Get translated text for a key."""
        # Try to get text in current language
        if self.current_language in self.translations:
            translation = self.translations[self.current_language].get(key)
            if translation:
                return translation
        
        # Fall back to Turkish
        if "tr" in self.translations and self.current_language != "tr":
            translation = self.translations["tr"].get(key)
            if translation:
                return translation
        
        # Return the key or default if not found
        return default if default is not None else key

# Create a singleton instance
_language_manager = LanguageManager()

# Convenience function for getting translations
def _(key, default=None):
    """Get translated text for a key."""
    return _language_manager.get_text(key, default)

# Export the language manager instance
set_language = _language_manager.set_language
get_language = lambda: _language_manager.current_language