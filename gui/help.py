# gui/help.py
import tkinter as tk
from tkinter import ttk, scrolledtext
from gui.preferences import preferences

class HelpContent:
    """Help content for the application."""
    
    # Help content in both Turkish and English
    CONTENT = {
        "tr": {
            "overview": {
                "title": "Genel Bakış",
                "content": """Çalışma Saati Hesaplama uygulaması, iş saatlerinizi kolayca hesaplamanızı ve kaydetmenizi sağlar.

Temel Özellikler:
• Giriş ve çıkış saatlerinden net çalışma süresini hesaplama
• Yemek ve mola sürelerini otomatik düşme
• Hafta içi ve hafta sonu farklı mola süreleri
• Çeşitli zaman yuvarlama seçenekleri
• Sicil numarasına göre kayıtları saklama ve görüntüleme
• Sicil kayıtlarını JSON formatında saklama"""
            },
            "calculation": {
                "title": "Hesaplama",
                "content": """Çalışma süresi hesaplamak için:

1. Giriş saatini HH:MM formatında girin (örn: 08:30)
2. Çıkış saatini HH:MM formatında girin (örn: 17:45)
3. Hafta içi veya Hafta sonu seçeneğini işaretleyin
4. "Hesapla" düğmesine tıklayın

Sonuç, girdiğiniz saatler arasındaki net çalışma süresini gösterecektir. Yemek molaları tercihlerinize göre otomatik olarak düşülür."""
            },
            "rounding": {
                "title": "Zaman Yuvarlama",
                "content": """Aşağıdaki yuvarlama algoritmaları mevcuttur:

• Standart (15 dakika): Klasik çeyrek saat yuvarlaması
• En yakın 5 dakika: En yakın 5 dakikaya yuvarlama
• En yakın 10 dakika: En yakın 10 dakikaya yuvarlama
• En yakın 30 dakika: En yakın 30 dakikaya yuvarlama
• Yukarı yuvarlama: Sonraki 15 dakikaya yuvarlama
• Aşağı yuvarlama: Önceki 15 dakikaya yuvarlama

Yuvarlama algoritmasını değiştirmek için: Araçlar > Tercihler > Genel > Yuvarlama Algoritması"""
            },
            "breaks": {
                "title": "Molalar",
                "content": """Uygulama varsayılan olarak şu molaları düşer:

Hafta İçi:
• Öğle molası: 13:00-13:45 (45 dakika)
• Akşam molası: 19:00-19:30 (30 dakika)

Hafta Sonu:
• Öğle molası: 13:00-13:30 (30 dakika)
• Akşam molası: 19:00-19:30 (30 dakika)

Mola saatlerini değiştirmek için: 
Araçlar > Tercihler > Hafta İçi Molaları / Hafta Sonu Molaları

Molalar sadece çalışma saatleri içinde düşülür. Örneğin, 8:00-13:00 arası çalışıyorsanız, akşam molası düşülmez."""
            },
            "save": {
                "title": "Kaydetme",
                "content": """Hesapladığınız çalışma süresini JSON formatında kaydetmek için:

1. "Hesapla" düğmesine basın
2. "Kaydet" düğmesine basın
3. İstendiğinde sicil numaranızı girin

Kayıtlar, JSON formatında saklanır ve sicil numarasına göre filtrelenebilir. 
Kayıtlar varsayılan olarak aşağıdaki konumda saklanır:
• Windows: Belgelerim/calisma_saati_hesaplama.json
• Linux/Mac: ~/Documents/calisma_saati_hesaplama.json

Farklı bir dosya seçmek için: Dosya > Yeni veya Dosya > Aç seçeneklerini kullanabilirsiniz."""
            },
            "badge_control": {
                "title": "Sicil Kontrol",
                "content": """Sicil numaralarına ait kayıtları görüntülemek için:

1. "Sicil Kontrol" düğmesine tıklayın
2. Görüntülenen tabloda tüm kayıtlar listelenir
3. Arama kutusunu kullanarak belirli bir sicil numarasını filtreleyebilirsiniz
4. Bir kaydı silmek için, kaydı seçin ve sağ tıklayarak "Sil" seçeneğini kullanın

Tablodaki veriler, seçili JSON dosyasından okunur."""
            },
            "preferences": {
                "title": "Tercihler",
                "content": """Uygulama tercihlerini değiştirmek için: Araçlar > Tercihler

Genel Sekmesi:
• Dil: Arayüz dilini değiştirin (Türkçe/İngilizce)
• Yuvarlama Algoritması: Zaman yuvarlama yöntemini seçin

Hafta İçi Molaları Sekmesi:
• Öğle ve akşam molalarını hafta içi günler için yapılandırın

Hafta Sonu Molaları Sekmesi:
• Öğle ve akşam molalarını hafta sonu günler için yapılandırın

Tercihler, işletim sisteminize bağlı olarak aşağıdaki konumlarda saklanır:
• Windows: C:\\Users\\<kullanıcı>\\AppData\\Local\\CalismaSaatiHesaplama\\preferences.json
• Linux/Mac: ~/.calisma_saati_hesaplama/preferences.json"""
            }
        },
        "en": {
            "overview": {
                "title": "Overview",
                "content": """The Working Hours Calculator application allows you to easily calculate and save your working hours.

Key Features:
• Calculate net working time from entry and exit times
• Automatically deduct meal and break times
• Different break durations for weekdays and weekends
• Various time rounding options
• Store and view records by badge number
• Save badge records in JSON format"""
            },
            "calculation": {
                "title": "Calculation",
                "content": """To calculate working hours:

1. Enter entry time in HH:MM format (e.g., 08:30)
2. Enter exit time in HH:MM format (e.g., 17:45)
3. Select Weekday or Weekend option
4. Click the "Calculate" button

The result will show the net working hours between the times you entered. Meal breaks are automatically deducted according to your preferences."""
            },
            "rounding": {
                "title": "Time Rounding",
                "content": """The following rounding algorithms are available:

• Standard (15 minutes): Classic quarter-hour rounding
• Nearest 5 minutes: Round to the nearest 5 minutes
• Nearest 10 minutes: Round to the nearest 10 minutes
• Nearest 30 minutes: Round to the nearest 30 minutes
• Ceiling: Round up to the next 15 minutes
• Floor: Round down to the previous 15 minutes

To change the rounding algorithm: Tools > Preferences > General > Rounding Algorithm"""
            },
            "breaks": {
                "title": "Breaks",
                "content": """By default, the application deducts the following breaks:

Weekdays:
• Lunch break: 13:00-13:45 (45 minutes)
• Dinner break: 19:00-19:30 (30 minutes)

Weekends:
• Lunch break: 13:00-13:30 (30 minutes)
• Dinner break: 19:00-19:30 (30 minutes)

To change break times:
Tools > Preferences > Weekday Breaks / Weekend Breaks

Breaks are only deducted if they fall within working hours. For example, if you work from 8:00-13:00, the dinner break is not deducted."""
            },
            "save": {
                "title": "Saving",
                "content": """To save your calculated working time in JSON format:

1. Press the "Calculate" button
2. Press the "Save" button
3. Enter your badge number when prompted

Records are stored in JSON format and can be filtered by badge number.
By default, records are stored at:
• Windows: My Documents/calisma_saati_hesaplama.json
• Linux/Mac: ~/Documents/calisma_saati_hesaplama.json

To select a different file: Use File > New or File > Open options."""
            },
            "badge_control": {
                "title": "Badge Control",
                "content": """To view records by badge number:

1. Click the "Badge Control" button
2. All records will be listed in the displayed table
3. Use the search box to filter for a specific badge number
4. To delete a record, select it and use the "Delete" option by right-clicking

Data in the table is read from the selected JSON file."""
            },
            "preferences": {
                "title": "Preferences",
                "content": """To change application preferences: Tools > Preferences

General Tab:
• Language: Change the interface language (Turkish/English)
• Rounding Algorithm: Select the time rounding method

Weekday Breaks Tab:
• Configure lunch and dinner breaks for weekdays

Weekend Breaks Tab:
• Configure lunch and dinner breaks for weekends

Preferences are stored at the following locations depending on your operating system:
• Windows: C:\\Users\\<username>\\AppData\\Local\\CalismaSaatiHesaplama\\preferences.json
• Linux/Mac: ~/.calisma_saati_hesaplama/preferences.json"""
            }
        }
    }
    
    @classmethod
    def get_help_sections(cls):
        """Get available help sections."""
        # Get current language from preferences
        language = preferences.get("language", "tr")
        
        # Return section titles
        return [(section, data["title"]) for section, data in cls.CONTENT[language].items()]
    
    @classmethod
    def get_help_content(cls, section):
        """Get help content for a specific section."""
        # Get current language from preferences
        language = preferences.get("language", "tr")
        
        # Return content for the requested section
        if section in cls.CONTENT[language]:
            return cls.CONTENT[language][section]
        return {"title": "Error", "content": "Help section not found"}

class HelpDialog:
    """Dialog for displaying help content."""
    
    def __init__(self, parent):
        self.parent = parent
        self.window = None
        
    def show(self):
        # If window already exists, bring it to front
        if self.window is not None and self.window.winfo_exists():
            self.window.lift()
            return
            
        # Create a new window for help
        self.window = tk.Toplevel(self.parent)
        language = preferences.get("language", "tr")
        help_title = "Help" if language == "en" else "Yardım"
        self.window.title(help_title)
        self.window.geometry("700x500")
        self.window.minsize(600, 400)
        
        # Create a frame for the table of contents
        toc_frame = tk.Frame(self.window, width=200, borderwidth=1, relief=tk.GROOVE)
        toc_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
        
        # Create a frame for the help content
        content_frame = tk.Frame(self.window)
        content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add title for the table of contents
        language = preferences.get("language", "tr")
        toc_title = "İçindekiler" if language == "tr" else "Contents"
        tk.Label(toc_frame, text=toc_title, font=("Helvetica", 12, "bold")).pack(pady=5)
        
        # Get help sections
        sections = HelpContent.get_help_sections()
        
        # Create buttons for each section
        for section_id, section_title in sections:
            btn = tk.Button(
                toc_frame, 
                text=section_title,
                anchor="w",
                padx=10,
                command=lambda s=section_id: self.show_section(s)
            )
            btn.pack(fill=tk.X, pady=2)
        
        # Create a title label for the content
        self.content_title = tk.Label(content_frame, text="", font=("Helvetica", 14, "bold"))
        self.content_title.pack(pady=10, anchor="w")
        
        # Create a text widget for the help content with scrollbars
        self.content_text = scrolledtext.ScrolledText(
            content_frame, 
            wrap=tk.WORD,
            width=50,
            height=20,
            font=("Helvetica", 11)
        )
        self.content_text.pack(fill=tk.BOTH, expand=True)
        self.content_text.config(state=tk.DISABLED)  # Make read-only
        
        # Show the overview section by default
        self.show_section("overview")
    
    def show_section(self, section):
        """Show the selected help section."""
        help_content = HelpContent.get_help_content(section)
        
        # Update title
        self.content_title.config(text=help_content["title"])
        
        # Update content
        self.content_text.config(state=tk.NORMAL)
        self.content_text.delete(1.0, tk.END)
        self.content_text.insert(tk.END, help_content["content"])
        self.content_text.config(state=tk.DISABLED)