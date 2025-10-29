# 🎓 YÖK Atlas API Entegrasyonu

## 📚 Genel Bakış

DERSLY artık **YÖK Atlas API** kullanarak gerçek zamanlı üniversite ve bölüm bilgilerini çekebiliyor!

### 🔗 Kullanılan Kütüphane
- **yokatlas-py**: [saidsurucu/yokatlas-py](https://github.com/saidsurucu/yokatlas-py)
- Python wrapper for YÖK Atlas API

## ✨ Özellikler

### 1. 🏛️ Üniversite Bilgileri
- ✅ Tüm Türkiye'deki üniversiteleri çekme
- ✅ Şehre göre filtreleme
- ✅ Üniversite türü (Devlet/Vakıf)
- ✅ Üniversite detay bilgileri

### 2. 🎓 Bölüm Bilgileri
- ✅ Fakültelere göre gruplandırılmış bölümler
- ✅ Tüm bölümleri arama
- ✅ Fakülte bazlı filtreleme
- ✅ Özel bölüm girişi

### 3. 📍 Şehir Bilgileri
- ✅ Üniversitesi olan şehirler listesi
- ✅ Şehre göre üniversite filtreleme

## 🚀 Kurulum

### Otomatik Kurulum
```bash
pip install -r requirements.txt
```

### Manuel Kurulum
```bash
pip install yokatlas-py
```

## 💻 Kullanım

### Profil Sayfasında

1. **Profil** sayfasına gidin
2. **Şehir Filtresi** ile şehrinizi seçin
3. **Üniversite** listesinden üniversitenizi seçin
4. **Fakülte** seçin (opsiyonel)
5. **Bölüm** seçin

### Kod Örnekleri

```python
from utils.yok_api import YokAPI

# Tüm üniversiteleri getir
universities = YokAPI.get_all_universities()

# Şehre göre filtrele
istanbul_unis = YokAPI.get_universities_by_city("İstanbul")

# Üniversite ara
results = YokAPI.search_universities("Boğaziçi")

# Bölümleri getir
departments = YokAPI.get_all_departments()

# Fakülteye göre bölümler
eng_depts = YokAPI.get_departments_by_faculty("Mühendislik")

# Şehir listesi
cities = YokAPI.get_cities()
```

## 🎯 Avantajlar

### ✅ Gerçek Zamanlı Veri
- YÖK'ün güncel veritabanından çekiliyor
- Manuel güncelleme gerektirmiyor

### ✅ Kapsamlı Liste
- Tüm Türkiye'deki üniversiteler
- Tüm bölümler ve fakülteler

### ✅ Akıllı Filtreleme
- Şehir bazlı filtreleme
- Fakülte bazlı bölüm seçimi
- Arama fonksiyonu

### ✅ Fallback Mekanizması
- API erişilemezse statik veri kullanılır
- Kesintisiz kullanıcı deneyimi

## 📊 Veri Yapısı

### Üniversite
```python
{
    'id': 1,
    'name': 'Boğaziçi Üniversitesi',
    'city': 'İstanbul',
    'type': 'Devlet'
}
```

### Bölümler (Fakültelere Göre)
```python
{
    'Mühendislik': [
        'Bilgisayar Mühendisliği',
        'Elektrik-Elektronik Mühendisliği',
        ...
    ],
    'Fen Bilimleri': [
        'Matematik',
        'Fizik',
        ...
    ]
}
```

## 🔄 Cache Mekanizması

API çağrıları cache'lenir:
- İlk çağrıda API'den çekilir
- Sonraki çağrılarda cache'den okunur
- Performans optimizasyonu

## ⚠️ Hata Yönetimi

### API Erişilemezse
```python
try:
    universities = YokAPI.get_all_universities()
except Exception as e:
    # Fallback to static data
    universities = YokAPI.UNIVERSITIES
```

### Kütüphane Yüklü Değilse
```
⚠️ yokatlas-py not installed. Using static data.
Install with: pip install yokatlas-py
```

## 🎨 Kullanıcı Arayüzü

### Profil Sayfası Özellikleri

1. **Şehir Filtresi**
   - Dropdown menü
   - "Tüm Şehirler" seçeneği
   - Seçilen şehirdeki üniversiteler gösterilir

2. **Üniversite Seçimi**
   - Filtrelenmiş liste
   - Üniversite bilgileri (şehir, tür)
   - "Diğer" seçeneği ile özel giriş

3. **Fakülte Seçimi**
   - Kategorize edilmiş bölümler
   - Opsiyonel seçim

4. **Bölüm Seçimi**
   - Fakülteye göre filtrelenmiş
   - Tüm bölümler listesi
   - Özel bölüm girişi

## 📈 Gelecek Geliştirmeler

- [ ] Üniversite logoları
- [ ] Bölüm kontenjanları
- [ ] Taban puanlar
- [ ] Üniversite sıralamaları
- [ ] Kampüs bilgileri
- [ ] İletişim bilgileri

## 🤝 Katkıda Bulunma

YÖK Atlas API hakkında daha fazla bilgi:
- GitHub: [saidsurucu/yokatlas-py](https://github.com/saidsurucu/yokatlas-py)
- YÖK Atlas: [yokatlas.yok.gov.tr](https://yokatlas.yok.gov.tr)

## 📝 Notlar

- API limitleri yokatlas-py kütüphanesi tarafından yönetilir
- Statik veri fallback olarak her zaman mevcuttur
- Cache mekanizması performansı artırır
- Tüm hatalar gracefully handle edilir

---

**Geliştirici:** DERSLY Team  
**Versiyon:** 2.0  
**Son Güncelleme:** 2025
