# gui/menu.py
import tkinter as tk
from tkinter import messagebox, filedialog
import os

class MenuBuilder:
    def __init__(self, root, callbacks):
        self.root = root
        self.callbacks = callbacks
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)
        
        self.create_file_menu()
        self.create_edit_menu()
        self.create_tools_menu()
        self.create_help_menu()
        
    def create_file_menu(self):
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Dosya", menu=file_menu)
        file_menu.add_command(label="Yeni", command=self.callbacks["new_file"])
        file_menu.add_command(label="Aç...", command=self.callbacks["open_file"])
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.root.quit)
        
    def create_edit_menu(self):
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Düzenle", menu=edit_menu)
        edit_menu.add_command(label="Geri Al", command=self.callbacks["undo"], accelerator="Ctrl+Z")
        edit_menu.add_command(label="İleri Al", command=self.callbacks["redo"], accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Kes", command=self.callbacks["cut"], accelerator="Ctrl+X")
        edit_menu.add_command(label="Kopyala", command=self.callbacks["copy"], accelerator="Ctrl+C")
        edit_menu.add_command(label="Yapıştır", command=self.callbacks["paste"], accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Tümünü Seç", command=self.callbacks["select_all"], accelerator="Ctrl+A")
        
    def create_tools_menu(self):
        tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Araçlar", menu=tools_menu)
        tools_menu.add_command(label="Hesapla", command=self.callbacks["calculate"])
        tools_menu.add_command(label="Kaydet", command=self.callbacks["save"])
        tools_menu.add_command(label="Sicil Kontrol", command=self.callbacks["badge_control"])
        tools_menu.add_separator()
        tools_menu.add_command(label="Tercihler", command=self.callbacks["preferences"])
        
    def create_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Yardım", menu=help_menu)
        help_menu.add_command(label="Yardım İçeriği", command=self.callbacks["help_content"])
        help_menu.add_command(label="Hakkında", 
                              command=lambda: messagebox.showinfo("Hakkında", 
                                                                  "Çalışma Süresi Hesaplayıcı\nVersion 1.0\nDeveloped by MMD"))