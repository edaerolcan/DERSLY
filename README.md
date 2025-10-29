# DERSLY - Öğrenci Destek Platformu 📚

Üniversite öğrencileri için ders programı, ödev takibi ve not yönetimi uygulaması.

## 🌟 Özellikler

- **📚 Ders Yönetimi**: Haftalık ders programınızı oluşturun ve yönetin
- **📝 Ödev Takibi**: Ödev, sınav, proje ve quizlerinizi takip edin
- **📊 GPA Hesaplama**: Notlarınızı girin ve GPA'nizi otomatik hesaplayın
- **📅 Takvim Görünümü**: Görevlerinizi aylık takvimde görüntüleyin
- **💾 Veri Yedekleme**: Verilerinizi JSON formatında dışa/içe aktarın
- **🔒 Gizlilik**: Verileriniz sadece tarayıcınızda saklanır

## 🚀 Kurulum

### Gereksinimler

- Python 3.8 veya üzeri
- pip (Python paket yöneticisi)

### Adımlar

1. Repoyu klonlayın:
```bash
git clone https://github.com/yourusername/DERSLY.git
cd DERSLY
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Uygulamayı çalıştırın:
```bash
streamlit run app.py
```

4. Tarayıcınızda `http://localhost:8501` adresine gidin

## 📖 Kullanım

### İlk Kullanım

1. Uygulama açıldığında profil oluşturma ekranı gelecektir
2. Ad, soyad ve e-posta bilgilerinizi girin
3. İsteğe bağlı olarak öğrenci no, bölüm ve sınıf bilgilerini ekleyin
4. "Profil Oluştur" butonuna tıklayın

### Ders Ekleme

1. Sol menüden "📚 Dersler" sayfasına gidin
2. "Yeni Ders Ekle" sekmesini seçin
3. Ders bilgilerini doldurun (ad, kod, gün, saat, kredi)
4. "Ders Ekle" butonuna tıklayın

### Ödev Ekleme

1. Sol menüden "📝 Ödevler" sayfasına gidin
2. "Yeni Görev Ekle" sekmesini seçin
3. Görev bilgilerini doldurun (başlık, tür, bitiş tarihi, öncelik)
4. "Görev Ekle" butonuna tıklayın

### Not Girme ve GPA Hesaplama

1. Sol menüden "📊 Not Ortalaması" sayfasına gidin
2. "Not Ekle" sekmesini seçin
3. Ders adı, not (0-4 arası), kredi, dönem ve yıl bilgilerini girin
4. "Not Ekle" butonuna tıklayın
5. GPA'niz otomatik olarak hesaplanacaktır

### Veri Yedekleme

1. Sol menüden "👤 Profil" sayfasına gidin
2. "Veri Yönetimi" sekmesini seçin
3. "Verileri İndir" butonuna tıklayın
4. JSON dosyası bilgisayarınıza indirilecektir

### Veri Geri Yükleme

1. Sol menüden "👤 Profil" sayfasına gidin
2. "Veri Yönetimi" sekmesini seçin
3. "JSON dosyası seçin" alanından yedek dosyanızı seçin
4. Uyarıları okuyun ve onaylayın
5. "Verileri İçe Aktar" butonuna tıklayın

## 💾 Veri Depolama

**Önemli:** DERSLY verilerinizi tarayıcınızın session state'inde saklar. Bu şu anlama gelir:

- ✅ Verileriniz sadece sizin cihazınızda kalır (gizlilik)
- ✅ Veritabanı kurulumu gerektirmez (kolay kullanım)
- ✅ Hızlı veri erişimi (performans)
- ⚠️ Tarayıcı kapatıldığında veriler kaybolur
- ⚠️ Farklı cihazlar arasında otomatik senkronizasyon yok

### Öneriler

1. **Düzenli Yedekleme**: Verilerinizi her hafta dışa aktarın
2. **Güvenli Saklama**: Yedek dosyalarınızı güvenli bir yerde saklayın
3. **Cihaz Değişikliği**: Farklı cihazda kullanmak için veri aktarımı yapın
4. **Tarayıcı Temizliği**: Tarayıcı önbelleğini temizlerken dikkatli olun

## 🌐 Streamlit Cloud'a Deploy

1. GitHub'a push edin:
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. [Streamlit Cloud](https://streamlit.io/cloud)'a gidin
3. "New app" butonuna tıklayın
4. Repository'nizi seçin
5. Main file path: `app.py`
6. "Deploy" butonuna tıklayın

**Not:** Veritabanı konfigürasyonu gerekmez!

## 🛠️ Teknolojiler

- **Streamlit**: Web arayüzü
- **Python**: Backend logic
- **Session State**: Veri depolama
- **JSON**: Veri export/import formatı

## 📁 Proje Yapısı

```
DERSLY/
├── app.py                      # Ana uygulama dosyası
├── config.py                   # Konfigürasyon ayarları
├── requirements.txt            # Python bağımlılıkları
├── .env                        # Ortam değişkenleri
├── utils/                      # Yardımcı modüller
│   ├── storage_manager.py      # Veri depolama yönetimi
│   ├── user_manager.py         # Kullanıcı profil yönetimi
│   ├── course_manager.py       # Ders yönetimi
│   ├── assignment_manager.py   # Ödev yönetimi
│   ├── grade_manager.py        # Not yönetimi
│   ├── export_import_ui.py     # Export/Import UI bileşenleri
│   ├── exceptions.py           # Özel exception sınıfları
│   ├── validators.py           # Veri doğrulama
│   ├── calculations.py         # Hesaplama fonksiyonları
│   └── ui_helpers.py           # UI yardımcı fonksiyonları
└── pages/                      # Streamlit sayfaları
    ├── 1_🏠_Home.py            # Ana sayfa
    ├── 2_📚_Courses.py         # Dersler sayfası
    ├── 3_📝_Assignments.py     # Ödevler sayfası
    ├── 4_📅_Calendar.py        # Takvim sayfası
    ├── 5_🔔_Reminders.py       # Hatırlatıcılar sayfası
    ├── 6_📊_GPA.py             # GPA sayfası
    └── 7_👤_Profile.py         # Profil sayfası
```

## 🔧 Geliştirme

### Yeni Özellik Ekleme

1. Yeni bir branch oluşturun:
```bash
git checkout -b feature/yeni-ozellik
```

2. Değişikliklerinizi yapın ve test edin

3. Commit edin:
```bash
git add .
git commit -m "Yeni özellik: açıklama"
```

4. Push edin:
```bash
git push origin feature/yeni-ozellik
```

### Kod Standartları

- PEP 8 Python stil kılavuzunu takip edin
- Fonksiyonlar için docstring yazın
- Anlamlı değişken isimleri kullanın
- Hata yönetimi ekleyin

## 🐛 Sorun Giderme

### Uygulama Açılmıyor

```bash
# Paketleri yeniden yükleyin
pip install -r requirements.txt --upgrade

# Streamlit cache'i temizleyin
streamlit cache clear
```

### Veriler Kayboldu

- Tarayıcı önbelleğini temizlediyseniz veriler kaybolmuş olabilir
- Yedek dosyanızı kullanarak verileri geri yükleyin
- Gelecekte düzenli yedekleme yapın

### Import Hatası

- JSON dosyasının geçerli bir DERSLY yedek dosyası olduğundan emin olun
- Dosyanın bozuk olmadığını kontrol edin
- Farklı bir yedek dosyası deneyin

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:

1. Fork edin
2. Feature branch oluşturun
3. Değişikliklerinizi commit edin
4. Branch'inizi push edin
5. Pull Request açın

## 📧 İletişim

Sorularınız veya önerileriniz için:
- Issue açın
- Pull Request gönderin

## 🙏 Teşekkürler

DERSLY'yi kullandığınız için teşekkür ederiz! Üniversite hayatınızda başarılar dileriz! 🎓

---

**Not:** Bu uygulama eğitim amaçlıdır ve sürekli geliştirilmektedir.
