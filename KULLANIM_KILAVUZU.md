# DERSLY Kullanım Kılavuzu 📖

## Veri Yönetimi Rehberi

### 📥 Veri Dışa Aktarma (Export)

Verilerinizi yedeklemek için:

1. **Profil Sayfasına Gidin**
   - Sol menüden "👤 Profil" seçeneğine tıklayın

2. **Veri Yönetimi Sekmesini Açın**
   - "💾 Veri Yönetimi" sekmesine geçin

3. **Verileri İndirin**
   - "📥 Verileri İndir" butonuna tıklayın
   - Sistem otomatik olarak bir JSON dosyası oluşturacaktır
   - Dosya adı: `dersly_backup_YYYY-MM-DD_HH-MM-SS.json`
   - "💾 Dosyayı Kaydet" butonuna tıklayarak indirin

4. **Yedek Dosyasını Saklayın**
   - Dosyayı güvenli bir yere kaydedin
   - Google Drive, Dropbox gibi bulut depolama servislerini kullanabilirsiniz
   - Birden fazla yedek tutmanız önerilir

### 📤 Veri İçe Aktarma (Import)

Yedek dosyanızı geri yüklemek için:

1. **Profil Sayfasına Gidin**
   - Sol menüden "👤 Profil" seçeneğine tıklayın

2. **Veri Yönetimi Sekmesini Açın**
   - "💾 Veri Yönetimi" sekmesine geçin

3. **Yedek Dosyasını Seçin**
   - "JSON dosyası seçin" alanına tıklayın
   - Daha önce indirdiğiniz yedek dosyasını seçin

4. **Dosya Önizlemesini İnceleyin**
   - Sistem dosyadaki verileri gösterecektir
   - Profil, ders, ödev, not sayılarını kontrol edin

5. **Uyarıları Okuyun**
   - ⚠️ Mevcut verileriniz silinecektir!
   - Onay kutusunu işaretleyin

6. **Verileri İçe Aktarın**
   - "📤 Verileri İçe Aktar" butonuna tıklayın
   - Sayfa otomatik olarak yenilenecektir

### 🗑️ Tüm Verileri Temizleme

Baştan başlamak için tüm verileri silmek isterseniz:

1. **Profil Sayfasına Gidin**
   - Sol menüden "👤 Profil" seçeneğine tıklayın

2. **Ayarlar Sekmesini Açın**
   - "⚙️ Ayarlar" sekmesine geçin

3. **Tehlikeli Bölge**
   - "🗑️ Tüm Verileri Temizle" bölümüne gidin

4. **Uyarıları Okuyun**
   - 🚨 Bu işlem geri alınamaz!
   - Önce verilerinizi dışa aktarmanız önerilir

5. **Onay Kutularını İşaretleyin**
   - İki onay kutusunu da işaretleyin
   - "🗑️ TÜM VERİLERİ SİL" butonu aktif olacaktır

6. **Verileri Silin**
   - Butona tıklayın
   - Tüm veriler silinecek ve sistem sıfırlanacaktır

## 💡 En İyi Uygulamalar

### Düzenli Yedekleme

**Önerilen Yedekleme Sıklığı:**
- 📅 **Haftalık**: Normal kullanım için
- 📅 **Günlük**: Yoğun dönemlerde (sınav haftası, proje teslimi)
- 📅 **Her Önemli Değişiklikten Sonra**: Çok sayıda veri girişi yaptıysanız

**Yedekleme Stratejisi:**
```
Örnek Yedekleme Takvimi:
- Her Pazar akşamı: Haftalık yedek
- Önemli değişikliklerden sonra: Anlık yedek
- Ay sonu: Aylık arşiv yedek
```

### Yedek Dosyası Organizasyonu

**Dosya İsimlendirme:**
```
dersly_backup_2024-10-29_20-30.json  ← Otomatik isim
dersly_haftalik_2024-10-29.json      ← Özel isim
dersly_donem_sonu_2024-06.json       ← Dönem arşivi
```

**Klasör Yapısı:**
```
Belgelerim/
└── DERSLY_Yedekler/
    ├── 2024/
    │   ├── Ekim/
    │   │   ├── dersly_backup_2024-10-01.json
    │   │   ├── dersly_backup_2024-10-08.json
    │   │   └── dersly_backup_2024-10-15.json
    │   └── Kasım/
    └── Arsiv/
        └── dersly_donem_sonu_2024-06.json
```

### Farklı Cihazlarda Kullanım

**Senaryo 1: Ev ve Okul Bilgisayarı**

1. **Ev Bilgisayarında:**
   - Verilerinizi girin
   - Çalışma bitiminde dışa aktarın
   - Dosyayı bulut depolamaya yükleyin

2. **Okul Bilgisayarında:**
   - Bulut depolamadan dosyayı indirin
   - DERSLY'yi açın ve verileri içe aktarın
   - Çalışmaya devam edin
   - Bitiminde tekrar dışa aktarın

**Senaryo 2: Bilgisayar ve Tablet**

1. **Bilgisayarda:**
   - Normal kullanım
   - Düzenli yedekleme

2. **Tablette:**
   - Yedek dosyasını içe aktarın
   - Sadece görüntüleme veya küçük değişiklikler
   - Önemli değişiklikler için bilgisayarı kullanın

### Veri Güvenliği

**Yedek Dosyası Güvenliği:**

1. **Şifreleme (Opsiyonel)**
   ```
   - Yedek dosyasını şifreli bir arşive koyun
   - 7-Zip, WinRAR gibi araçlar kullanın
   - Güçlü bir şifre belirleyin
   ```

2. **Bulut Depolama**
   ```
   Önerilen Servisler:
   - Google Drive (15 GB ücretsiz)
   - Dropbox (2 GB ücretsiz)
   - OneDrive (5 GB ücretsiz)
   ```

3. **Yerel Yedekleme**
   ```
   - USB bellek
   - Harici disk
   - Bilgisayarınızın farklı bir klasörü
   ```

## 🚨 Sorun Giderme

### Veriler Kayboldu

**Neden Kayboluyor?**
- Tarayıcı önbelleği temizlendi
- Farklı tarayıcı kullanıldı
- Farklı cihaz kullanıldı
- Tarayıcı gizli mod kullanıldı

**Çözüm:**
1. En son yedek dosyanızı bulun
2. Profil > Veri Yönetimi > İçe Aktar
3. Yedek dosyasını seçin ve yükleyin

### Import Hatası

**Hata: "Geçersiz JSON dosyası"**
- Dosyanın DERSLY yedek dosyası olduğundan emin olun
- Dosya uzantısının `.json` olduğunu kontrol edin
- Dosyayı bir metin editöründe açıp bozuk olmadığını kontrol edin

**Hata: "Veri formatı uyumsuz"**
- Eski bir DERSLY versiyonundan yedek alınmış olabilir
- En güncel DERSLY versiyonunu kullanın
- Farklı bir yedek dosyası deneyin

### Depolama Alanı Doldu

**Belirtiler:**
- Yeni veri eklenemiyor
- Uygulama yavaşladı
- Uyarı mesajları görünüyor

**Çözüm:**
1. Verilerinizi dışa aktarın (yedek alın)
2. Eski/gereksiz verileri silin:
   - Tamamlanmış eski ödevler
   - Geçmiş dönem notları (arşivlediyseniz)
   - Kullanılmayan dersler
3. Gerekirse tüm verileri temizleyip yeniden başlayın

## 📊 Depolama Limitleri

**Tarayıcı Depolama Kapasitesi:**
- Chrome: ~10 MB
- Firefox: ~10 MB
- Safari: ~5 MB
- Edge: ~10 MB

**Ortalama Veri Boyutları:**
- Profil: ~1 KB
- Ders (1 adet): ~0.5 KB
- Ödev (1 adet): ~1 KB
- Not (1 adet): ~0.5 KB

**Örnek Hesaplama:**
```
100 ders + 200 ödev + 50 not = ~300 KB
Bu, depolama limitinin sadece %3'ü!
```

## 🎯 İpuçları

### Verimli Veri Yönetimi

1. **Dönem Sonu Temizliği**
   - Her dönem sonunda verileri dışa aktarın
   - Eski dönem verilerini temizleyin
   - Yeni döneme temiz başlayın

2. **Seçici Yedekleme**
   - Sadece aktif dönem verilerini tutun
   - Eski dönemleri arşiv dosyalarında saklayın

3. **Düzenli Kontrol**
   - Ayda bir depolama bilgilerini kontrol edin
   - Gereksiz verileri temizleyin

### Veri Kaybını Önleme

**Altın Kurallar:**
1. ✅ Her hafta yedek alın
2. ✅ Yedekleri farklı yerlerde saklayın
3. ✅ Önemli değişikliklerden sonra yedek alın
4. ✅ Tarayıcı önbelleğini temizlemeden önce yedek alın
5. ✅ Farklı cihaza geçmeden önce yedek alın

**Yedekleme Kontrol Listesi:**
```
□ Haftalık yedek alındı mı?
□ Yedek dosyası bulut depolamada mı?
□ Yedek dosyası yerel diskte mi?
□ Yedek dosyası açılıyor mu?
□ Son değişiklikler yedekte mi?
```

## 📞 Yardım

Daha fazla yardım için:
- README.md dosyasını okuyun
- GitHub Issues'da soru sorun
- Uygulama içi ipuçlarını inceleyin

---

**Son Güncelleme:** Ekim 2024
**Versiyon:** 2.0.0 (Browser Storage)
