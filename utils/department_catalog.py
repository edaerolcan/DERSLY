"""
Department and Course Catalog for DERSLY.
Pre-defined lists of Turkish university departments and common courses.
"""
from typing import List, Dict


class DepartmentCatalog:
    """Catalog of Turkish university departments organized by faculty."""
    
    DEPARTMENTS = {
        "Mühendislik Fakültesi": [
            "Bilgisayar Mühendisliği",
            "Elektrik-Elektronik Mühendisliği",
            "Makine Mühendisliği",
            "Endüstri Mühendisliği",
            "İnşaat Mühendisliği",
            "Yazılım Mühendisliği",
            "Mekatronik Mühendisliği",
            "Kimya Mühendisliği",
            "Çevre Mühendisliği",
            "Gıda Mühendisliği",
            "Biyomedikal Mühendisliği",
            "Harita Mühendisliği",
            "Jeoloji Mühendisliği",
            "Metalurji ve Malzeme Mühendisliği",
            "Petrol ve Doğalgaz Mühendisliği"
        ],
        "Fen Fakültesi": [
            "Matematik",
            "Fizik",
            "Kimya",
            "Biyoloji",
            "İstatistik",
            "Astronomi ve Uzay Bilimleri",
            "Moleküler Biyoloji ve Genetik"
        ],
        "Tıp Fakültesi": [
            "Tıp",
            "Diş Hekimliği",
            "Eczacılık",
            "Hemşirelik",
            "Fizyoterapi ve Rehabilitasyon",
            "Beslenme ve Diyetetik"
        ],
        "İktisadi ve İdari Bilimler Fakültesi": [
            "İşletme",
            "İktisat",
            "Uluslararası İlişkiler",
            "Siyaset Bilimi ve Kamu Yönetimi",
            "Maliye",
            "Ekonometri",
            "İnsan Kaynakları Yönetimi",
            "Lojistik Yönetimi"
        ],
        "Hukuk Fakültesi": [
            "Hukuk"
        ],
        "İletişim Fakültesi": [
            "Gazetecilik",
            "Halkla İlişkiler ve Tanıtım",
            "Radyo, Televizyon ve Sinema",
            "Reklamcılık",
            "Yeni Medya ve İletişim"
        ],
        "Mimarlık Fakültesi": [
            "Mimarlık",
            "İç Mimarlık",
            "Şehir ve Bölge Planlama",
            "Peyzaj Mimarlığı",
            "Endüstri Ürünleri Tasarımı"
        ],
        "Eğitim Fakültesi": [
            "İlköğretim Matematik Öğretmenliği",
            "Türkçe Öğretmenliği",
            "İngilizce Öğretmenliği",
            "Okul Öncesi Öğretmenliği",
            "Rehberlik ve Psikolojik Danışmanlık",
            "Bilgisayar ve Öğretim Teknolojileri Öğretmenliği"
        ],
        "Fen-Edebiyat Fakültesi": [
            "Türk Dili ve Edebiyatı",
            "Tarih",
            "Felsefe",
            "Sosyoloji",
            "Psikoloji",
            "Arkeoloji",
            "Sanat Tarihi",
            "Coğrafya"
        ],
        "Güzel Sanatlar Fakültesi": [
            "Resim",
            "Heykel",
            "Grafik Tasarım",
            "Seramik",
            "Müzik",
            "Sahne Sanatları"
        ]
    }
    
    @staticmethod
    def get_all_departments() -> List[str]:
        """Get flat list of all departments."""
        all_deps = []
        for faculty_deps in DepartmentCatalog.DEPARTMENTS.values():
            all_deps.extend(faculty_deps)
        return sorted(all_deps)
    
    @staticmethod
    def get_departments_by_faculty() -> Dict[str, List[str]]:
        """Get departments organized by faculty."""
        return DepartmentCatalog.DEPARTMENTS
    
    @staticmethod
    def search_departments(query: str) -> List[str]:
        """Search departments by query."""
        query = query.lower()
        all_deps = DepartmentCatalog.get_all_departments()
        return [dep for dep in all_deps if query in dep.lower()]


class CourseCatalog:
    """Catalog of common courses by department."""
    
    COMMON_COURSES = {
        "Bilgisayar Mühendisliği": [
            {"code": "CS101", "name": "Bilgisayar Bilimlerine Giriş", "credits": 3},
            {"code": "CS102", "name": "Programlama Temelleri", "credits": 4},
            {"code": "CS201", "name": "Veri Yapıları", "credits": 4},
            {"code": "CS202", "name": "Algoritmalar", "credits": 4},
            {"code": "CS301", "name": "Veritabanı Sistemleri", "credits": 3},
            {"code": "CS302", "name": "İşletim Sistemleri", "credits": 3},
            {"code": "CS303", "name": "Bilgisayar Ağları", "credits": 3},
            {"code": "CS401", "name": "Yazılım Mühendisliği", "credits": 3},
            {"code": "CS402", "name": "Yapay Zeka", "credits": 3},
            {"code": "MATH101", "name": "Matematik I", "credits": 4},
            {"code": "MATH102", "name": "Matematik II", "credits": 4},
            {"code": "PHYS101", "name": "Fizik I", "credits": 3},
            {"code": "PHYS102", "name": "Fizik II", "credits": 3}
        ],
        "İşletme": [
            {"code": "BUS101", "name": "İşletmeye Giriş", "credits": 3},
            {"code": "BUS102", "name": "Muhasebe İlkeleri", "credits": 3},
            {"code": "BUS201", "name": "Pazarlama Yönetimi", "credits": 3},
            {"code": "BUS202", "name": "Finansal Yönetim", "credits": 3},
            {"code": "BUS301", "name": "İnsan Kaynakları Yönetimi", "credits": 3},
            {"code": "BUS302", "name": "Stratejik Yönetim", "credits": 3},
            {"code": "ECON101", "name": "Mikroekonomi", "credits": 3},
            {"code": "ECON102", "name": "Makroekonomi", "credits": 3},
            {"code": "STAT101", "name": "İstatistik", "credits": 3}
        ],
        "Hukuk": [
            {"code": "LAW101", "name": "Hukuka Giriş", "credits": 3},
            {"code": "LAW102", "name": "Anayasa Hukuku", "credits": 4},
            {"code": "LAW201", "name": "Medeni Hukuk", "credits": 4},
            {"code": "LAW202", "name": "Ceza Hukuku", "credits": 4},
            {"code": "LAW301", "name": "Ticaret Hukuku", "credits": 3},
            {"code": "LAW302", "name": "İdare Hukuku", "credits": 3}
        ],
        # Genel dersler (tüm bölümler için)
        "Genel": [
            {"code": "TURK101", "name": "Türk Dili I", "credits": 2},
            {"code": "TURK102", "name": "Türk Dili II", "credits": 2},
            {"code": "ENG101", "name": "İngilizce I", "credits": 3},
            {"code": "ENG102", "name": "İngilizce II", "credits": 3},
            {"code": "HIST101", "name": "Atatürk İlkeleri ve İnkılap Tarihi I", "credits": 2},
            {"code": "HIST102", "name": "Atatürk İlkeleri ve İnkılap Tarihi II", "credits": 2}
        ]
    }
    
    @staticmethod
    def get_courses_for_department(department: str) -> List[Dict]:
        """Get course suggestions for a department."""
        # Get department-specific courses
        courses = CourseCatalog.COMMON_COURSES.get(department, []).copy()
        # Add general courses
        courses.extend(CourseCatalog.COMMON_COURSES["Genel"])
        return courses
    
    @staticmethod
    def search_courses(query: str, department: str = None) -> List[Dict]:
        """Search courses by query."""
        query = query.lower()
        
        if department:
            courses = CourseCatalog.get_courses_for_department(department)
        else:
            # Search all courses
            courses = []
            for dept_courses in CourseCatalog.COMMON_COURSES.values():
                courses.extend(dept_courses)
        
        return [
            course for course in courses
            if query in course['code'].lower() or query in course['name'].lower()
        ]


class TimeSlotSuggestions:
    """Common time slot suggestions for courses."""
    
    COMMON_SLOTS = [
        {"start": "08:30", "end": "09:20", "duration": 50},
        {"start": "08:30", "end": "10:20", "duration": 110},
        {"start": "09:00", "end": "10:30", "duration": 90},
        {"start": "09:30", "end": "10:20", "duration": 50},
        {"start": "09:30", "end": "11:20", "duration": 110},
        {"start": "10:30", "end": "11:20", "duration": 50},
        {"start": "10:30", "end": "12:20", "duration": 110},
        {"start": "10:40", "end": "12:10", "duration": 90},
        {"start": "11:30", "end": "12:20", "duration": 50},
        {"start": "11:30", "end": "13:20", "duration": 110},
        {"start": "13:00", "end": "14:30", "duration": 90},
        {"start": "13:30", "end": "14:20", "duration": 50},
        {"start": "13:30", "end": "15:20", "duration": 110},
        {"start": "14:30", "end": "15:20", "duration": 50},
        {"start": "14:40", "end": "16:10", "duration": 90},
        {"start": "15:30", "end": "16:20", "duration": 50},
        {"start": "15:30", "end": "17:20", "duration": 110},
        {"start": "16:30", "end": "17:20", "duration": 50},
        {"start": "16:40", "end": "18:10", "duration": 90}
    ]
    
    @staticmethod
    def get_end_time_suggestions(start_time: str) -> List[str]:
        """Get end time suggestions based on start time."""
        suggestions = []
        for slot in TimeSlotSuggestions.COMMON_SLOTS:
            if slot['start'] == start_time:
                suggestions.append(slot['end'])
        return suggestions if suggestions else [start_time]  # Return start time if no match
