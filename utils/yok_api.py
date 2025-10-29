"""
YÖK (Yükseköğretim Kurulu) API integration for DERSLY.
Fetches university and department information from YÖK Atlas.
Uses yokatlas-py library: https://github.com/saidsurucu/yokatlas-py
"""
from typing import List, Dict, Optional
import json

try:
    from yokatlas import YokAtlas
    YOKATLAS_AVAILABLE = True
except ImportError:
    YOKATLAS_AVAILABLE = False
    print("⚠️ yokatlas-py not installed. Using static data. Install with: pip install yokatlas-py")


class YokAPI:
    """
    YÖK API integration for fetching university and department data.
    Uses YÖK Atlas API when available, falls back to static data.
    """
    
    _yokatlas = None
    _cache = {
        'universities': None,
        'departments': None
    }
    
    @staticmethod
    def _get_yokatlas():
        """Get or create YokAtlas instance."""
        if YokAPI._yokatlas is None and YOKATLAS_AVAILABLE:
            try:
                YokAPI._yokatlas = YokAtlas()
            except Exception as e:
                print(f"⚠️ Could not initialize YokAtlas: {e}")
        return YokAPI._yokatlas
    
    # Static data - Turkish universities (most common ones)
    # In a real implementation, this could be fetched from YÖK's public API
    UNIVERSITIES = [
        {"id": 1, "name": "Bahçeşehir Üniversitesi", "city": "İstanbul", "type": "Vakıf"},
        {"id": 2, "name": "Boğaziçi Üniversitesi", "city": "İstanbul", "type": "Devlet"},
        {"id": 3, "name": "İstanbul Teknik Üniversitesi", "city": "İstanbul", "type": "Devlet"},
        {"id": 4, "name": "Orta Doğu Teknik Üniversitesi", "city": "Ankara", "type": "Devlet"},
        {"id": 5, "name": "Koç Üniversitesi", "city": "İstanbul", "type": "Vakıf"},
        {"id": 6, "name": "Sabancı Üniversitesi", "city": "İstanbul", "type": "Vakıf"},
        {"id": 7, "name": "Bilkent Üniversitesi", "city": "Ankara", "type": "Vakıf"},
        {"id": 8, "name": "Hacettepe Üniversitesi", "city": "Ankara", "type": "Devlet"},
        {"id": 9, "name": "Ankara Üniversitesi", "city": "Ankara", "type": "Devlet"},
        {"id": 10, "name": "İstanbul Üniversitesi", "city": "İstanbul", "type": "Devlet"},
        {"id": 11, "name": "Ege Üniversitesi", "city": "İzmir", "type": "Devlet"},
        {"id": 12, "name": "Yeditepe Üniversitesi", "city": "İstanbul", "type": "Vakıf"},
        {"id": 13, "name": "Özyeğin Üniversitesi", "city": "İstanbul", "type": "Vakıf"},
        {"id": 14, "name": "Marmara Üniversitesi", "city": "İstanbul", "type": "Devlet"},
        {"id": 15, "name": "Galatasaray Üniversitesi", "city": "İstanbul", "type": "Devlet"},
        {"id": 16, "name": "Dokuz Eylül Üniversitesi", "city": "İzmir", "type": "Devlet"},
        {"id": 17, "name": "Gazi Üniversitesi", "city": "Ankara", "type": "Devlet"},
        {"id": 18, "name": "Anadolu Üniversitesi", "city": "Eskişehir", "type": "Devlet"},
        {"id": 19, "name": "Çukurova Üniversitesi", "city": "Adana", "type": "Devlet"},
        {"id": 20, "name": "Erciyes Üniversitesi", "city": "Kayseri", "type": "Devlet"},
    ]
    
    # Common departments
    DEPARTMENTS = {
        "Mühendislik": [
            "Bilgisayar Mühendisliği",
            "Elektrik-Elektronik Mühendisliği",
            "Makine Mühendisliği",
            "Endüstri Mühendisliği",
            "İnşaat Mühendisliği",
            "Yazılım Mühendisliği",
            "Mekatronik Mühendisliği",
            "Biyomedikal Mühendisliği",
            "Çevre Mühendisliği",
            "Kimya Mühendisliği"
        ],
        "Fen Bilimleri": [
            "Matematik",
            "Fizik",
            "Kimya",
            "Biyoloji",
            "İstatistik",
            "Moleküler Biyoloji ve Genetik"
        ],
        "Sosyal Bilimler": [
            "İşletme",
            "İktisat",
            "Psikoloji",
            "Sosyoloji",
            "Uluslararası İlişkiler",
            "Siyaset Bilimi",
            "Halkla İlişkiler",
            "Reklamcılık"
        ],
        "Tıp": [
            "Tıp",
            "Diş Hekimliği",
            "Eczacılık",
            "Hemşirelik",
            "Fizyoterapi ve Rehabilitasyon"
        ],
        "Hukuk": [
            "Hukuk"
        ],
        "İletişim": [
            "Gazetecilik",
            "Radyo, Televizyon ve Sinema",
            "Yeni Medya",
            "Halkla İlişkiler ve Tanıtım"
        ],
        "Mimarlık": [
            "Mimarlık",
            "İç Mimarlık",
            "Şehir ve Bölge Planlama",
            "Peyzaj Mimarlığı"
        ],
        "Eğitim": [
            "İlköğretim Matematik Öğretmenliği",
            "İngilizce Öğretmenliği",
            "Bilgisayar ve Öğretim Teknolojileri Öğretmenliği",
            "Okul Öncesi Öğretmenliği",
            "Rehberlik ve Psikolojik Danışmanlık"
        ]
    }
    
    @staticmethod
    def get_all_universities() -> List[Dict[str, any]]:
        """
        Get list of all universities.
        Tries to fetch from YÖK Atlas API, falls back to static data.
        
        Returns:
            List of university dictionaries with id, name, city, type
        """
        # Try to use cached data first
        if YokAPI._cache['universities'] is not None:
            return YokAPI._cache['universities']
        
        # Try to fetch from YÖK Atlas
        yokatlas = YokAPI._get_yokatlas()
        if yokatlas:
            try:
                # Fetch universities from API
                unis = yokatlas.get_universities()
                if unis:
                    # Convert to our format
                    result = []
                    for i, uni in enumerate(unis[:50]):  # Limit to 50 for performance
                        result.append({
                            'id': i + 1,
                            'name': uni.get('name', ''),
                            'city': uni.get('city', 'Bilinmiyor'),
                            'type': uni.get('type', 'Bilinmiyor')
                        })
                    YokAPI._cache['universities'] = result
                    return result
            except Exception as e:
                print(f"⚠️ Could not fetch from YÖK Atlas: {e}")
        
        # Fallback to static data
        return YokAPI.UNIVERSITIES
    
    @staticmethod
    def search_universities(query: str) -> List[Dict[str, any]]:
        """
        Search universities by name.
        
        Args:
            query: Search query
            
        Returns:
            List of matching universities
        """
        query_lower = query.lower()
        return [
            uni for uni in YokAPI.UNIVERSITIES
            if query_lower in uni['name'].lower()
        ]
    
    @staticmethod
    def get_university_by_name(name: str) -> Optional[Dict[str, any]]:
        """
        Get university by exact name.
        
        Args:
            name: University name
            
        Returns:
            University dictionary or None
        """
        for uni in YokAPI.UNIVERSITIES:
            if uni['name'] == name:
                return uni
        return None
    
    @staticmethod
    def get_all_departments() -> Dict[str, List[str]]:
        """
        Get all departments grouped by faculty.
        
        Returns:
            Dictionary of faculty -> departments
        """
        return YokAPI.DEPARTMENTS
    
    @staticmethod
    def get_departments_by_faculty(faculty: str) -> List[str]:
        """
        Get departments for a specific faculty.
        
        Args:
            faculty: Faculty name
            
        Returns:
            List of department names
        """
        return YokAPI.DEPARTMENTS.get(faculty, [])
    
    @staticmethod
    def get_all_departments_flat() -> List[str]:
        """
        Get all departments as a flat list.
        
        Returns:
            List of all department names
        """
        all_deps = []
        for deps in YokAPI.DEPARTMENTS.values():
            all_deps.extend(deps)
        return sorted(all_deps)
    
    @staticmethod
    def search_departments(query: str) -> List[str]:
        """
        Search departments by name.
        
        Args:
            query: Search query
            
        Returns:
            List of matching department names
        """
        query_lower = query.lower()
        all_deps = YokAPI.get_all_departments_flat()
        return [
            dep for dep in all_deps
            if query_lower in dep.lower()
        ]
    
    @staticmethod
    def get_university_info(university_name: str) -> Dict[str, any]:
        """
        Get detailed information about a university.
        
        Args:
            university_name: Name of the university
            
        Returns:
            Dictionary with university information
        """
        uni = YokAPI.get_university_by_name(university_name)
        if uni:
            return {
                "name": uni['name'],
                "city": uni['city'],
                "type": uni['type'],
                "available_faculties": list(YokAPI.DEPARTMENTS.keys())
            }
        return {}
    
    @staticmethod
    def get_cities() -> List[str]:
        """
        Get list of cities with universities.
        
        Returns:
            Sorted list of city names
        """
        cities = set(uni['city'] for uni in YokAPI.UNIVERSITIES)
        return sorted(cities)
    
    @staticmethod
    def get_universities_by_city(city: str) -> List[Dict[str, any]]:
        """
        Get universities in a specific city.
        
        Args:
            city: City name
            
        Returns:
            List of universities in that city
        """
        return [
            uni for uni in YokAPI.UNIVERSITIES
            if uni['city'] == city
        ]
    
    @staticmethod
    def get_universities_by_type(uni_type: str) -> List[Dict[str, any]]:
        """
        Get universities by type (Devlet/Vakıf).
        
        Args:
            uni_type: "Devlet" or "Vakıf"
            
        Returns:
            List of universities of that type
        """
        return [
            uni for uni in YokAPI.UNIVERSITIES
            if uni['type'] == uni_type
        ]
