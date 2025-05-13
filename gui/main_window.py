# gui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime
import json
import os
from gui.widgets import UndoRedoEntry
from gui.menu import MenuBuilder
from gui.dialogs import BadgeDataDialog, JsonDataDialog
from core.time_calc import round_time, calculate_work_hours
from core.data import save_record, load_records, create_new_file, open_json_file
from utils.file_utils import set_custom_file_path
from utils.languages import _

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(_("app_title"))
        self.root.geometry("600x400")
        
        # Data cache for entry, exit times
        self.data_cache = {
            "entry": None,
            "exit": None,
            "net_duration": None
        }
        
        # Current active file path
        self.current_file_path = None
        
        # Track active badge dialog window
        self.badge_dialog = None
        
        # Setup UI components
        self.setup_menu()
        self.setup_interface()
        self.setup_keyboard_shortcuts()
    
    def setup_menu(self):
        """Setup the menu bar and its items."""
        callbacks = {
            "new_file": self.new_file,
            "open_file": self.open_file,
            "save": self.save_json,
            "undo": self.undo,
            "redo": self.redo,
            "cut": self.cut,
            "copy": self.copy,
            "paste": self.paste,
            "select_all": self.select_all,
            "calculate": self.calculate,
            "badge_control": self.display_badge_data,
            "preferences": self.show_preferences,
            "help_content": self.show_help
        }
        self.menu_builder = MenuBuilder(self.root, callbacks)
    
    def setup_interface(self):
        """Setup the main interface components."""
        # Input fields
        tk.Label(self.root, text=_("entry_time_label"), font=("Helvetica", 11, "bold")).pack(pady=5)
        self.entry_input = UndoRedoEntry(self.root)
        self.entry_input.pack(pady=5)

        tk.Label(self.root, text=_("exit_time_label"), font=("Helvetica", 11, "bold")).pack(pady=5)
        self.exit_input = UndoRedoEntry(self.root)
        self.exit_input.pack(pady=5)

        # Radio buttons for weekday/weekend
        self.weekday_var = tk.StringVar(value=_("weekday"))
        tk.Radiobutton(self.root, text=_("weekday"), variable=self.weekday_var, value=_("weekday")).pack()
        tk.Radiobutton(self.root, text=_("weekend"), variable=self.weekday_var, value=_("weekend")).pack()

        # Button frame for aligning buttons in a single row
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        calculate_button = tk.Button(button_frame, text=_("button_calculate"), command=self.calculate)
        calculate_button.grid(row=0, column=0, padx=10)

        save_button = tk.Button(button_frame, text=_("button_save"), command=self.save_json)
        save_button.grid(row=0, column=1, padx=10)

        control_button = tk.Button(button_frame, text=_("button_badge_control"), command=self.display_badge_data)
        control_button.grid(row=0, column=2, padx=10)

        # Result label
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 10), justify="left")
        self.result_label.pack(pady=10)

        # Footer
        footer = tk.Label(self.root, text=_("footer_text"), font=("Arial", 8), fg="gray")
        footer.pack(side="bottom", pady=5)
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for edit operations."""
        self.root.bind("<Control-z>", lambda event: self.undo())
        self.root.bind("<Control-y>", lambda event: self.redo())
        self.root.bind("<Control-x>", lambda event: self.cut())
        self.root.bind("<Control-c>", lambda event: self.copy())
        self.root.bind("<Control-v>", lambda event: self.paste())
        self.root.bind("<Control-a>", lambda event: self.select_all())
    
    def run(self):
        """Start the main event loop."""
        self.root.mainloop()
    
    # Edit functions
    def undo(self):
        try:
            widget = self.root.focus_get()
            if isinstance(widget, UndoRedoEntry):
                widget.undo()
        except Exception as e:
            messagebox.showerror(_("error"), f"{_('error_undo')}\n{e}")

    def redo(self):
        try:
            widget = self.root.focus_get()
            if isinstance(widget, UndoRedoEntry):
                widget.redo()
        except Exception as e:
            messagebox.showerror(_("error"), f"{_('error_redo')}\n{e}")

    def cut(self):
        try:
            widget = self.root.focus_get()
            if isinstance(widget, tk.Entry):
                widget.event_generate("<<Cut>>")
        except Exception as e:
            messagebox.showerror(_("error"), f"{_('error_cut')}\n{e}")

    def copy(self):
        try:
            widget = self.root.focus_get()
            if isinstance(widget, tk.Entry):
                widget.event_generate("<<Copy>>")
        except Exception as e:
            messagebox.showerror(_("error"), f"{_('error_copy')}\n{e}")

    def paste(self):
        try:
            widget = self.root.focus_get()
            if isinstance(widget, tk.Entry):
                widget.event_generate("<<Paste>>")
        except Exception as e:
            messagebox.showerror(_("error"), f"{_('error_paste')}\n{e}")

    def select_all(self):
        try:
            widget = self.root.focus_get()
            if isinstance(widget, tk.Entry):
                widget.select_range(0, 'end')
                widget.icursor('end')
        except Exception as e:
            messagebox.showerror(_("error"), f"{_('error_select_all')}\n{e}")
    
    # Action functions
    def calculate(self):
        try:
            entry = self.entry_input.get()
            exit = self.exit_input.get()
            is_weekday = self.weekday_var.get() == _("weekday")
            rounded_entry = round_time(datetime.strptime(entry, "%H:%M"))
            rounded_exit = round_time(datetime.strptime(exit, "%H:%M"))
            
            sonuc = calculate_work_hours(entry, exit, is_weekday, self.data_cache)
            self.result_label.config(
                text=f"{_('net_work_time')} {sonuc}\n"
                     f"{_('rounded_entry')} {rounded_entry.strftime('%H:%M')}\n"
                     f"{_('rounded_exit')} {rounded_exit.strftime('%H:%M')}"
            )
        except Exception as e:
            messagebox.showerror(_("error"), f"{_('invalid_time')} {e}")

    def save_json(self):
        try:
            if not self.data_cache["entry"] or not self.data_cache["exit"] or not self.data_cache["net_duration"]:
                messagebox.showwarning(_("warning"), _("calculate_first"))
                return
                
            sicil_no = simpledialog.askstring(_("badge_number_prompt"), _("badge_number_prompt"))
            if not sicil_no:
                messagebox.showinfo(_("info"), _("record_cancelled"))
                return
            
            # Use current_file_path if it exists, otherwise use default
            if self.current_file_path:
                file_path = save_record(sicil_no, self.data_cache, self.current_file_path)
            else:
                file_path = save_record(sicil_no, self.data_cache)
            
            messagebox.showinfo(_("success"), f"{_('record_success')}\n{_('file_path')} {file_path}")
        except Exception as e:
            messagebox.showerror(_("error"), f"{_('error_save')}\n{e}")

    def display_badge_data(self):
        # Check if we already have an active badge dialog
        if self.badge_dialog is not None and hasattr(self.badge_dialog, 'window') and self.badge_dialog.window is not None:
            # If the window exists, bring it to front
            if self.badge_dialog.window.winfo_exists():
                self.badge_dialog.window.lift()
                return
            # If the window doesn't exist anymore, clear the reference
            self.badge_dialog = None
            
        # Create callback function to clear dialog reference when window closes
        def on_dialog_close():
            self.badge_dialog = None
            
        # Use a default badge number - no prompt needed
        badge_number = _("all_records")
        self.badge_dialog = BadgeDataDialog(self.root, badge_number, load_records, on_close=on_dialog_close)
        self.badge_dialog.show()

    def new_file(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[(_("json_files"), "*.json"), (_("all_files"), "*.*")],
                title=_("create_new_json")
            )
            
            if not file_path:  # User cancelled the dialog
                return
                
            create_new_file(file_path)
            
            # Set the custom file path globally
            set_custom_file_path(file_path)
            
            # Store the current file path and update window title
            self.current_file_path = file_path
            file_name = os.path.basename(file_path)
            self.root.title(f"{_('app_title')} - {file_name}")
            
            messagebox.showinfo(_("success"), f"{_('file_created')}\n{file_path}")
        except Exception as e:
            messagebox.showerror(_("error"), f"{_('error_file_create')}\n{e}")

    def open_file(self):
        try:
            file_path = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[(_("json_files"), "*.json"), (_("all_files"), "*.*")],
                title=_("open_json")
            )
            
            if not file_path:  # User cancelled the dialog
                return
                
            data = open_json_file(file_path)
            
            # Set the custom file path globally
            set_custom_file_path(file_path)
            
            # Store the current file path and update window title
            self.current_file_path = file_path
            file_name = os.path.basename(file_path)
            self.root.title(f"{_('app_title')} - {file_name}")
            
            dialog = JsonDataDialog(self.root, data, file_path)
            dialog.show()
        except json.JSONDecodeError:
            messagebox.showerror(_("error"), _("invalid_json"))
        except Exception as e:
            messagebox.showerror(_("error"), f"{_('error_file_open')}\n{e}")

    def show_preferences(self):
        """Display the preferences dialog."""
        from gui.preferences import PreferencesDialog, preferences
        dialog = PreferencesDialog(self.root, preferences)
        dialog.show()

    def show_help(self):
        """Display the help content dialog."""
        from gui.help import HelpDialog
        dialog = HelpDialog(self.root)
        dialog.show()