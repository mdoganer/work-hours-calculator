# gui/dialogs.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
from core.data import filter_by_badge

class BadgeDataDialog:
    def __init__(self, parent, badge_number, data_provider):
        self.parent = parent
        self.badge_number = badge_number
        self.data_provider = data_provider
        self.window = None
        
    def show(self):
        # If window already exists, bring it to front
        if self.window is not None and self.window.winfo_exists():
            self.window.lift()
            return
            
        # Create a new window for the control table
        self.window = tk.Toplevel(self.parent)
        self.window.title(f"Sicil Numarası: {self.badge_number}")
        self.window.geometry("900x600")

        # Add a Treeview in the new window
        columns = ("Tarih", "Giriş", "Çıkış", "Net Çalışma (Saat)")
        self.tree = ttk.Treeview(self.window, columns=columns, show="headings", height=10)
        self.tree.heading("Tarih", text="Tarih")
        self.tree.heading("Giriş", text="Giriş")
        self.tree.heading("Çıkış", text="Çıkış")
        self.tree.heading("Net Çalışma (Saat)", text="Net Çalışma (Saat)")
        self.tree.pack(pady=10, fill="both", expand=True)

        # Add a refresh button below the table
        refresh_button = tk.Button(self.window, text="Yenile", command=self.refresh_table)
        refresh_button.pack(pady=5)
        
        # Initial population of the Treeview
        self.refresh_table()
        
    def refresh_table(self):
        try:
            # Fetch the latest data from the JSON file
            data = self.data_provider()
            filtered_data = filter_by_badge(data, self.badge_number)

            # Clear the existing rows in the Treeview
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Re-insert the filtered data
            for record in filtered_data:
                self.tree.insert("", "end", values=(
                    record["tarih"], 
                    record["giris"], 
                    record["cikis"], 
                    record["net_calisma"]
                ))

            # Show a message if no data is found
            if not filtered_data:
                messagebox.showinfo("Bilgi", f"Sicil Numarası {self.badge_number} için kayıt bulunamadı.")
                
        except Exception as e:
            messagebox.showerror("Hata", f"Tablo yenilenirken bir hata oluştu:\n{e}")

class JsonDataDialog:
    def __init__(self, parent, data, file_path):
        self.parent = parent
        self.data = data
        self.file_path = file_path
        
    def show(self):
        # Create a new window
        window = tk.Toplevel(self.parent)
        window.title(f"JSON Data: {os.path.basename(self.file_path)}")
        window.geometry("800x600")
        
        # Add a Treeview in the new window
        columns = ("Sicil", "Tarih", "Giriş", "Çıkış", "Net Çalışma (Saat)")
        tree = ttk.Treeview(window, columns=columns, show="headings", height=20)
        tree.heading("Sicil", text="Sicil")
        tree.heading("Tarih", text="Tarih")
        tree.heading("Giriş", text="Giriş")
        tree.heading("Çıkış", text="Çıkış")
        tree.heading("Net Çalışma (Saat)", text="Net Çalışma (Saat)")
        
        # Add scrollbars
        vsb = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(window, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout for treeview with scrollbars
        tree.grid(column=0, row=0, sticky="nsew")
        vsb.grid(column=1, row=0, sticky="ns")
        hsb.grid(column=0, row=1, sticky="ew")
        
        # Make treeview expandable
        window.grid_columnconfigure(0, weight=1)
        window.grid_rowconfigure(0, weight=1)
        
        # Insert data into the Treeview
        for record in self.data:
            # Skip records without required fields
            if not all(k in record for k in ["sicil", "tarih", "giris", "cikis", "net_calisma"]):
                continue
                
            tree.insert("", "end", values=(
                record["sicil"],
                record["tarih"],
                record["giris"],
                record["cikis"],
                record["net_calisma"]
            ))