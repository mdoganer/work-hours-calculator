# gui/dialogs.py
import tkinter as tk
from tkinter import ttk, messagebox
import os
from core.data import filter_by_badge
from utils.languages import _

class BadgeDataDialog:
    def __init__(self, parent, badge_number, data_provider, on_close=None):
        self.parent = parent
        self.badge_number = badge_number
        self.data_provider = data_provider
        self.window = None
        self.on_close = on_close
        self.show_all = badge_number == _("all_records", "tüm kayıtlar")  # Check if we should show all records
        
    def show(self):
        # If window already exists, bring it to front
        if self.window is not None and self.window.winfo_exists():
            self.window.lift()
            return
            
        # Create a new window for the control table
        self.window = tk.Toplevel(self.parent)
        if self.show_all:
            self.window.title(_("badge_control_title", "Sicil Kontrol"))
        else:
            self.window.title(f"{_('badge', 'Sicil Numarası')}: {self.badge_number}")
        self.window.geometry("900x600")

        # Add a search frame if we're showing all records
        if self.show_all:
            search_frame = tk.Frame(self.window)
            search_frame.pack(fill="x", padx=10, pady=5)
            
            tk.Label(search_frame, text=_("search_badge", "Sicil Ara:")).pack(side=tk.LEFT, padx=5)
            self.search_entry = tk.Entry(search_frame, width=15)
            self.search_entry.pack(side=tk.LEFT, padx=5)
            self.search_entry.bind("<KeyRelease>", self.filter_records)

        # Create an outer frame to hold the treeview and scrollbars
        tree_frame = tk.Frame(self.window)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Add a Treeview in the new window
        if self.show_all:
            columns = (_("badge", "Sicil"), _("date", "Tarih"), _("entry", "Giriş"), 
                      _("exit", "Çıkış"), _("net_work_hours", "Net Çalışma (Saat)"))
        else:
            columns = (_("date", "Tarih"), _("entry", "Giriş"), 
                      _("exit", "Çıkış"), _("net_work_hours", "Net Çalışma (Saat)"))
            
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        # Configure columns
        if self.show_all:
            self.tree.heading(_("badge", "Sicil"), text=_("badge", "Sicil"))
            self.tree.column(_("badge", "Sicil"), width=80)
            self.tree.heading(_("date", "Tarih"), text=_("date", "Tarih"))
            self.tree.column(_("date", "Tarih"), width=100)
            self.tree.heading(_("entry", "Giriş"), text=_("entry", "Giriş"))
            self.tree.column(_("entry", "Giriş"), width=80)
            self.tree.heading(_("exit", "Çıkış"), text=_("exit", "Çıkış"))
            self.tree.column(_("exit", "Çıkış"), width=80)
            self.tree.heading(_("net_work_hours", "Net Çalışma (Saat)"), text=_("net_work_hours", "Net Çalışma (Saat)"))
            self.tree.column(_("net_work_hours", "Net Çalışma (Saat)"), width=120)
        else:
            self.tree.heading(_("date", "Tarih"), text=_("date", "Tarih"))
            self.tree.column(_("date", "Tarih"), width=100)
            self.tree.heading(_("entry", "Giriş"), text=_("entry", "Giriş"))
            self.tree.column(_("entry", "Giriş"), width=80)
            self.tree.heading(_("exit", "Çıkış"), text=_("exit", "Çıkış"))
            self.tree.column(_("exit", "Çıkış"), width=80)
            self.tree.heading(_("net_work_hours", "Net Çalışma (Saat)"), text=_("net_work_hours", "Net Çalışma (Saat)"))
            self.tree.column(_("net_work_hours", "Net Çalışma (Saat)"), width=120)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout for treeview with scrollbars
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        
        # Make the treeview and frame expandable
        tree_frame.grid_columnconfigure(0, weight=1)
        tree_frame.grid_rowconfigure(0, weight=1)

        # Create a frame for action buttons
        buttons_frame = tk.Frame(self.window)
        buttons_frame.pack(pady=5, fill="x")
        
        # Add a refresh button
        refresh_button = tk.Button(buttons_frame, text=_("refresh", "Yenile"), command=self.refresh_table)
        refresh_button.pack(side=tk.LEFT, padx=10)
        
        # Add delete button with default state disabled
        self.delete_button = tk.Button(buttons_frame, text=_("delete_selected", "Seçili Kaydı Sil"), 
                                      command=self.delete_selected, state=tk.DISABLED)
        self.delete_button.pack(side=tk.LEFT, padx=10)
        
        # Bind selection event to enable/disable delete button
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        
        # Set up window close event
        self.window.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        # Add right-click context menu
        self.create_context_menu()
        
        # Initial population of the Treeview
        self.refresh_table()
    
    def create_context_menu(self):
        """Create a context menu for right-click actions on rows."""
        self.context_menu = tk.Menu(self.window, tearoff=0)
        self.context_menu.add_command(label=_("delete", "Sil"), command=self.delete_selected)
        
        # Bind right-click to show context menu
        self.tree.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        """Show context menu on right-click."""
        # Select the row that was right-clicked
        item = self.tree.identify_row(event.y)
        if item:
            # Select the row
            self.tree.selection_set(item)
            # Show context menu
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()
    
    def on_select(self, event):
        """Handle selection events in the Treeview."""
        selected = self.tree.selection()
        # Enable or disable delete button based on selection
        if selected:
            self.delete_button.config(state=tk.NORMAL)
        else:
            self.delete_button.config(state=tk.DISABLED)
    
    def delete_selected(self):
        """Delete the selected record from the table and JSON file."""
        selected = self.tree.selection()
        if not selected:
            return
            
        # Get the record data from the selected row
        values = self.tree.item(selected[0], 'values')
        
        # Confirm deletion
        if not messagebox.askyesno(_("confirmation", "Onay"), _("delete_confirm", "Seçili kaydı silmek istediğinizden emin misiniz?")):
            return
            
        try:
            # Get the record identifiers
            if self.show_all:
                sicil = values[0]  # Sicil is at index 0
                tarih = values[1]  # Date is at index 1
                giris = values[2]  # Entry time is at index 2
                cikis = values[3]  # Exit time is at index 3
            else:
                sicil = self.badge_number
                tarih = values[0]  # Date is at index 0
                giris = values[1]  # Entry time is at index 1
                cikis = values[2]  # Exit time is at index 2
            
            # Import delete_record function
            from core.data import delete_record
            
            # Delete the record from JSON
            success = delete_record(sicil, tarih, giris, cikis)
            
            if success:
                # Remove from treeview
                self.tree.delete(selected)
                messagebox.showinfo(_("success", "Başarılı"), _("record_deleted", "Kayıt başarıyla silindi."))
                
                # If we're showing all records and have filtered, refresh all_records
                if self.show_all and hasattr(self, 'all_records'):
                    self.all_records = [r for r in self.all_records 
                                     if not (r.get('sicil') == sicil and 
                                             r.get('tarih') == tarih and 
                                             r.get('giris') == giris and 
                                             r.get('cikis') == cikis)]
                    
            else:
                messagebox.showerror(_("error", "Hata"), _("record_delete_error", "Kayıt silinemedi."))
        except Exception as e:
            messagebox.showerror(_("error", "Hata"), f"{_('error_delete', 'Kayıt silme sırasında bir hata oluştu:')}\n{e}")
    
    def _on_window_close(self):
        # Call the on_close callback if provided
        if self.on_close:
            self.on_close()
        # Destroy the window
        if self.window:
            self.window.destroy()
            self.window = None
    
    def filter_records(self, event=None):
        # Filter records based on search text
        if not hasattr(self, 'search_entry') or not hasattr(self, 'all_records'):
            return
            
        search_text = self.search_entry.get().strip().lower()
        
        # Clear the existing rows in the Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        # Filter and re-insert records
        for record in self.all_records:
            sicil = str(record.get("sicil", "")).lower()
            
            if not search_text or search_text in sicil:
                # Insert with standard columns
                self.tree.insert("", "end", values=(
                    record.get("sicil", ""),
                    record.get("tarih", ""), 
                    record.get("giris", ""), 
                    record.get("cikis", ""), 
                    record.get("net_calisma", "")
                ))
        
    def refresh_table(self):
        try:
            # Fetch the latest data from the JSON file
            data = self.data_provider()
            
            if self.show_all:
                filtered_data = data  # Show all records
                self.all_records = data  # Store for filtering
            else:
                filtered_data = filter_by_badge(data, self.badge_number)

            # Clear the existing rows in the Treeview
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Re-insert the filtered data
            for record in filtered_data:
                if self.show_all:
                    # When showing all, include badge number column
                    self.tree.insert("", "end", values=(
                        record.get("sicil", ""),
                        record.get("tarih", ""), 
                        record.get("giris", ""), 
                        record.get("cikis", ""), 
                        record.get("net_calisma", "")
                    ))
                else:
                    # For specific badge, don't include badge number column
                    self.tree.insert("", "end", values=(
                        record.get("tarih", ""), 
                        record.get("giris", ""), 
                        record.get("cikis", ""), 
                        record.get("net_calisma", "")
                    ))

            # Show a message if no data is found
            if not filtered_data and not self.show_all:
                messagebox.showinfo(_("info", "Bilgi"), _("no_records", "Sicil Numarası {0} için kayıt bulunamadı.").format(self.badge_number))
                
        except Exception as e:
            messagebox.showerror(_("error", "Hata"), f"{_('error_table_refresh', 'Tablo yenilenirken bir hata oluştu:')}\n{e}")

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
        columns = (_("badge", "Sicil"), _("date", "Tarih"), _("entry", "Giriş"), 
                  _("exit", "Çıkış"), _("net_work_hours", "Net Çalışma (Saat)"))
        tree = ttk.Treeview(window, columns=columns, show="headings", height=20)
        tree.heading(_("badge", "Sicil"), text=_("badge", "Sicil"))
        tree.heading(_("date", "Tarih"), text=_("date", "Tarih"))
        tree.heading(_("entry", "Giriş"), text=_("entry", "Giriş"))
        tree.heading(_("exit", "Çıkış"), text=_("exit", "Çıkış"))
        tree.heading(_("net_work_hours", "Net Çalışma (Saat)"), text=_("net_work_hours", "Net Çalışma (Saat)"))
        
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