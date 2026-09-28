import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
from pypdf import PdfWriter

# Tema Ayarları (Modern Koyu Tema)
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class MediaConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Görsel & PDF Dönüştürücü")
        self.geometry("600 x 550")
        self.resizable(False, False)

        self.secilen_dosyalar = []

        # --- ARAYÜZ ELEMANLARI ---
        
        # Başlık
        self.baslik = ctk.CTkLabel(
            self, text="Görsel & PDF İşleme Aracı", font=ctk.CTkFont(size=22, weight="bold")
        )
        self.baslik.pack(pady=15)

        # Dosya Seçim Alanı
        self.btn_dosya_sec = ctk.CTkButton(
            self, text="📁 Dosya(lar) Seç", command=self.dosya_sec, width=200, height=40
        )
        self.btn_dosya_sec.pack(pady=10)

        # Seçilen Dosya Sayısı Etiketi
        self.lbl_dosya_durum = ctk.CTkLabel(
            self, text="Henüz dosya seçilmedi", font=ctk.CTkFont(size=13)
        )
        self.lbl_dosya_durum.pack(pady=5)

        # TABVIEW (İki Farklı Mod: Görsel ve PDF)
        self.tabview = ctk.CTkTabview(self, width=540, height=280)
        self.tabview.pack(pady=15)

        self.tab_gorsel = self.tabview.add("🖼️ Görsel İşlemleri")
        self.tab_pdf = self.tabview.add("📄 PDF İşlemleri")

        self.gorsel_sekmesini_kur()
        self.pdf_sekmesini_kur()

        # Alt Durum Çubuğu
        self.lbl_alt_durum = ctk.CTkLabel(
            self, text="Hazır", font=ctk.CTkFont(size=12), text_color="gray"
        )
        self.lbl_alt_durum.pack(side="bottom", pady=10)

    # --- GÖRSEL SEKME DÜZENİ ---
    def gorsel_sekmesini_kur(self):
        # Format Seçimi
        self.lbl_format = ctk.CTkLabel(self.tab_gorsel, text="Hedef Format:")
        self.lbl_format.grid(row=0, column=0, padx=15, pady=10, sticky="w")

        self.combo_format = ctk.CTkComboBox(
            self.tab_gorsel, values=["PNG", "JPG", "WEBP", "BMP"]
        )
        self.combo_format.grid(row=0, column=1, padx=15, pady=10)

        # Boyutlandırma (Genişlik / Yükseklik)
        self.lbl_genislik = ctk.CTkLabel(self.tab_gorsel, text="Genişlik (px):")
        self.lbl_genislik.grid(row=1, column=0, padx=15, pady=10, sticky="w")

        self.ent_genislik = ctk.CTkEntry(self.tab_gorsel, placeholder_text="Orijinal")
        self.ent_genislik.grid(row=1, column=1, padx=15, pady=10)

        self.lbl_yukseklik = ctk.CTkLabel(self.tab_gorsel, text="Yükseklik (px):")
        self.lbl_yukseklik.grid(row=2, column=0, padx=15, pady=10, sticky="w")

        self.ent_yukseklik = ctk.CTkEntry(self.tab_gorsel, placeholder_text="Orijinal")
        self.ent_yukseklik.grid(row=2, column=1, padx=15, pady=10)

        # Dönüştür Butonu
        self.btn_gorsel_islem = ctk.CTkButton(
            self.tab_gorsel, text="Görselleri Dönüştür / Boyutlandır", command=self.gorsel_dondur
        )
        self.btn_gorsel_islem.grid(row=3, column=0, columnspan=2, pady=20)

    # --- PDF SEKME DÜZENİ ---
    def pdf_sekmesini_kur(self):
        self.lbl_pdf_bilgi = ctk.CTkLabel(
            self.tab_pdf,
            text="Seçtiğiniz birden fazla PDF dosyasını tek bir PDF'te birleştirebilir\nveya görselleri tek bir PDF haline getirebilirsiniz.",
            justify="center"
        )
        self.lbl_pdf_bilgi.pack(pady=20)

        self.btn_pdf_birlestir = ctk.CTkButton(
            self.tab_pdf, text="PDF / Görselleri Tek PDF Yap", command=self.pdf_birlestir
        )
        self.btn_pdf_birlestir.pack(pady=10)

    # --- FONKSİYONLAR VE MANTIK ---
    def dosya_sec(self):
        dosyalar = filedialog.askopenfilenames(
            title="Dosya Seç",
            filetypes=[
                ("Tüm Desteklenenler", "*.png *.jpg *.jpeg *.webp *.bmp *.pdf"),
                ("Görseller", "*.png *.jpg *.jpeg *.webp *.bmp"),
                ("PDF Dosyaları", "*.pdf")
            ]
        )
        if dosyalar:
            self.secilen_dosyalar = list(dosyalar)
            self.lbl_dosya_durum.configure(text=f"{len(self.secilen_dosyalar)} dosya seçildi.")
            self.lbl_alt_durum.configure(text="Dosyalar yüklendi.")

    def gorsel_dondur(self):
        if not self.secilen_dosyalar:
            messagebox.showwarning("Uyarı", "Lütfen önce görsel dosya(ları) seçin!")
            return

        hedef_klasor = filedialog.askdirectory(title="Kayıt Klasörünü Seçin")
        if not hedef_klasor:
            return

        hedef_format = self.combo_format.get().lower()
        if hedef_format == "jpg":
            hedef_format = "jpeg"

        genislik_str = self.ent_genislik.get().strip()
        yukseklik_str = self.ent_yukseklik.get().strip()

        basarili_sayisi = 0

        for dosya_yolu in self.secilen_dosyalar:
            try:
                # PDF ise es geç
                if dosya_yolu.lower().endswith('.pdf'):
                    continue

                img = Image.open(dosya_yolu)

                # Renk Modı Kontrolü (PNG'deki Transparanlığı JPEG yaparken beyaza çevirme)
                if img.mode in ("RGBA", "P") and hedef_format == "jpeg":
                    img = img.convert("RGB")

                # Boyutlandırma
                if genislik_str.isdigit() and yukseklik_str.isdigit():
                    yeni_boyut = (int(genislik_str), int(yukseklik_str))
                    img = img.resize(yeni_boyut, Image.Resampling.LANCZOS)
                elif genislik_str.isdigit():
                    # Orantılı boyutlandırma (Sadece genişlik girildiyse)
                    w = int(genislik_str)
                    w_orani = w / float(img.size[0])
                    h = int(float(img.size[1]) * float(w_orani))
                    img = img.resize((w, h), Image.Resampling.LANCZOS)

                # Yeni Dosya Adı
                dosya_adi = os.path.splitext(os.path.basename(dosya_yolu))[0]
                yeni_dosya_yolu = os.path.join(hedef_klasor, f"{dosya_adi}_yeni.{hedef_format}")

                img.save(yeni_dosya_yolu, format=hedef_format.upper())
                basarili_sayisi += 1

            except Exception as e:
                print(f"Hata ({dosya_yolu}): {e} - converter_app.py:165")

        self.lbl_alt_durum.configure(text=f"{basarili_sayisi} görsel dönüştürüldü.")
        messagebox.showinfo("Başarılı", f"{basarili_sayisi} adet görsel başarıyla işlendi ve kaydedildi!")

    def pdf_birlestir(self):
        if not self.secilen_dosyalar:
            messagebox.showwarning("Uyarı", "Lütfen önce dosya(ları) seçin!")
            return

        kayit_yolu = filedialog.asksaveasfilename(
            title="PDF Olarak Kaydet",
            defaultextension=".pdf",
            filetypes=[("PDF Dosyası", "*.pdf")]
        )

        if not kayit_yolu:
            return

        try:
            # Seçilenler PDF dosyaları ise birleştir
            pdf_dosyalari = [d for d in self.secilen_dosyalar if d.lower().endswith('.pdf')]
            gorsel_dosyalari = [d for d in self.secilen_dosyalar if not d.lower().endswith('.pdf')]

            if pdf_dosyalari:
                merger = PdfWriter()
                for pdf in pdf_dosyalari:
                    merger.append(pdf)
                merger.write(kayit_yolu)
                merger.close()

            # Seçilenler görsel ise görselleri tek bir PDF yap
            elif gorsel_dosyalari:
                islenmis_gorseller = []
                for gorsel in gorsel_dosyalari:
                    img = Image.open(gorsel)
                    if img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    islenmis_gorseller.append(img)

                if islenmis_gorseller:
                    ilk_gorsel = islenmis_gorseller[0]
                    kalan_gorseller = islenmis_gorseller[1:]
                    ilk_gorsel.save(kayit_yolu, save_all=True, append_images=kalan_gorseller)

            self.lbl_alt_durum.configure(text="PDF oluşturuldu.")
            messagebox.showinfo("Başarılı", "PDF başarıyla oluşturuldu!")

        except Exception as e:
            messagebox.showerror("Hata", f"PDF oluşturulurken bir hata çıktı: {e}")

if __name__ == "__main__":
    app = MediaConverterApp()
    app.mainloop()
