# 🖼️ Görsel & PDF Dönüştürücü ve Boyutlandırıcı (Media Converter)

Modern, hızlı ve kullanımı kolay bir masaüstü medya işleme aracı! Bu uygulama ile görsellerinizi farklı formatlara dönüştürebilir, boyutlandırabilir veya birden fazla PDF/görsel dosyasını tek bir PDF belgesinde birleştirebilirsiniz.

![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-darkgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)

---

## 🌟 Özellikler

### 🖼️ Görsel İşlemleri
* **Toplu Format Dönüştürme:** PNG, JPG, WEBP ve BMP formatları arasında kayıpsız/hızlı geçiş.
* **Akıllı Boyutlandırma:** 
  * Sabit piksel boyutlandırma (Genişlik x Yükseklik).
  * Sadece genişlik girildiğinde **orantılı (aspekt oranını koruyan)** boyutlandırma.
* **Transparan Görsel Koruması:** PNG/WEBP gibi şeffaf arka plana sahip görseller JPG'ye dönüştürülürken otomatik arka plan düzeltmesi (`RGBA` -> `RGB`).

### 📄 PDF İşlemleri
* **PDF Birleştirme:** Birden fazla PDF dosyasını sıralı bir şekilde tek bir PDF altında toplama.
* **Görsellerden PDF Oluşturma:** Seçilen birden fazla resmi (`.png`, `.jpg` vb.) tek tıkla sayfa sayfa tek bir PDF dosyasına çevirme.

---

## 🛠️ Sıfırdan Nasıl Yapılır? (Kurulum ve Çalıştırma)

Bu projeyi kendi bilgisayarınızda sıfırdan oluşturup çalıştırmak için aşağıdaki adımları sırasıyla uygulayabilirsiniz:

### 1. Adım: Proje Klasörü ve Dosyası Oluşturun
Bilgisayarınızda veya VS Code içinde yeni bir klasör oluşturun ve içine `"istediğinizad".py` adında boş bir Python dosyası açın.

### 2. Adım: Gerekli Kütüphaneleri Yükleyin
VS Code Terminalini (`Ctrl + ~`) veya Terminale basıp New Terminal (`Ctrl + shift + "`) basarak açabilrisiniz:

```bash
pip install customtkinter Pillow pypdf
```
Terminal'e bu bashi yazarak gereken kurulumu yapmış olursunuz ve açmış olduğunuz "istediğinizad".py'nin içerisine kodunuzu yazabilirsiniz.
