# utils/file_utils.py
from pathlib import Path
import platform

# Global variable to store the custom file path
custom_file_path = None

def get_file_path():
    """
    Determine the universal file path based on the operating system or use custom path if set.
    Returns either the custom file path (if set) or the default path.
    """
    # First check if there's a path in preferences
    try:
        from gui.preferences import preferences
        pref_path = preferences.get("file_path")
        if pref_path:
            return Path(pref_path)
    except ImportError:
        # Module might not be available during initial import
        pass
    
    # If a custom file path has been set via the setter, return it
    global custom_file_path
    if custom_file_path is not None:
        return custom_file_path
    
    # Otherwise return the default path based on the operating system
    if platform.system() == "Windows":
        # Use AppData\Local for Windows
        app_dir = Path.home() / "AppData" / "Local" / "WorkHoursCalculator"
    else:
        # Use ~/.calisma_saati_hesaplama for Linux/Mac
        app_dir = Path.home() / ".work_hours_calculator"

    app_dir.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist
    return app_dir / "work_record.json"

def set_custom_file_path(path):
    """Set a custom file path to be used instead of the default."""
    global custom_file_path
    if path:
        custom_file_path = Path(path)
    else:
        custom_file_path = None
    return custom_file_path