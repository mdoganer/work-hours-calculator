# gui/menu.py
import tkinter as tk
from tkinter import messagebox
from utils.languages import _

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
        self.menu_bar.add_cascade(label=_("file"), menu=file_menu)
        file_menu.add_command(label=_("new_file"), command=self.callbacks["new_file"])
        file_menu.add_command(label=_("open_file"), command=self.callbacks["open_file"])
        file_menu.add_separator()
        file_menu.add_command(label=_("quit"), command=self.root.quit)
        
    def create_edit_menu(self):
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=_("edit"), menu=edit_menu)
        edit_menu.add_command(label=_("edit_undo"), command=self.callbacks["undo"], accelerator="Ctrl+Z")
        edit_menu.add_command(label=_("edit_redo"), command=self.callbacks["redo"], accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label=_("edit_cut"), command=self.callbacks["cut"], accelerator="Ctrl+X")
        edit_menu.add_command(label=_("edit_copy"), command=self.callbacks["copy"], accelerator="Ctrl+C")
        edit_menu.add_command(label=_("edit_paste"), command=self.callbacks["paste"], accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label=_("edit_select_all"), command=self.callbacks["select_all"], accelerator="Ctrl+A")
        
    def create_tools_menu(self):
        tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=_("tools_menu"), menu=tools_menu)
        tools_menu.add_command(label=_("tools_calculate"), command=self.callbacks["calculate"])
        tools_menu.add_command(label=_("save"), command=self.callbacks["save"])
        tools_menu.add_command(label=_("tools_badge_control"), command=self.callbacks["badge_control"])
        tools_menu.add_separator()
        tools_menu.add_command(label=_("preferences"), command=self.callbacks["preferences"])
        
    def create_help_menu(self):
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label=_("help"), menu=help_menu)
        help_menu.add_command(label=_("help_content"), command=self.callbacks["help_content"])
        help_menu.add_command(label=_("about"), 
                              command=lambda: messagebox.showinfo(_("about"), 
                                                                _("about_text")))