from pathlib import Path
import platform

def get_file_path():
    """Determine the universal file path based on the operating system."""
    if platform.system() == "Windows":
        # Use AppData\Local for Windows
        app_dir = Path.home() / "AppData" / "Local" / "CalismaSaatiHesaplama"
    else:
        # Use ~/.calisma_saati_hesaplama for Linux/Mac
        app_dir = Path.home() / ".calisma_saati_hesaplama"

    app_dir.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist
    return app_dir / "calisma_kaydi.json"