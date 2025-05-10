# gui/preferences.py
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import platform
from pathlib import Path

class PreferencesManager:
    """Manage application preferences."""
    
    DEFAULT_PREFERENCES = {
        "language": "tr",  # Default language (Turkish)
        "rounding_algorithm": "standard",  # Standard 15-minute rounding
        "breaks": {
            "weekday": {
                "lunch": {"start_time": "13:00", "end_time": "13:45", "enabled": True},
                "dinner": {"start_time": "19:00", "end_time": "19:30", "enabled": True}
            },
            "weekend": {
                "lunch": {"start_time": "13:00", "end_time": "13:30", "enabled": True},
                "dinner": {"start_time": "19:00", "end_time": "19:30", "enabled": True}
            }
        }
    }
    
    def __init__(self):
        self.preferences = self.load_preferences()
    
    def get_preferences_path(self):
        """Get the path to the preferences file."""
        # Use different paths based on the operating system
        if platform.system() == "Windows":
            # Store preferences in AppData\Local for Windows
            app_dir = Path.home() / "AppData" / "Local" / "CalismaSaatiHesaplama"
        else:
            # Store preferences in ~/.calisma_saati_hesaplama for Linux/Mac
            app_dir = Path.home() / ".calisma_saati_hesaplama"
        
        # Create directory if it doesn't exist
        app_dir.mkdir(exist_ok=True, parents=True)
        
        return app_dir / "preferences.json"
    
    def load_preferences(self):
        """Load preferences from file or use defaults."""
        try:
            preferences_path = self.get_preferences_path()
            if preferences_path.exists():
                with open(preferences_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            return self.DEFAULT_PREFERENCES.copy()
        except Exception:
            # If there's any error, return defaults
            return self.DEFAULT_PREFERENCES.copy()
    
    def save_preferences(self):
        """Save current preferences to file."""
        try:
            preferences_path = self.get_preferences_path()
            with open(preferences_path, "w", encoding="utf-8") as f:
                json.dump(self.preferences, f, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def get(self, key, default=None):
        """Get a preference value."""
        return self.preferences.get(key, default)
    
    def set(self, key, value):
        """Set a preference value."""
        self.preferences[key] = value
        return self.save_preferences()
        
    def get_break_info(self, break_type, is_weekday=True):
        """Get break information based on day type.
        
        Args:
            break_type: Type of break (lunch or dinner)
            is_weekday: True for weekday, False for weekend
        """
        day_type = "weekday" if is_weekday else "weekend"
        breaks = self.preferences.get("breaks", {})
        day_breaks = breaks.get(day_type, {})
        return day_breaks.get(break_type, {})
    
    def set_break_info(self, break_type, start_time, end_time, enabled, is_weekday=True):
        """Set break information for specific day type.
        
        Args:
            break_type: Type of break (lunch or dinner)
            start_time: Start time of break (HH:MM)
            end_time: End time of break (HH:MM)
            enabled: Whether break is enabled
            is_weekday: True for weekday, False for weekend
        """
        day_type = "weekday" if is_weekday else "weekend"
        
        if "breaks" not in self.preferences:
            self.preferences["breaks"] = {}
            
        if day_type not in self.preferences["breaks"]:
            self.preferences["breaks"][day_type] = {}
            
        if break_type not in self.preferences["breaks"][day_type]:
            self.preferences["breaks"][day_type][break_type] = {}
            
        self.preferences["breaks"][day_type][break_type] = {
            "start_time": start_time,
            "end_time": end_time,
            "enabled": enabled
        }
        return self.save_preferences()

class PreferencesDialog:
    """Dialog for editing application preferences."""
    
    def __init__(self, parent, preferences_manager):
        self.parent = parent
        self.prefs = preferences_manager
        self.window = None
        
    def show(self):
        # If window already exists, bring it to front
        if self.window is not None and self.window.winfo_exists():
            self.window.lift()
            return
            
        # Create a new window for preferences
        self.window = tk.Toplevel(self.parent)
        self.window.title("Tercihler")
        self.window.geometry("500x550")
        self.window.resizable(False, False)
        
        # Create a notebook (tabbed interface)
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create tabs
        general_tab = ttk.Frame(notebook)
        weekday_breaks_tab = ttk.Frame(notebook)
        weekend_breaks_tab = ttk.Frame(notebook)
        
        notebook.add(general_tab, text="Genel")
        notebook.add(weekday_breaks_tab, text="Hafta İçi Molaları")
        notebook.add(weekend_breaks_tab, text="Hafta Sonu Molaları")
        
        # Populate general tab
        self.setup_general_tab(general_tab)
        
        # Populate breaks tabs
        self.setup_breaks_tab(weekday_breaks_tab, is_weekday=True)
        self.setup_breaks_tab(weekend_breaks_tab, is_weekday=False)
        
        # Create buttons at the bottom
        button_frame = tk.Frame(self.window)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        save_button = tk.Button(button_frame, text="Kaydet", command=self.save_preferences)
        save_button.pack(side=tk.RIGHT, padx=5)
        
        cancel_button = tk.Button(button_frame, text="İptal", command=self.window.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)
        
    def setup_general_tab(self, tab):
        """Set up the general preferences tab."""
        # Language selection
        lang_frame = tk.LabelFrame(tab, text="Dil", padx=10, pady=10)
        lang_frame.pack(fill="x", padx=10, pady=10)
        
        self.lang_var = tk.StringVar(value=self.prefs.get("language"))
        
        languages = {
            "tr": "Türkçe",
            "en": "English"
        }
        
        for code, name in languages.items():
            rb = tk.Radiobutton(lang_frame, text=name, value=code, variable=self.lang_var)
            rb.pack(anchor="w")
        
        # Rounding algorithm selection
        round_frame = tk.LabelFrame(tab, text="Yuvarlama Algoritması", padx=10, pady=10)
        round_frame.pack(fill="x", padx=10, pady=10)
        
        self.round_var = tk.StringVar(value=self.prefs.get("rounding_algorithm"))
        
        algorithms = {
            "standard": "Standart (15 dakika)",
            "nearest_5": "En yakın 5 dakika",
            "nearest_10": "En yakın 10 dakika",
            "nearest_30": "En yakın 30 dakika",  # New 30-minute rounding option
            "ceiling": "Yukarı yuvarlama (tavan)",
            "floor": "Aşağı yuvarlama (taban)"
        }
        
        for code, name in algorithms.items():
            rb = tk.Radiobutton(round_frame, text=name, value=code, variable=self.round_var)
            rb.pack(anchor="w")
    
    def setup_breaks_tab(self, tab, is_weekday):
        """Set up the breaks configuration tab."""
        day_type = "Hafta İçi" if is_weekday else "Hafta Sonu"
        
        # Lunch break configuration
        lunch_frame = tk.LabelFrame(tab, text=f"{day_type} Öğle Molası", padx=10, pady=10)
        lunch_frame.pack(fill="x", padx=10, pady=10)
        
        # Get current lunch break settings
        lunch_info = self.prefs.get_break_info("lunch", is_weekday=is_weekday)
        lunch_enabled = lunch_info.get("enabled", True)
        lunch_start = lunch_info.get("start_time", "13:00")
        lunch_end = lunch_info.get("end_time", "13:45" if is_weekday else "13:30")
        
        # Enabled checkbox
        if is_weekday:
            self.weekday_lunch_enabled_var = tk.BooleanVar(value=lunch_enabled)
            lunch_cb = tk.Checkbutton(lunch_frame, text="Öğle Molasını Etkinleştir", 
                                    variable=self.weekday_lunch_enabled_var)
        else:
            self.weekend_lunch_enabled_var = tk.BooleanVar(value=lunch_enabled)
            lunch_cb = tk.Checkbutton(lunch_frame, text="Öğle Molasını Etkinleştir", 
                                    variable=self.weekend_lunch_enabled_var)
        lunch_cb.grid(row=0, column=0, columnspan=2, sticky="w")
        
        # Start time
        tk.Label(lunch_frame, text="Başlangıç:").grid(row=1, column=0, sticky="w", pady=5)
        if is_weekday:
            self.weekday_lunch_start_var = tk.StringVar(value=lunch_start)
            lunch_start_entry = tk.Entry(lunch_frame, textvariable=self.weekday_lunch_start_var, width=10)
        else:
            self.weekend_lunch_start_var = tk.StringVar(value=lunch_start)
            lunch_start_entry = tk.Entry(lunch_frame, textvariable=self.weekend_lunch_start_var, width=10)
        lunch_start_entry.grid(row=1, column=1, sticky="w", padx=10)
        
        # End time
        tk.Label(lunch_frame, text="Bitiş:").grid(row=2, column=0, sticky="w", pady=5)
        if is_weekday:
            self.weekday_lunch_end_var = tk.StringVar(value=lunch_end)
            lunch_end_entry = tk.Entry(lunch_frame, textvariable=self.weekday_lunch_end_var, width=10)
        else:
            self.weekend_lunch_end_var = tk.StringVar(value=lunch_end)
            lunch_end_entry = tk.Entry(lunch_frame, textvariable=self.weekend_lunch_end_var, width=10)
        lunch_end_entry.grid(row=2, column=1, sticky="w", padx=10)
        
        # Dinner break configuration
        dinner_frame = tk.LabelFrame(tab, text=f"{day_type} Akşam Molası", padx=10, pady=10)
        dinner_frame.pack(fill="x", padx=10, pady=10)
        
        # Get current dinner break settings
        dinner_info = self.prefs.get_break_info("dinner", is_weekday=is_weekday)
        dinner_enabled = dinner_info.get("enabled", True)
        dinner_start = dinner_info.get("start_time", "19:00")
        dinner_end = dinner_info.get("end_time", "19:30")
        
        # Enabled checkbox
        if is_weekday:
            self.weekday_dinner_enabled_var = tk.BooleanVar(value=dinner_enabled)
            dinner_cb = tk.Checkbutton(dinner_frame, text="Akşam Molasını Etkinleştir", 
                                     variable=self.weekday_dinner_enabled_var)
        else:
            self.weekend_dinner_enabled_var = tk.BooleanVar(value=dinner_enabled)
            dinner_cb = tk.Checkbutton(dinner_frame, text="Akşam Molasını Etkinleştir", 
                                     variable=self.weekend_dinner_enabled_var)
        dinner_cb.grid(row=0, column=0, columnspan=2, sticky="w")
        
        # Start time
        tk.Label(dinner_frame, text="Başlangıç:").grid(row=1, column=0, sticky="w", pady=5)
        if is_weekday:
            self.weekday_dinner_start_var = tk.StringVar(value=dinner_start)
            dinner_start_entry = tk.Entry(dinner_frame, textvariable=self.weekday_dinner_start_var, width=10)
        else:
            self.weekend_dinner_start_var = tk.StringVar(value=dinner_start)
            dinner_start_entry = tk.Entry(dinner_frame, textvariable=self.weekend_dinner_start_var, width=10)
        dinner_start_entry.grid(row=1, column=1, sticky="w", padx=10)
        
        # End time
        tk.Label(dinner_frame, text="Bitiş:").grid(row=2, column=0, sticky="w", pady=5)
        if is_weekday:
            self.weekday_dinner_end_var = tk.StringVar(value=dinner_end)
            dinner_end_entry = tk.Entry(dinner_frame, textvariable=self.weekday_dinner_end_var, width=10)
        else:
            self.weekend_dinner_end_var = tk.StringVar(value=dinner_end)
            dinner_end_entry = tk.Entry(dinner_frame, textvariable=self.weekend_dinner_end_var, width=10)
        dinner_end_entry.grid(row=2, column=1, sticky="w", padx=10)
    
    def save_preferences(self):
        """Save preferences and close the dialog."""
        # Validate time formats
        time_fields = {
            "Hafta İçi Öğle Molası Başlangıç": self.weekday_lunch_start_var.get(),
            "Hafta İçi Öğle Molası Bitiş": self.weekday_lunch_end_var.get(),
            "Hafta İçi Akşam Molası Başlangıç": self.weekday_dinner_start_var.get(),
            "Hafta İçi Akşam Molası Bitiş": self.weekday_dinner_end_var.get(),
            "Hafta Sonu Öğle Molası Başlangıç": self.weekend_lunch_start_var.get(),
            "Hafta Sonu Öğle Molası Bitiş": self.weekend_lunch_end_var.get(),
            "Hafta Sonu Akşam Molası Başlangıç": self.weekend_dinner_start_var.get(),
            "Hafta Sonu Akşam Molası Bitiş": self.weekend_dinner_end_var.get()
        }
        
        # Validate time format (HH:MM)
        for field_name, time_str in time_fields.items():
            if not self._is_valid_time_format(time_str):
                messagebox.showerror("Geçersiz Zaman Formatı", 
                                    f"{field_name}: {time_str} geçerli bir zaman değil.\n"
                                    "Lütfen HH:MM formatında girin (örn: 13:45)")
                return
        
        # Save preferences
        self.prefs.set("language", self.lang_var.get())
        self.prefs.set("rounding_algorithm", self.round_var.get())
        
        # Save weekday break settings
        self.prefs.set_break_info(
            "lunch",
            self.weekday_lunch_start_var.get(),
            self.weekday_lunch_end_var.get(),
            self.weekday_lunch_enabled_var.get(),
            is_weekday=True
        )
        
        self.prefs.set_break_info(
            "dinner",
            self.weekday_dinner_start_var.get(),
            self.weekday_dinner_end_var.get(),
            self.weekday_dinner_enabled_var.get(),
            is_weekday=True
        )
        
        # Save weekend break settings
        self.prefs.set_break_info(
            "lunch",
            self.weekend_lunch_start_var.get(),
            self.weekend_lunch_end_var.get(),
            self.weekend_lunch_enabled_var.get(),
            is_weekday=False
        )
        
        self.prefs.set_break_info(
            "dinner",
            self.weekend_dinner_start_var.get(),
            self.weekend_dinner_end_var.get(),
            self.weekend_dinner_enabled_var.get(),
            is_weekday=False
        )
        
        # Inform user and close window
        messagebox.showinfo("Tercihler", "Tercihler başarıyla kaydedildi.")
        self.window.destroy()
    
    def _is_valid_time_format(self, time_str):
        """Check if a string is in valid HH:MM format."""
        try:
            hours, minutes = time_str.split(":")
            hours = int(hours)
            minutes = int(minutes)
            return 0 <= hours <= 23 and 0 <= minutes <= 59
        except (ValueError, AttributeError):
            return False

# Create a global preferences manager instance
preferences = PreferencesManager()