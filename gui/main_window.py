# gui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from datetime import datetime
import os
from gui.widgets import UndoRedoEntry
from gui.menu import MenuBuilder
from gui.dialogs import BadgeDataDialog, JsonDataDialog
from core.time_calc import round_time, calculate_work_hours
from core.data import save_record, load_records, create_new_file, open_json_file
from utils.file_utils import set_custom_file_path

class MainWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Çalışma Süresi Hesaplayıcı")
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
            "badge_control": self.display_badge_data
        }
        self.menu_builder = MenuBuilder(self.root, callbacks)
    
    def setup_interface(self):
        """Setup the main interface components."""
        # Input fields
        tk.Label(self.root, text="Giriş Saati (HH:MM):", font=("Helvetica", 11, "bold")).pack(pady=5)
        self.entry_input = UndoRedoEntry(self.root)
        self.entry_input.pack(pady=5)

        tk.Label(self.root, text="Çıkış Saati (HH:MM):", font=("Helvetica", 11, "bold")).pack(pady=5)
        self.exit_input = UndoRedoEntry(self.root)
        self.exit_input.pack(pady=5)

        # Radio buttons for weekday/weekend
        self.weekday_var = tk.StringVar(value="Hafta İçi")
        tk.Radiobutton(self.root, text="Hafta İçi", variable=self.weekday_var, value="Hafta İçi").pack()
        tk.Radiobutton(self.root, text="Hafta Sonu", variable=self.weekday_var, value="Hafta Sonu").pack()

        # Button frame for aligning buttons in a single row
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10)

        calculate_button = tk.Button(button_frame, text="Hesapla", command=self.calculate)
        calculate_button.grid(row=0, column=0, padx=10)

        save_button = tk.Button(button_frame, text="Kaydet", command=self.save_json)
        save_button.grid(row=0, column=1, padx=10)

        control_button = tk.Button(button_frame, text="Sicil Kontrol", command=self.display_badge_data)
        control_button.grid(row=0, column=2, padx=10)

        # Result label
        self.result_label = tk.Label(self.root, text="", font=("Helvetica", 10), justify="left")
        self.result_label.pack(pady=10)

        # Footer
        footer = tk.Label(self.root, text="Developed by MMD", font=("Arial", 8), fg="gray")
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
            messagebox.showerror("Hata", f"Geri alma sırasında bir hata oluştu:\n{e}")

    def redo(self):
        try:
            widget = self.root.focus_get()
            if isinstance(widget, UndoRedoEntry):
                widget.redo()
        except Exception as e:
            messagebox.showerror("Hata", f"Yineleme sırasında bir hata oluştu:\n{e}")

    def cut(self):
        try:
            widget = self.root.focus_get()
            if isinstance(widget, tk.Entry):
                widget.event_generate("<<Cut>>")
        except Exception as e:
            messagebox.showerror("Hata", f"Kesme sırasında bir hata oluştu:\n{e}")

    def copy(self):
        try:
            widget = self.root.focus_get()
            if isinstance(widget, tk.Entry):
                widget.event_generate("<<Copy>>")
        except Exception as e:
            messagebox.showerror("Hata", f"Kopyalama sırasında bir hata oluştu:\n{e}")

    def paste(self):
        try:
            widget = self.root.focus_get()
            if isinstance(widget, tk.Entry):
                widget.event_generate("<<Paste>>")
        except Exception as e:
            messagebox.showerror("Hata", f"Yapıştırma sırasında bir hata oluştu:\n{e}")

    def select_all(self):
        try:
            widget = self.root.focus_get()
            if isinstance(widget, tk.Entry):
                widget.select_range(0, 'end')
                widget.icursor('end')
        except Exception as e:
            messagebox.showerror("Hata", f"Tümünü seçme sırasında bir hata oluştu:\n{e}")
    
    # Action functions
    def calculate(self):
        try:
            entry = self.entry_input.get()
            exit = self.exit_input.get()
            is_weekday = self.weekday_var.get()
            rounded_entry = round_time(datetime.strptime(entry, "%H:%M"))
            rounded_exit = round_time(datetime.strptime(exit, "%H:%M"))
            
            sonuc = calculate_work_hours(entry, exit, is_weekday == "Hafta İçi", self.data_cache)
            self.result_label.config(
                text=f"Net Çalışma Süresi: {sonuc}\n"
                     f"Giriş (yuvarlanmış): {rounded_entry.strftime('%H:%M')}\n"
                     f"Çıkış (yuvarlanmış): {rounded_exit.strftime('%H:%M')}"
            )
        except Exception as e:
            messagebox.showerror("Hata", f"Geçersiz giriş: {e}")

    def save_json(self):
        try:
            if not self.data_cache["entry"] or not self.data_cache["exit"] or not self.data_cache["net_duration"]:
                messagebox.showwarning("Uyarı", "Lütfen önce HESAPLA butonuna basın.")
                return
                
            sicil_no = simpledialog.askstring("Sicil Numarası", "Sicil numaranızı giriniz:")
            if not sicil_no:
                messagebox.showinfo("Bilgi", "Kayıt iptal edildi.")
                return
            
            # Use current_file_path if it exists, otherwise use default
            if self.current_file_path:
                file_path = save_record(sicil_no, self.data_cache, self.current_file_path)
            else:
                file_path = save_record(sicil_no, self.data_cache)
            
            messagebox.showinfo("Başarılı", f"Kayıt başarıyla yapıldı.\nDosya Yolu: {file_path}")
        except Exception as e:
            messagebox.showerror("Hata", f"Kayıt sırasında bir hata oluştu:\n{e}")

    def display_badge_data(self):
        # Check if we already have an active badge dialog
        if self.badge_dialog is not None and hasattr(self.badge_dialog, 'window') and self.badge_dialog.window is not None:
            # If the window exists, bring it to front
            if self.badge_dialog.window.winfo_exists():
                self.badge_dialog.window.lift()
                return
            # If the window doesn't exist anymore, clear the reference
            self.badge_dialog = None
            
        # No active dialog, proceed to create a new one
        badge_number = simpledialog.askstring("Sicil Numarası", "Lütfen sicil numarasını girin:")
        if not badge_number:
            return
        
        # Create callback function to clear dialog reference when window closes
        def on_dialog_close():
            self.badge_dialog = None
            
        self.badge_dialog = BadgeDataDialog(self.root, badge_number, load_records, on_close=on_dialog_close)
        self.badge_dialog.show()

    def new_file(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Create New JSON File"
            )
            
            if not file_path:  # User cancelled the dialog
                return
                
            create_new_file(file_path)
            
            # Set the custom file path globally
            set_custom_file_path(file_path)
            
            # Store the current file path and update window title
            self.current_file_path = file_path
            file_name = os.path.basename(file_path)
            self.root.title(f"Çalışma Süresi Hesaplayıcı - {file_name}")
            
            messagebox.showinfo("Başarılı", f"Yeni dosya oluşturuldu:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya oluşturulurken hata oluştu:\n{e}")

    def open_file(self):
        try:
            file_path = filedialog.askopenfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Open JSON File"
            )
            
            if not file_path:  # User cancelled the dialog
                return
                
            data = open_json_file(file_path)
            
            # Set the custom file path globally
            set_custom_file_path(file_path)
            
            # Store the current file path and update window title
            self.current_file_path = file_path
            file_name = os.path.basename(file_path)
            self.root.title(f"Çalışma Süresi Hesaplayıcı - {file_name}")
            
            dialog = JsonDataDialog(self.root, data, file_path)
            dialog.show()
        except json.JSONDecodeError:
            messagebox.showerror("Hata", "Geçersiz JSON dosyası.")
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya açılırken hata oluştu:\n{e}")