"""
Input validation utilities for DERSLY Streamlit application.
Provides validation functions for forms and user inputs.
"""
from typing import Tuple, Optional
from datetime import datetime, time
import re
import logging

logger = logging.getLogger(__name__)


class Validator:
    """
    Validator class providing validation methods for various input types.
    """
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """
        Validate email address format.
        
        Args:
            email: Email address to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not email:
            return False, "📧 E-posta adresi gereklidir"
        
        email = email.strip()
        
        # Basic email regex pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(pattern, email):
            return False, "📧 Geçerli bir e-posta adresi girin (örn: kullanici@universite.edu.tr)"
        
        # Check for common typos
        if '..' in email or email.startswith('.') or email.endswith('.'):
            return False, "📧 E-posta adresinde geçersiz nokta kullanımı"
        
        return True, "✅ Geçerli e-posta adresi"
    
    @staticmethod
    def validate_password(password: str, min_length: int = 6) -> Tuple[bool, str]:
        """
        Validate password strength.
        
        Args:
            password: Password to validate
            min_length: Minimum password length
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not password:
            return False, "🔒 Şifre gereklidir"
        
        if len(password) < min_length:
            return False, f"🔒 Şifre en az {min_length} karakter olmalıdır (şu an: {len(password)})"
        
        # Check for common weak passwords
        weak_passwords = ['123456', 'password', '12345678', 'qwerty', 'abc123', '111111']
        if password.lower() in weak_passwords:
            return False, "🔒 Bu şifre çok yaygın kullanılıyor. Daha güçlü bir şifre seçin"
        
        # Strength recommendations
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        
        if len(password) >= 8 and has_upper and has_lower and has_digit:
            return True, "✅ Güçlü şifre"
        elif len(password) >= min_length:
            return True, "⚠️ Şifre kabul edilebilir (daha güçlü olabilir)"
        
        return True, ""
    
    @staticmethod
    def validate_course_data(course_data: dict) -> Tuple[bool, str]:
        """
        Validate course data.
        
        Args:
            course_data: Dictionary containing course information
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Required fields
        required_fields = ['course_name', 'course_code', 'day', 'start_time', 'end_time']
        
        for field in required_fields:
            if field not in course_data or not course_data[field]:
                field_names = {
                    'course_name': 'Ders adı',
                    'course_code': 'Ders kodu',
                    'day': 'Gün',
                    'start_time': 'Başlangıç saati',
                    'end_time': 'Bitiş saati'
                }
                return False, f"{field_names.get(field, field)} gereklidir"
        
        # Validate course name length
        if len(course_data['course_name']) < 2:
            return False, "Ders adı en az 2 karakter olmalıdır"
        
        if len(course_data['course_name']) > 200:
            return False, "Ders adı en fazla 200 karakter olabilir"
        
        # Validate course code length
        if len(course_data['course_code']) < 2:
            return False, "Ders kodu en az 2 karakter olmalıdır"
        
        if len(course_data['course_code']) > 50:
            return False, "Ders kodu en fazla 50 karakter olabilir"
        
        # Validate day
        valid_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday',
                     'Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
        if course_data['day'] not in valid_days:
            return False, "Geçerli bir gün seçin"
        
        # Validate time order
        if isinstance(course_data['start_time'], time) and isinstance(course_data['end_time'], time):
            if course_data['start_time'] >= course_data['end_time']:
                return False, "Bitiş saati başlangıç saatinden sonra olmalıdır"
        
        # Validate credits if provided
        if 'credits' in course_data and course_data['credits'] is not None:
            if not isinstance(course_data['credits'], int) or course_data['credits'] < 0 or course_data['credits'] > 20:
                return False, "Kredi 0 ile 20 arasında olmalıdır"
        
        # Validate color if provided
        if 'color' in course_data and course_data['color']:
            if not re.match(r'^#[0-9A-Fa-f]{6}$', course_data['color']):
                return False, "Geçerli bir renk kodu girin (örn: #FF5733)"
        
        return True, ""
    
    @staticmethod
    def validate_assignment_data(assignment_data: dict) -> Tuple[bool, str]:
        """
        Validate assignment data.
        
        Args:
            assignment_data: Dictionary containing assignment information
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Required fields
        required_fields = ['title', 'type', 'due_date']
        
        for field in required_fields:
            if field not in assignment_data or not assignment_data[field]:
                field_names = {
                    'title': 'Başlık',
                    'type': 'Tür',
                    'due_date': 'Son teslim tarihi'
                }
                return False, f"{field_names.get(field, field)} gereklidir"
        
        # Validate title length
        if len(assignment_data['title']) < 2:
            return False, "Başlık en az 2 karakter olmalıdır"
        
        if len(assignment_data['title']) > 200:
            return False, "Başlık en fazla 200 karakter olabilir"
        
        # Validate type
        valid_types = ['assignment', 'exam', 'project', 'quiz']
        if assignment_data['type'] not in valid_types:
            return False, "Geçerli bir tür seçin (ödev, sınav, proje, quiz)"
        
        # Validate due date
        if isinstance(assignment_data['due_date'], datetime):
            if assignment_data['due_date'] < datetime.now():
                return False, "Son teslim tarihi geçmiş bir tarih olamaz"
        
        # Validate status if provided
        if 'status' in assignment_data and assignment_data['status']:
            valid_statuses = ['pending', 'completed']
            if assignment_data['status'] not in valid_statuses:
                return False, "Geçerli bir durum seçin (beklemede, tamamlandı)"
        
        # Validate priority if provided
        if 'priority' in assignment_data and assignment_data['priority']:
            valid_priorities = ['low', 'medium', 'high']
            if assignment_data['priority'] not in valid_priorities:
                return False, "Geçerli bir öncelik seçin (düşük, orta, yüksek)"
        
        # Validate description length if provided
        if 'description' in assignment_data and assignment_data['description']:
            if len(assignment_data['description']) > 5000:
                return False, "Açıklama en fazla 5000 karakter olabilir"
        
        return True, ""
    
    @staticmethod
    def validate_grade_data(grade_data: dict) -> Tuple[bool, str]:
        """
        Validate grade entry data.
        
        Args:
            grade_data: Dictionary containing grade information
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Required fields
        required_fields = ['course_name', 'grade', 'credits', 'semester', 'year']
        
        for field in required_fields:
            if field not in grade_data or grade_data[field] is None:
                field_names = {
                    'course_name': 'Ders adı',
                    'grade': 'Not',
                    'credits': 'Kredi',
                    'semester': 'Dönem',
                    'year': 'Yıl'
                }
                return False, f"{field_names.get(field, field)} gereklidir"
        
        # Validate course name length
        if len(grade_data['course_name']) < 2:
            return False, "Ders adı en az 2 karakter olmalıdır"
        
        if len(grade_data['course_name']) > 200:
            return False, "Ders adı en fazla 200 karakter olabilir"
        
        # Validate grade value (0.0 to 4.0)
        try:
            grade = float(grade_data['grade'])
            if grade < 0.0 or grade > 4.0:
                return False, "Not 0.0 ile 4.0 arasında olmalıdır"
        except (ValueError, TypeError):
            return False, "Geçerli bir not değeri girin"
        
        # Validate credits
        try:
            credits = int(grade_data['credits'])
            if credits < 0 or credits > 20:
                return False, "Kredi 0 ile 20 arasında olmalıdır"
        except (ValueError, TypeError):
            return False, "Geçerli bir kredi değeri girin"
        
        # Validate semester
        if len(grade_data['semester']) < 2:
            return False, "Dönem bilgisi gereklidir"
        
        # Validate year
        try:
            year = int(grade_data['year'])
            current_year = datetime.now().year
            if year < 1900 or year > current_year + 10:
                return False, f"Yıl 1900 ile {current_year + 10} arasında olmalıdır"
        except (ValueError, TypeError):
            return False, "Geçerli bir yıl değeri girin"
        
        return True, ""
    
    @staticmethod
    def validate_reminder_data(reminder_data: dict) -> Tuple[bool, str]:
        """
        Validate reminder data.
        
        Args:
            reminder_data: Dictionary containing reminder information
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Required fields
        required_fields = ['reminder_date', 'reminder_type']
        
        for field in required_fields:
            if field not in reminder_data or not reminder_data[field]:
                field_names = {
                    'reminder_date': 'Hatırlatma tarihi',
                    'reminder_type': 'Hatırlatma türü'
                }
                return False, f"{field_names.get(field, field)} gereklidir"
        
        # Validate reminder date
        if isinstance(reminder_data['reminder_date'], datetime):
            if reminder_data['reminder_date'] < datetime.now():
                return False, "Hatırlatma tarihi geçmiş bir tarih olamaz"
        
        # Validate reminder type
        valid_types = ['notification', 'email', 'push']
        if reminder_data['reminder_type'] not in valid_types:
            return False, "Geçerli bir hatırlatma türü seçin"
        
        return True, ""
    
    @staticmethod
    def validate_user_profile_data(profile_data: dict) -> Tuple[bool, str]:
        """
        Validate user profile data.
        
        Args:
            profile_data: Dictionary containing profile information
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate name if provided
        if 'name' in profile_data and profile_data['name']:
            if len(profile_data['name']) < 2:
                return False, "Ad Soyad en az 2 karakter olmalıdır"
            if len(profile_data['name']) > 100:
                return False, "Ad Soyad en fazla 100 karakter olabilir"
        
        # Validate email if provided
        if 'email' in profile_data and profile_data['email']:
            is_valid, error_msg = Validator.validate_email(profile_data['email'])
            if not is_valid:
                return False, error_msg
        
        # Validate student_id if provided
        if 'student_id' in profile_data and profile_data['student_id']:
            if len(profile_data['student_id']) > 50:
                return False, "Öğrenci numarası en fazla 50 karakter olabilir"
        
        # Validate department if provided
        if 'department' in profile_data and profile_data['department']:
            if len(profile_data['department']) > 100:
                return False, "Bölüm adı en fazla 100 karakter olabilir"
        
        # Validate class_year if provided
        if 'class_year' in profile_data and profile_data['class_year'] is not None:
            try:
                class_year = int(profile_data['class_year'])
                if class_year < 1 or class_year > 10:
                    return False, "Sınıf 1 ile 10 arasında olmalıdır"
            except (ValueError, TypeError):
                return False, "Geçerli bir sınıf değeri girin"
        
        return True, ""
    
    @staticmethod
    def sanitize_string(text: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize string input by removing potentially harmful characters.
        
        Args:
            text: Text to sanitize
            max_length: Optional maximum length
        
        Returns:
            Sanitized text
        """
        if not text:
            return ""
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        # Truncate if max_length specified
        if max_length and len(text) > max_length:
            text = text[:max_length]
        
        return text
