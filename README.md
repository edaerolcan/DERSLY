# 📚 DERSLY - Öğrenci Destek Platformu

Modern, kullanıcı dostu üniversite öğrenci yönetim sistemi.

---


## 🚀 Hızlı Başlangıç

### 🌐 Online Kullanım (Önerilen)

*Tarayıcınızdan doğrudan kullanın:*

👉 **[dersly.streamlit.app](https://dersly.streamlit.app)** 👈

- ✅ Kurulum gerektirmez
- ✅ Tüm cihazlardan erişilebilir
- ✅ Otomatik güncellemeler
- ✅ Mobil uyumlu

### 📱 Web App Olarak Kurulum (Opsiyonel)

Uygulamayı telefonunuza veya bilgisayarınıza web app olarak ekleyebilirsiniz:

**iOS (iPhone/iPad):**
1. Safari'de [dersly.streamlit.app](https://dersly.streamlit.app) açın
2. Paylaş butonuna tıklayın (⬆️)
3. "Ana Ekrana Ekle" seçin
4. Artık bir uygulama gibi kullanabilirsiniz!

**Android:**
1. Chrome'da [dersly.streamlit.app](https://dersly.streamlit.app) açın
2. Menü butonuna tıklayın (⋮)
3. "Ana ekrana ekle" seçin
4. Artık bir uygulama gibi kullanabilirsiniz!

**Desktop (Chrome/Edge):**
1. [dersly.streamlit.app](https://dersly.streamlit.app) açın
2. Adres çubuğundaki yükle simgesine tıklayın
3. "Yükle" butonuna tıklayın
4. Artık masaüstü uygulaması gibi kullanabilirsiniz!

## ✨ Özellikler

### 🎓 Akademik Yönetim
- **Ders Programı:** Haftalık ders programınızı yönetin
- **Ödev Takibi:** Ödev, sınav, proje ve quizleri takip edin
- **Not Hesaplama:** Özelleştirilebilir GPA sistemleri (4.0, 5.0, 100'lük)
- **Takvim Görünümü:** Aylık takvim ile görevlerinizi görüntüleyin

### 🔔 Hatırlatıcılar
- Aciliyet bazlı hatırlatıcılar (🔴 Acil, 🟡 Yakında, 🟢 Sonra)
- Filtreleme seçenekleri (Bugün, Yarın, Bu Hafta)
- Sidebar'da acil hatırlatıcı sayacı

### 📅 Takvim Entegrasyonu
- iCalendar (.ics) export
- Tek tıkla mobil takvime ekleme
- Toplu export (tüm görevler)
- Tekrarlayan ders programı (14 hafta)
- iOS, Android, Windows, macOS desteği

### 🎨 Modern UI/UX
- Glassmorphism tasarım
- Smooth animasyonlar
- Responsive (mobil uyumlu)
- Touch-friendly (44x44px minimum)
- Dark mode desteği

### 🚀 Akıllı Özellikler
- **Bölüm Kataloğu:** 60+ bölüm, 10 fakülte
- **Ders Önerileri:** Bölüme özel ders kataloğu
- **Zaman Dilimleri:** 19 yaygın ders saati önerisi
- **GPA Sistemleri:** 5 farklı not sistemi
- **Üniversite Presetleri:** 10 üniversite için hazır ayarlar

### 🔒 Güvenlik & Gizlilik
- Tüm veriler tarayıcıda saklanır
- Sunucuya veri gönderilmez
- Kapsamlı input validasyonu
- Türkçe hata mesajları

## � Yerel Kurulum (Geliştiriciler İçin)

Uygulamayı kendi bilgisayarınızda çalıştırmak isterseniz:

### Gereksinimler
- Python 3.8+
- pip

### Kurulum Adımları

1. **Repoyu klonlayın:**
```bash
git clone https://github.com/yourusername/dersly.git
cd dersly
```

2. **Virtual environment oluşturun:**
```bash
python -m venv venv
```

3. **Virtual environment'ı aktifleştirin:**
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

4. **Bağımlılıkları yükleyin:**
```bash
pip install -r requirements.txt
```

5. **Uygulamayı çalıştırın:**
```bash
streamlit run app.py
```

6. **Tarayıcınızda açın:**
```
http://localhost:8501
```

> **💡 Not:** Çoğu kullanıcı için online versiyon ([dersly.streamlit.app](https://dersly.streamlit.app)) daha pratiktir.

## 📖 Kullanım

### İlk Kurulum
1. Uygulamayı açın
2. İsterseniz profil oluşturun (opsiyonel)
3. Üniversitenizi ve bölümünüzü seçin
4. GPA sistemi otomatik ayarlanır

### Ders Ekleme
1. **Dersler** sayfasına gidin
2. **Yeni Ders Ekle** sekmesini açın
3. Bölümünüze göre ders önerileri görürsünüz
4. Zaman dilimi önerilerinden seçin
5. **Takvime Ekle** ile mobil takviminize ekleyin

### Ödev Ekleme
1. **Ödevler** sayfasına gidin
2. **Yeni Görev Ekle** sekmesini açın
3. Bilgileri doldurun
4. **Takvime Ekle** ile mobil takviminize ekleyin

### Not Girişi
1. **Not Ortalaması** sayfasına gidin
2. GPA sisteminiz otomatik seçili
3. Notları girin (sisteme uygun seçenekler)
4. GPA otomatik hesaplanır

### Hatırlatıcılar
1. **Hatırlatıcılar** sayfasına gidin
2. Acil görevlerinizi görün
3. Filtreleme yapın (Bugün, Yarın, Bu Hafta)
4. Sidebar'da acil sayacı takip edin

## 🎯 GPA Sistemleri

### Desteklenen Sistemler:
- **4.0 Çift Harf:** AA, BA, BB, CB, CC, DC, DD, FD, FF
- **4.0 Tek Harf:** A, B, C, D, F
- **4.0 Artı/Eksi:** A+, A, A-, B+, B, B-, ...
- **5.0 Sistem:** 5, 4, 3, 2, 1, 0
- **100 Sistem:** Yüzdelik notlar

### Üniversite Presetleri:
- Boğaziçi Üniversitesi → 4.0 Tek Harf
- İTÜ → 4.0 Çift Harf
- ODTÜ → 4.0 Tek Harf
- Koç/Sabancı → 4.0 Artı/Eksi
- Ve daha fazlası...

## 📱 Mobil Kullanım

### Responsive Tasarım:
- ✅ Mobile-first yaklaşım
- ✅ Touch-friendly butonlar (44x44px)
- ✅ Stack columns on mobile
- ✅ Collapsible sidebar
- ✅ 16px minimum font

### Takvim Entegrasyonu:
1. Ödev/ders ekleyin
2. **📅 Takvime Ekle** butonuna tıklayın
3. .ics dosyası indirilir
4. Dosyayı açın
5. Mobil takvim uygulaması otomatik açılır
6. Etkinlik eklenir, bildirimler kurulur

## 🧪 Test

### Otomatik Testler:
```bash
# Tüm testleri çalıştır
python -m pytest tests/ -v

# Sadece validation testleri
python -m pytest tests/test_input_validator.py -v

# Sadece integration testleri
python -m pytest tests/test_auth_removal.py -v
```

### Test Coverage:
- **57 test** (100% pass rate)
- **40 unit tests** (validation)
- **17 integration tests** (auth removal)

## 📊 Proje Yapısı

```
DERSLY/
├── app.py                          # Ana uygulama
├── pages/                          # Streamlit sayfaları
│   ├── 1_🏠_Ana_Sayfa.py
│   ├── 2_📚_Dersler.py
│   ├── 3_📝_Ödevler.py
│   ├── 4_📅_Takvim.py
│   ├── 5_🔔_Hatırlatıcılar.py
│   ├── 6_📊_Not_Ortalaması.py
│   └── 7_👤_Profil.py
├── utils/                          # Yardımcı modüller
│   ├── storage_manager.py         # Veri yönetimi
│   ├── user_manager.py            # Kullanıcı yönetimi
│   ├── course_manager.py          # Ders yönetimi
│   ├── assignment_manager.py      # Ödev yönetimi
│   ├── grade_manager.py           # Not yönetimi
│   ├── reminder_manager.py        # Hatırlatıcı yönetimi
│   ├── input_validator.py         # Validasyon
│   ├── calendar_export.py         # Takvim export
│   ├── department_catalog.py      # Bölüm kataloğu
│   ├── gpa_systems.py             # GPA sistemleri
│   ├── ui_styles.py               # UI stilleri
│   ├── ui_polish.py               # UI yardımcıları
│   └── mobile_utils.py            # Mobil yardımcıları
├── tests/                          # Test dosyaları
│   ├── test_input_validator.py
│   └── test_auth_removal.py
└── requirements.txt                # Python bağımlılıkları
```

## 🛠️ Teknolojiler

- **Framework:** Streamlit 1.28+
- **Language:** Python 3.8+
- **Storage:** Browser Session State
- **Styling:** Custom CSS (Glassmorphism)
- **Calendar:** iCalendar (.ics) format
- **Testing:** pytest

## 📝 Özellik Listesi

### ✅ Tamamlanan:
- [x] Ders programı yönetimi
- [x] Ödev/sınav takibi
- [x] GPA hesaplama (5 sistem)
- [x] Takvim görünümü
- [x] Hatırlatıcı sistemi
- [x] Takvim entegrasyonu (.ics)
- [x] Mobil responsive
- [x] Input validasyonu
- [x] Bölüm kataloğu
- [x] Ders önerileri
- [x] Zaman dilimi önerileri
- [x] Üniversite presetleri
- [x] Dark mode
- [x] Veri export/import

### 🔄 Gelecek Özellikler:
- [ ] Google Calendar API entegrasyonu
- [ ] Web push notifications
- [ ] PWA (Progressive Web App)
- [ ] AI destekli çalışma planı
- [ ] Sosyal özellikler
- [ ] Multi-language support

## 🤝 Katkıda Bulunma

1. Fork edin
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Commit edin (`git commit -m 'Add amazing feature'`)
4. Push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🌐 Demo & Kullanım

### Online Demo
👉 **[dersly.streamlit.app](https://dersly.streamlit.app)**

### Özellikler
- ✅ Anında kullanıma hazır
- ✅ Kurulum gerektirmez
- ✅ Ücretsiz
- ✅ Tüm özellikler aktif
- ✅ Mobil uyumlu

## 👥 İletişim

- **Live App:** [dersly.streamlit.app](https://dersly.streamlit.app)
- **GitHub:** [https://github.com/yourusername/dersly](https://github.com/yourusername/dersly)
- **Issues:** [GitHub Issues](https://github.com/yourusername/dersly/issues)

## 🙏 Teşekkürler

- Streamlit ekibine harika framework için
- Tüm katkıda bulunanlara
- Kullanıcılarımıza geri bildirimleri için

---

**Made with ❤️ for students**

**🌐 Live:** [dersly.streamlit.app](https://dersly.streamlit.app)  
**Version:** 2.0.0  
**Status:** ✅ Production Ready  
**Last Updated:** 2024
