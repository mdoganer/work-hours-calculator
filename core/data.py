# core/data.py
import json
from datetime import datetime
from pathlib import Path
from utils.file_utils import get_file_path

def save_record(sicil_no, data_cache, custom_path=None):
    """Save a record to the JSON file."""
    date = datetime.now().strftime("%Y-%m-%d")
    record = {
        "sicil": sicil_no,
        "tarih": date,
        "giris": data_cache["entry"].strftime("%H:%M"),
        "cikis": data_cache["exit"].strftime("%H:%M"),
        "net_calisma": data_cache["net_duration"].total_seconds() / 3600
    }

    # Get the file path (custom or default)
    if custom_path:
        file_path = Path(custom_path)
    else:
        file_path = get_file_path()

    # Read existing data or initialize an empty list
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            records = json.load(f)
    else:
        records = []

    # Append the new record and save it
    records.append(record)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=4, ensure_ascii=False)
    
    return file_path

def load_records():
    """Load all records from the JSON file."""
    file_path = get_file_path()
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def filter_by_badge(data, badge_number):
    """Filter records for the given badge number."""
    return [record for record in data if record['sicil'] == badge_number]

def create_new_file(file_path):
    """Create a new JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump([], f, indent=4, ensure_ascii=False)
    return file_path

def open_json_file(file_path):
    """Open a JSON file and return its data."""
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def delete_record(sicil, tarih, giris, cikis, custom_path=None):
    """Delete a specific record from the JSON file.
    
    Args:
        sicil: Badge number
        tarih: Date of the record
        giris: Entry time
        cikis: Exit time
        custom_path: Optional custom file path
    
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        # Get the file path (custom or default)
        if custom_path:
            file_path = Path(custom_path)
        else:
            file_path = get_file_path()
            
        if not file_path.exists():
            return False
        
        # Read existing data
        with open(file_path, "r", encoding="utf-8") as f:
            records = json.load(f)
        
        # Find and remove the matching record
        original_length = len(records)
        records = [r for r in records if not (r.get('sicil') == sicil and 
                                             r.get('tarih') == tarih and 
                                             r.get('giris') == giris and 
                                             r.get('cikis') == cikis)]
        
        # If no record was removed, return False
        if len(records) == original_length:
            return False
        
        # Save the updated records
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=4, ensure_ascii=False)
            
        return True
    except Exception:
        return False