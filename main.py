import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
from datetime import datetime, timedelta
import json
import os
from control_json import json_open, filter_by_badge  # Import functions from json-test.py
from utils import get_file_path  # Import the global get_file_path function

data_cache = {
    "entry": None,
    "exit": None,
    "net_duration": None
} 

badge_window = None  # Global variable to track the badge window

def round_time(dt):
    minute = dt.minute
    if minute < 8:
        minute = 0
    elif minute < 23:
        minute = 15
    elif minute < 38:
        minute = 30
    elif minute < 53:
        minute = 45
    else:
        dt += timedelta(hours=1)
        minute = 0
    return dt.replace(minute=minute, second=0, microsecond=0)

def calculate_work_hours(entry_time, exit_time, is_weekday):
    entry_dt = round_time(datetime.strptime(entry_time, "%H:%M"))
    exit_dt = round_time(datetime.strptime(exit_time, "%H:%M"))
    work_duration = exit_dt - entry_dt

    lunch_duration = timedelta()
    if is_weekday:
        lunch_1 = datetime(entry_dt.year, entry_dt.month, entry_dt.day, 13, 0)
        dinner = datetime(entry_dt.year, entry_dt.month, entry_dt.day, 19, 0)
        if entry_dt <= lunch_1 < exit_dt:
            lunch_duration += timedelta(minutes=45)
        if entry_dt <= dinner < exit_dt:
            lunch_duration += timedelta(minutes=30)
    else:
        lunch_1 = datetime(entry_dt.year, entry_dt.month, entry_dt.day, 13, 0)
        dinner = datetime(entry_dt.year, entry_dt.month, entry_dt.day, 19, 0)
        if entry_dt <= lunch_1 < exit_dt:
            lunch_duration += timedelta(minutes=30)
        if entry_dt <= dinner < exit_dt:
            lunch_duration += timedelta(minutes=30)

    net_duration = work_duration - lunch_duration


    data_cache["entry"] = entry_dt
    data_cache["exit"] = exit_dt
    data_cache["net_duration"] = net_duration
    return round(net_duration.total_seconds() / 3600, 2)


def calculate():
    entry = entry_input.get()
    exit = exit_input.get()
    is_weekday = weekday_var.get()
    rounded_entry = round_time(datetime.strptime(entry, "%H:%M"))
    rounded_exit = round_time(datetime.strptime(exit, "%H:%M"))
    try:
        sonuc = calculate_work_hours(entry, exit, is_weekday == "Hafta İçi")
        result_label.config(
            text=f"Net Çalışma Süresi: {sonuc}\n"
                 f"Giriş (yuvarlanmış): {rounded_entry.strftime('%H:%M')}\n"
                 f"Çıkış (yuvarlanmış): {rounded_exit.strftime('%H:%M')}"
        )
    except Exception as e:
        messagebox.showerror("Hata", f"Geçersiz giriş: {e}")


def save_json():
    try:
        if not data_cache["entry"] or not data_cache["exit"] or not data_cache["net_duration"]:
            messagebox.showwarning("Uyarı", "Lütfen önce HESAPLA butonuna basın.")
            return
        sicil_no = simpledialog.askstring("Sicil Numarası", "Sicil numaranızı giriniz:")

        if not sicil_no:
            messagebox.showinfo("Bilgi", "Kayıt iptal edildi.")
            return

        date = datetime.now().strftime("%Y-%m-%d")
        kayit = {
            "sicil": sicil_no,
            "tarih": date,
            "giris": data_cache["entry"].strftime("%H:%M"),
            "cikis": data_cache["exit"].strftime("%H:%M"),
            "net_calisma": data_cache["net_duration"].total_seconds() / 3600
        }

        # Get the universal file path
        file_name = get_file_path()

        # Read existing data or initialize an empty list
        if file_name.exists():
            with open(file_name, "r", encoding="utf-8") as f:
                veriler = json.load(f)
        else:
            veriler = []

        # Append the new record and save it
        veriler.append(kayit)
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(veriler, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Başarılı", f"Kayıt başarıyla yapıldı.\nDosya Yolu: {file_name}")
    except Exception as e:
        messagebox.showerror("Hata", f"Kayıt sırasında bir hata oluştu:\n{e}")

def display_badge_data():
    global badge_window
    
    # If window already exists, bring it to front instead of creating a new one
    if badge_window is not None and badge_window.winfo_exists():
        badge_window.lift()  # Bring existing window to front
        return
        
    try:
        badge_number = simpledialog.askstring("Sicil Numarası", "Lütfen sicil numarasını girin:")
        if not badge_number:
            return

        # Create a new window for the control table
        badge_window = tk.Toplevel(root)
        badge_window.title(f"Sicil Numarası: {badge_number}")
        badge_window.geometry("900x600")

        # Add a Treeview in the new window
        columns = ("Tarih", "Giriş", "Çıkış", "Net Çalışma (Saat)")
        tree = ttk.Treeview(badge_window, columns=columns, show="headings", height=10)
        tree.heading("Tarih", text="Tarih")
        tree.heading("Giriş", text="Giriş")
        tree.heading("Çıkış", text="Çıkış")
        tree.heading("Net Çalışma (Saat)", text="Net Çalışma (Saat)")
        tree.pack(pady=10, fill="both", expand=True)

        # Track window closure to reset the global variable
        def on_window_close():
            global badge_window
            badge_window = None
            badge_window_temp.destroy()
            
        badge_window_temp = badge_window
        badge_window.protocol("WM_DELETE_WINDOW", on_window_close)

        # Function to refresh the table
        def refresh_table():
            try:
                # Fetch the latest data from the JSON file
                data = json_open()
                filtered_data = filter_by_badge(data, badge_number)

                # Clear the existing rows in the Treeview
                for row in tree.get_children():
                    tree.delete(row)

                # Re-insert the filtered data
                for record in filtered_data:
                    tree.insert("", "end", values=(record["tarih"], record["giris"], record["cikis"], record["net_calisma"]))

                # Show a message if no data is found
                if not filtered_data:
                    messagebox.showinfo("Bilgi", f"Sicil Numarası {badge_number} için kayıt bulunamadı.")
            except Exception as e:
                messagebox.showerror("Hata", f"Tablo yenilenirken bir hata oluştu:\n{e}")

        # Initial population of the Treeview
        refresh_table()

        # Add a refresh button below the table
        refresh_button = tk.Button(badge_window, text="Yenile", command=refresh_table)
        refresh_button.pack(pady=5)

    except Exception as e:
        messagebox.showerror("Hata", f"Veri görüntüleme sırasında bir hata oluştu:\n{e}")

# Interface setup
root = tk.Tk()
root.title("Çalışma Süresi Hesaplayıcı")
root.geometry("600x400")

tk.Label(root, text="Giriş Saati (HH:MM):", font=("Helvetica", 11, "bold")).pack(pady=5)
entry_input = tk.Entry(root)
entry_input.pack(pady=5)

tk.Label(root, text="Çıkış Saati (HH:MM):", font=("Helvetica", 11, "bold")).pack(pady=5)
exit_input = tk.Entry(root)
exit_input.pack(pady=5)

weekday_var = tk.StringVar(value="Hafta İçi")
tk.Radiobutton(root, text="Hafta İçi", variable=weekday_var, value="Hafta İçi").pack()
tk.Radiobutton(root, text="Hafta Sonu", variable=weekday_var, value="Hafta Sonu").pack()

# Button frame for aligning buttons in a single row
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

calculate_button = tk.Button(button_frame, text="Hesapla", command=calculate)
calculate_button.grid(row=0, column=0, padx=10)

save_button = tk.Button(button_frame, text="Kaydet", command=save_json)
save_button.grid(row=0, column=1, padx=10)

control_button = tk.Button(button_frame, text="Sicil Kontrol", command=display_badge_data)
control_button.grid(row=0, column=2, padx=10)

# Result label
result_label = tk.Label(root, text="", font=("Helvetica", 10), justify="left")
result_label.pack(pady=10)

# Footer
footer = tk.Label(root, text="Developed by MMD", font=("Arial", 8), fg="gray")
footer.pack(side="bottom", pady=5)

root.mainloop()

