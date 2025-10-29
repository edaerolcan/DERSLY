# Design Document: Browser Storage Migration

## Overview

Bu tasarım, DERSLY uygulamasını veritabanı tabanlı depolamadan tarayıcı tabanlı (client-side) depolamaya geçirmeyi amaçlamaktadır. Streamlit'in `session_state` mekanizması kullanılarak veriler tarayıcı oturumunda saklanacak ve kullanıcılara JSON formatında veri dışa/içe aktarma imkanı sunulacaktır.

### Design Goals

1. **Basitlik**: Veritabanı bağımlılığını tamamen kaldırarak deployment'ı basitleştirmek
2. **Taşınabilirlik**: Kullanıcıların verilerini farklı cihazlar/tarayıcılar arasında taşıyabilmesi
3. **Yedekleme**: Kullanıcıların verilerini yerel olarak yedekleyebilmesi
4. **Performans**: Veritabanı sorguları yerine bellek içi işlemlerle daha hızlı erişim
5. **Gizlilik**: Veriler kullanıcının cihazında kalır, merkezi sunucuda saklanmaz

### Trade-offs

**Avantajlar:**
- Veritabanı kurulumu/yönetimi gerektirmez
- Streamlit Cloud'da kolay deployment
- Daha hızlı veri erişimi (bellek içi)
- Kullanıcı gizliliği (veriler yerel)
- Maliyet tasarrufu (veritabanı hosting gerekmez)

**Dezavantajlar:**
- Tarayıcı kapatıldığında veriler kaybolur (export/import ile çözülür)
- Farklı cihazlar arasında otomatik senkronizasyon yok
- Tarayıcı depolama limitleri (genellikle 5-10MB, yeterli olacaktır)
- Çoklu kullanıcı desteği yok (her kullanıcı kendi tarayıcısında)

## Architecture

### Current Architecture (Database-Based)

```
┌─────────────┐
│  Streamlit  │
│     App     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   SQLAlchemy│
│     ORM     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   MySQL/    │
│   TiDB      │
└─────────────┘
```

### New Architecture (Browser Storage)

```
┌─────────────────────────────────────┐
│         Streamlit App               │
│  ┌─────────────────────────────┐   │
│  │   Session State Storage     │   │
│  │  (In-Memory Data Store)     │   │
│  └─────────────────────────────┘   │
│              ▲  │                   │
│              │  │                   │
│              │  ▼                   │
│  ┌─────────────────────────────┐   │
│  │   Storage Manager           │   │
│  │  - Initialize               │   │
│  │  - CRUD Operations          │   │
│  │  - Export/Import            │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
         │                    ▲
         │ Export             │ Import
         ▼                    │
    ┌─────────────────────────────┐
    │   User's Local File System  │
    │   (JSON Backup Files)       │
    └─────────────────────────────┘
```

## Components and Interfaces

### 1. Storage Manager (`utils/storage_manager.py`)

Tüm veri yönetimi işlemlerini merkezi olarak yöneten ana modül.

```python
class StorageManager:
    """
    Manages all data storage operations using Streamlit session state.
    Provides CRUD operations and export/import functionality.
    """
    
    @staticmethod
    def initialize_storage() -> None:
        """Initialize empty data structures in session state if not exists."""
        
    @staticmethod
    def export_data() -> dict:
        """Export all data as a dictionary for JSON serialization."""
        
    @staticmethod
    def import_data(data: dict) -> bool:
        """Import data from dictionary and update session state."""
        
    @staticmethod
    def clear_all_data() -> None:
        """Clear all data from session state."""
        
    @staticmethod
    def get_storage_info() -> dict:
        """Get storage usage information."""
```

### 2. User Manager (`utils/user_manager.py`)

Kullanıcı kimlik doğrulama ve profil yönetimi (basitleştirilmiş).

```python
class UserManager:
    """
    Simplified user management without database.
    Stores single user profile in session state.
    """
    
    @staticmethod
    def create_profile(name: str, email: str, **kwargs) -> dict:
        """Create user profile in session state."""
        
    @staticmethod
    def get_profile() -> Optional[dict]:
        """Get current user profile from session state."""
        
    @staticmethod
    def update_profile(updates: dict) -> bool:
        """Update user profile."""
        
    @staticmethod
    def is_profile_exists() -> bool:
        """Check if user profile exists."""
```

### 3. Course Manager (`utils/course_manager.py`)

Ders yönetimi işlemleri.

```python
class CourseManager:
    """
    Manages course data in session state.
    """
    
    @staticmethod
    def add_course(course_data: dict) -> int:
        """Add new course and return ID."""
        
    @staticmethod
    def get_course(course_id: int) -> Optional[dict]:
        """Get course by ID."""
        
    @staticmethod
    def get_all_courses() -> List[dict]:
        """Get all courses."""
        
    @staticmethod
    def update_course(course_id: int, updates: dict) -> bool:
        """Update course."""
        
    @staticmethod
    def delete_course(course_id: int) -> bool:
        """Delete course."""
        
    @staticmethod
    def get_courses_by_day(day: str) -> List[dict]:
        """Get courses for specific day."""
```

### 4. Assignment Manager (`utils/assignment_manager.py`)

Ödev/sınav yönetimi işlemleri.

```python
class AssignmentManager:
    """
    Manages assignment data in session state.
    """
    
    @staticmethod
    def add_assignment(assignment_data: dict) -> int:
        """Add new assignment and return ID."""
        
    @staticmethod
    def get_assignment(assignment_id: int) -> Optional[dict]:
        """Get assignment by ID."""
        
    @staticmethod
    def get_all_assignments() -> List[dict]:
        """Get all assignments."""
        
    @staticmethod
    def update_assignment(assignment_id: int, updates: dict) -> bool:
        """Update assignment."""
        
    @staticmethod
    def delete_assignment(assignment_id: int) -> bool:
        """Delete assignment."""
        
    @staticmethod
    def get_assignments_by_status(status: str) -> List[dict]:
        """Get assignments by status."""
        
    @staticmethod
    def get_upcoming_assignments(days: int = 7) -> List[dict]:
        """Get assignments due in next N days."""
```

### 5. Grade Manager (`utils/grade_manager.py`)

Not yönetimi ve GPA hesaplama işlemleri.

```python
class GradeManager:
    """
    Manages grade entries and GPA calculations.
    """
    
    @staticmethod
    def add_grade(grade_data: dict) -> int:
        """Add new grade entry and return ID."""
        
    @staticmethod
    def get_all_grades() -> List[dict]:
        """Get all grade entries."""
        
    @staticmethod
    def update_grade(grade_id: int, updates: dict) -> bool:
        """Update grade entry."""
        
    @staticmethod
    def delete_grade(grade_id: int) -> bool:
        """Delete grade entry."""
        
    @staticmethod
    def calculate_gpa() -> float:
        """Calculate overall GPA."""
        
    @staticmethod
    def calculate_semester_gpa(semester: str, year: int) -> float:
        """Calculate GPA for specific semester."""
        
    @staticmethod
    def get_grades_by_semester(semester: str, year: int) -> List[dict]:
        """Get grades for specific semester."""
```

### 6. Export/Import UI Component (`utils/export_import_ui.py`)

Kullanıcı arayüzü için export/import bileşenleri.

```python
def show_export_button() -> None:
    """Display export button and handle export operation."""
    
def show_import_button() -> None:
    """Display import button and handle import operation."""
    
def show_clear_data_button() -> None:
    """Display clear data button with confirmation."""
    
def show_storage_info() -> None:
    """Display storage usage information."""
```

## Data Models

### Session State Structure

```python
st.session_state = {
    # User Profile (replaces User table)
    'user_profile': {
        'name': str,
        'email': str,
        'student_id': Optional[str],
        'department': Optional[str],
        'class_year': Optional[int],
        'created_at': str  # ISO format datetime
    },
    
    # Courses (replaces Course table)
    'courses': {
        1: {
            'id': int,
            'course_name': str,
            'course_code': str,
            'day': str,
            'start_time': str,  # HH:MM format
            'end_time': str,
            'color': str,
            'credits': int,
            'created_at': str
        },
        # ... more courses
    },
    
    # Assignments (replaces Assignment table)
    'assignments': {
        1: {
            'id': int,
            'course_id': Optional[int],
            'title': str,
            'description': Optional[str],
            'type': str,  # assignment, exam, project, quiz
            'due_date': str,  # ISO format datetime
            'status': str,  # pending, completed
            'priority': str,  # low, medium, high
            'created_at': str
        },
        # ... more assignments
    },
    
    # Grade Entries (replaces GradeEntry table)
    'grades': {
        1: {
            'id': int,
            'course_name': str,
            'grade': float,
            'credits': int,
            'semester': str,
            'year': int,
            'created_at': str
        },
        # ... more grades
    },
    
    # Reminders (replaces Reminder table)
    'reminders': {
        1: {
            'id': int,
            'assignment_id': Optional[int],
            'reminder_date': str,
            'reminder_type': str,
            'is_sent': bool,
            'is_active': bool,
            'created_at': str
        },
        # ... more reminders
    },
    
    # Metadata
    'metadata': {
        'version': str,  # Data format version
        'last_export': Optional[str],  # Last export timestamp
        'last_import': Optional[str],  # Last import timestamp
    },
    
    # Auto-increment counters for IDs
    'next_course_id': int,
    'next_assignment_id': int,
    'next_grade_id': int,
    'next_reminder_id': int,
}
```

### Export JSON Format

```json
{
  "version": "1.0.0",
  "exported_at": "2025-10-29T10:30:00Z",
  "user_profile": {
    "name": "Ahmet Yılmaz",
    "email": "ahmet@universite.edu.tr",
    "student_id": "2020123456",
    "department": "Bilgisayar Mühendisliği",
    "class_year": 3
  },
  "courses": [
    {
      "id": 1,
      "course_name": "Veri Yapıları",
      "course_code": "CS201",
      "day": "Monday",
      "start_time": "09:00",
      "end_time": "11:00",
      "color": "#FF5733",
      "credits": 4
    }
  ],
  "assignments": [
    {
      "id": 1,
      "course_id": 1,
      "title": "Ödev 1",
      "description": "Binary tree implementasyonu",
      "type": "assignment",
      "due_date": "2025-11-05T23:59:00Z",
      "status": "pending",
      "priority": "high"
    }
  ],
  "grades": [
    {
      "id": 1,
      "course_name": "Algoritma Analizi",
      "grade": 3.5,
      "credits": 4,
      "semester": "Fall",
      "year": 2024
    }
  ],
  "reminders": []
}
```

## Migration Strategy

### Phase 1: Create New Storage Layer

1. `StorageManager` sınıfını oluştur
2. Veri yapılarını session state'te initialize et
3. Temel CRUD operasyonlarını implement et

### Phase 2: Create Manager Classes

1. `UserManager` - Kullanıcı profil yönetimi
2. `CourseManager` - Ders yönetimi
3. `AssignmentManager` - Ödev yönetimi
4. `GradeManager` - Not yönetimi

### Phase 3: Implement Export/Import

1. JSON export fonksiyonalitesi
2. JSON import ve validasyon
3. UI bileşenleri (butonlar, file uploader)
4. Hata yönetimi ve kullanıcı geri bildirimleri

### Phase 4: Update Application Pages

1. `app.py` - Authentication'ı basitleştir
2. `pages/1_🏠_Home.py` - Yeni manager'ları kullan
3. `pages/2_📚_Courses.py` - CourseManager'a geç
4. `pages/3_📝_Assignments.py` - AssignmentManager'a geç
5. `pages/6_📊_GPA.py` - GradeManager'a geç
6. `pages/7_👤_Profile.py` - UserManager ve export/import UI ekle

### Phase 5: Remove Database Dependencies

1. `database/` klasörünü sil
2. `config.py`'den database ayarlarını kaldır
3. `requirements.txt`'den SQLAlchemy ve ilgili paketleri kaldır
4. `.env` dosyasını temizle

## Error Handling

### Storage Errors

```python
class StorageError(Exception):
    """Base exception for storage operations."""
    pass

class StorageQuotaExceeded(StorageError):
    """Raised when storage quota is exceeded."""
    pass

class InvalidDataFormat(StorageError):
    """Raised when imported data format is invalid."""
    pass

class DataCorrupted(StorageError):
    """Raised when data is corrupted."""
    pass
```

### Error Handling Strategy

1. **Graceful Degradation**: Hata durumunda uygulama çökmemeli
2. **User Feedback**: Kullanıcıya anlaşılır hata mesajları
3. **Data Validation**: Import sırasında veri doğrulama
4. **Backup Suggestion**: Hata durumunda export önerisi
5. **Logging**: Hataları log'la (debugging için)

## Testing Strategy

### Unit Tests

```python
# tests/test_storage_manager.py
def test_initialize_storage()
def test_export_data()
def test_import_data()
def test_clear_all_data()

# tests/test_course_manager.py
def test_add_course()
def test_get_course()
def test_update_course()
def test_delete_course()

# tests/test_assignment_manager.py
def test_add_assignment()
def test_get_upcoming_assignments()
def test_update_assignment_status()

# tests/test_grade_manager.py
def test_calculate_gpa()
def test_calculate_semester_gpa()
```

### Integration Tests

```python
# tests/test_export_import.py
def test_export_import_roundtrip()
def test_import_with_existing_data()
def test_import_invalid_format()

# tests/test_data_persistence.py
def test_data_persists_across_reruns()
def test_data_cleared_on_clear_all()
```

### Manual Testing Checklist

- [ ] Yeni profil oluşturma
- [ ] Ders ekleme, düzenleme, silme
- [ ] Ödev ekleme, düzenleme, silme
- [ ] Not ekleme ve GPA hesaplama
- [ ] Veri export etme
- [ ] Veri import etme
- [ ] Mevcut veri üzerine import uyarısı
- [ ] Tüm verileri temizleme
- [ ] Tarayıcı yenileme sonrası veri kaybı (beklenen davranış)
- [ ] Farklı tarayıcıda import

## Security Considerations

### Data Privacy

1. **Local Storage**: Veriler sadece kullanıcının tarayıcısında
2. **No Server Storage**: Merkezi sunucuda veri saklanmaz
3. **Export Encryption**: (Opsiyonel) Export dosyalarını şifreleyebiliriz
4. **No Authentication**: Basitleştirilmiş model, şifre yok

### Input Validation

1. **JSON Schema Validation**: Import edilen verileri validate et
2. **Type Checking**: Veri tiplerini kontrol et
3. **Sanitization**: XSS ve injection saldırılarına karşı koruma
4. **Size Limits**: Import dosya boyutu limiti

## Performance Considerations

### Memory Usage

- Session state bellek içi çalışır
- Ortalama kullanıcı verisi: ~1-5MB
- Streamlit session state limiti: Yeterli (10MB+)

### Optimization Strategies

1. **Lazy Loading**: Sadece gerekli verileri yükle
2. **Caching**: `@st.cache_data` kullan
3. **Efficient Data Structures**: Dict kullanımı (O(1) lookup)
4. **Minimal Reruns**: Session state değişikliklerini minimize et

## Deployment Considerations

### Streamlit Cloud

1. **No Database Setup**: Veritabanı konfigürasyonu gerektirmez
2. **Secrets**: Artık veritabanı secrets'ı gerekmez
3. **Dependencies**: Daha az dependency (SQLAlchemy yok)
4. **Faster Deployment**: Daha hızlı build ve deploy

### User Experience

1. **First-Time Users**: Boş state ile başlar
2. **Returning Users**: Export/import ile veri taşır
3. **Data Loss Warning**: Tarayıcı temizlenirse veri kaybolur
4. **Regular Exports**: Kullanıcıları düzenli export yapmaya teşvik et

## Future Enhancements

### Potential Improvements

1. **Browser LocalStorage**: Session state yerine localStorage kullanımı (kalıcı)
2. **Auto-Export**: Periyodik otomatik export
3. **Cloud Sync**: (Opsiyonel) Google Drive, Dropbox entegrasyonu
4. **Data Encryption**: Export dosyalarını şifreleme
5. **Version Control**: Veri versiyonlama ve geri alma
6. **Multi-Device Sync**: QR kod ile cihazlar arası transfer

### LocalStorage Implementation (Future)

```python
# Streamlit components ile custom JavaScript
import streamlit.components.v1 as components

def save_to_localstorage(key: str, value: str):
    """Save data to browser localStorage."""
    components.html(f"""
        <script>
        localStorage.setItem('{key}', '{value}');
        </script>
    """, height=0)

def load_from_localstorage(key: str) -> str:
    """Load data from browser localStorage."""
    # Implementation using custom component
    pass
```

## Conclusion

Bu tasarım, DERSLY uygulamasını veritabanı bağımlılığından kurtararak daha basit, taşınabilir ve deployment-friendly bir yapıya dönüştürecektir. Kullanıcılar verilerini kendi cihazlarında saklayacak ve istedikleri zaman yedekleyip geri yükleyebileceklerdir.

Tasarım, mevcut tüm özellikleri korurken (dersler, ödevler, notlar, GPA hesaplama) altyapıyı tamamen değiştirecektir. Migration stratejisi aşamalı olarak uygulanabilir ve her aşama test edilebilir.
