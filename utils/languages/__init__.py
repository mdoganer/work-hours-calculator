"""
Languages module for the application.
This module provides translation support for the UI.
"""

from .language_manager import _, set_language, get_language, _language_manager as language_manager

__all__ = ['language_manager', 'get_text', '_']