"""
Input Validator for DERSLY Streamlit application.
Centralized validation logic with Turkish error messages.
"""
import re
from datetime import datetime, timedelta
from typing import Dict, Any, Tuple, Optional


class InputValidator:
    """Centralized input validation with Turkish error messages."""
    
    # Error message constants in Turkish with emoji icons
    ERROR_MESSAGES = {
        # Course errors
        'course_name_too_short': '❌ Ders adı en az 2 karakter olmalıdır',
        'course_name_too_long': '❌ Ders adı en fazla 100 karakter olabilir',
        'course_name_empty': '❌ Ders adı boş bırakılamaz',
        'course_code_too_short': '❌ Ders kodu en az 2 karakter olmalıdır',
        'course_code_too_long': '❌ Ders kodu en fazla 20 karakter olabilir',
        'course_code_invalid': '❌ Ders kodu sadece harf, rakam, boşluk ve tire içerebilir',
        'course_code_empty': '❌ Ders kodu boş bırakılamaz',
        'time_range_invalid': '❌ Başlangıç saati bitiş saatinden önce olmalıdır',
        'duration_too_short': '❌ Ders süresi en az 30 dakika olmalıdır',
        'credits_invalid': '❌ Kredi değeri 1-15 arasında olmalıdır',
        
        # Assignment errors
        'title_too_short': '❌ Başlık en az 3 karakter olmalıdır',
        'title_too_long': '❌ Başlık en fazla 200 karakter olabilir',
        'title_empty': '❌ Başlık boş bırakılamaz',
        'description_too_long': '❌ Açıklama en fazla 2000 karakter olabilir',
        'due_date_too_far': '❌ Bitiş tarihi 2 yıldan fazla ileri olamaz',
        'due_date_past_warning': '⚠️ Uyarı: Bitiş tarihi geçmişte',
        'type_invalid': '❌ Geçersiz görev türü',
        'priority_invalid': '❌ Geçersiz öncelik değeri',
        
        # Grade errors
        'grade_value_invalid': '❌ Not değeri 0.0-4.0 arasında olmalıdır',
        'letter_grade_invalid': '❌ Geçersiz harf notu (AA, BA, BB, CB, CC, DC, DD, FD, FF)',
        'grade_credits_invalid': '❌ Kredi değeri 1-15 arasında olmalıdır',
        
        # Profile errors
        'name_too_short': '❌ Ad Soyad en az 2 karakter olmalıdır',
        'name_too_long': '❌ Ad Soyad en fazla 100 karakter olabilir',
        'name_empty': '❌ Ad Soyad boş bırakılamaz',
        'email_invalid': '❌ Geçerli bir e-posta adresi girin (örnek: kullanici@universite.edu.tr)',
        'email_empty': '❌ E-posta boş bırakılamaz',
        'student_id_invalid': '❌ Öğrenci numarası sadece harf ve rakam içerebilir',
        'student_id_too_long': '❌ Öğrenci numarası en fazla 20 karakter olabilir',
        'class_year_invalid': '❌ Sınıf 1-8 arasında olmalıdır',
        'department_too_long': '❌ Bölüm adı en fazla 100 karakter olabilir',
        
        # Generic errors
        'required_field': '❌ Bu alan zorunludur',
        'invalid_input': '❌ Geçersiz giriş'
    }
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format using regex.
        
        Args:
            email: Email address to validate
        
        Returns:
            True if valid email format, False otherwise
        """
        if not email or not email.strip():
            return False
        
        # Basic email regex pattern
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email.strip()) is not None
    
    @staticmethod
    def validate_time_range(start_time: str, end_time: str) -> Tuple[bool, Optional[str]]:
        """
        Validate time range (start before end, minimum duration).
        
        Args:
            start_time: Start time in HH:MM format
            end_time: End time in HH:MM format
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            # Parse times
            start_parts = start_time.split(':')
            end_parts = end_time.split(':')
            
            start_hour, start_min = int(start_parts[0]), int(start_parts[1])
            end_hour, end_min = int(end_parts[0]), int(end_parts[1])
            
            # Convert to minutes for comparison
            start_minutes = start_hour * 60 + start_min
            end_minutes = end_hour * 60 + end_min
            
            # Check if start is before end
            if start_minutes >= end_minutes:
                return False, InputValidator.ERROR_MESSAGES['time_range_invalid']
            
            # Check minimum duration (30 minutes)
            duration = end_minutes - start_minutes
            if duration < 30:
                return False, InputValidator.ERROR_MESSAGES['duration_too_short']
            
            return True, None
            
        except (ValueError, IndexError, AttributeError):
            return False, InputValidator.ERROR_MESSAGES['invalid_input']
    
    @staticmethod
    def validate_string_length(value: str, min_len: int, max_len: int, 
                               field_name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate string length with Turkish error message.
        
        Args:
            value: String value to validate
            min_len: Minimum length
            max_len: Maximum length
            field_name: Name of field for error message
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not value or not value.strip():
            return False, InputValidator.ERROR_MESSAGES.get(f'{field_name}_empty', 
                                                            InputValidator.ERROR_MESSAGES['required_field'])
        
        length = len(value.strip())
        
        if length < min_len:
            return False, InputValidator.ERROR_MESSAGES.get(f'{field_name}_too_short',
                                                            f'❌ En az {min_len} karakter olmalıdır')
        
        if length > max_len:
            return False, InputValidator.ERROR_MESSAGES.get(f'{field_name}_too_long',
                                                            f'❌ En fazla {max_len} karakter olabilir')
        
        return True, None
    
    @staticmethod
    def validate_number_range(value: float, min_val: float, max_val: float, 
                              field_name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate number range with Turkish error message.
        
        Args:
            value: Number value to validate
            min_val: Minimum value
            max_val: Maximum value
            field_name: Name of field for error message
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if value < min_val or value > max_val:
            return False, InputValidator.ERROR_MESSAGES.get(f'{field_name}_invalid',
                                                            f'❌ {min_val}-{max_val} arasında olmalıdır')
        
        return True, None
    
    @staticmethod
    def validate_course(course_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate course input data.
        
        Args:
            course_data: Dictionary with course fields
                Required: course_name, course_code, start_time, end_time
                Optional: credits
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate course name
        is_valid, error = InputValidator.validate_string_length(
            course_data.get('course_name', ''), 2, 100, 'course_name'
        )
        if not is_valid:
            return False, error
        
        # Validate course code
        course_code = course_data.get('course_code', '').strip()
        is_valid, error = InputValidator.validate_string_length(
            course_code, 2, 20, 'course_code'
        )
        if not is_valid:
            return False, error
        
        # Validate course code format (alphanumeric with spaces and dashes)
        if not re.match(r'^[a-zA-Z0-9\s\-]+$', course_code):
            return False, InputValidator.ERROR_MESSAGES['course_code_invalid']
        
        # Validate time range
        start_time = course_data.get('start_time', '')
        end_time = course_data.get('end_time', '')
        is_valid, error = InputValidator.validate_time_range(start_time, end_time)
        if not is_valid:
            return False, error
        
        # Validate credits
        credits = course_data.get('credits', 3)
        is_valid, error = InputValidator.validate_number_range(credits, 1, 15, 'credits')
        if not is_valid:
            return False, error
        
        return True, None
    
    @staticmethod
    def validate_assignment(assignment_data: Dict[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Validate assignment input data.
        
        Args:
            assignment_data: Dictionary with assignment fields
                Required: title, due_date, type, priority
                Optional: description
        
        Returns:
            Tuple of (is_valid, error_message, warning_message)
        """
        warning_message = None
        
        # Validate title
        is_valid, error = InputValidator.validate_string_length(
            assignment_data.get('title', ''), 3, 200, 'title'
        )
        if not is_valid:
            return False, error, None
        
        # Validate description (optional)
        description = assignment_data.get('description', '')
        if description and len(description) > 2000:
            return False, InputValidator.ERROR_MESSAGES['description_too_long'], None
        
        # Validate due date
        due_date = assignment_data.get('due_date')
        if due_date:
            try:
                # Parse due date
                if isinstance(due_date, str):
                    if 'T' in due_date:
                        due_datetime = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                    else:
                        due_datetime = datetime.fromisoformat(due_date)
                else:
                    due_datetime = due_date
                
                now = datetime.now()
                
                # Check if too far in future (more than 2 years)
                two_years_future = now + timedelta(days=730)
                if due_datetime > two_years_future:
                    return False, InputValidator.ERROR_MESSAGES['due_date_too_far'], None
                
                # Check if in past (warning only)
                if due_datetime < now:
                    warning_message = InputValidator.ERROR_MESSAGES['due_date_past_warning']
                
            except (ValueError, AttributeError):
                return False, InputValidator.ERROR_MESSAGES['invalid_input'], None
        
        # Validate type
        valid_types = ['assignment', 'exam', 'project', 'quiz']
        if assignment_data.get('type') not in valid_types:
            return False, InputValidator.ERROR_MESSAGES['type_invalid'], None
        
        # Validate priority
        valid_priorities = ['low', 'medium', 'high']
        if assignment_data.get('priority') not in valid_priorities:
            return False, InputValidator.ERROR_MESSAGES['priority_invalid'], None
        
        return True, None, warning_message
    
    @staticmethod
    def validate_grade(grade_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate grade input data.
        
        Args:
            grade_data: Dictionary with grade fields
                Required: grade_value OR letter_grade, credits
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate grade value (if provided)
        if 'grade_value' in grade_data:
            grade_value = grade_data['grade_value']
            is_valid, error = InputValidator.validate_number_range(
                grade_value, 0.0, 4.0, 'grade_value'
            )
            if not is_valid:
                return False, error
        
        # Validate letter grade (if provided)
        if 'letter_grade' in grade_data:
            valid_grades = ['AA', 'BA', 'BB', 'CB', 'CC', 'DC', 'DD', 'FD', 'FF']
            if grade_data['letter_grade'] not in valid_grades:
                return False, InputValidator.ERROR_MESSAGES['letter_grade_invalid']
        
        # Validate credits
        credits = grade_data.get('credits', 3)
        is_valid, error = InputValidator.validate_number_range(credits, 1, 15, 'grade_credits')
        if not is_valid:
            return False, error
        
        return True, None
    
    @staticmethod
    def validate_profile(profile_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate profile input data.
        
        Args:
            profile_data: Dictionary with profile fields
                Required: name, email
                Optional: student_id, department, class_year
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate name
        is_valid, error = InputValidator.validate_string_length(
            profile_data.get('name', ''), 2, 100, 'name'
        )
        if not is_valid:
            return False, error
        
        # Validate email
        email = profile_data.get('email', '').strip()
        if not email:
            return False, InputValidator.ERROR_MESSAGES['email_empty']
        
        if not InputValidator.validate_email(email):
            return False, InputValidator.ERROR_MESSAGES['email_invalid']
        
        # Validate student ID (optional)
        student_id = profile_data.get('student_id', '')
        if student_id:
            student_id = student_id.strip()
            if len(student_id) > 20:
                return False, InputValidator.ERROR_MESSAGES['student_id_too_long']
            if not re.match(r'^[a-zA-Z0-9]+$', student_id):
                return False, InputValidator.ERROR_MESSAGES['student_id_invalid']
        
        # Validate class year (optional)
        class_year = profile_data.get('class_year')
        if class_year is not None:
            is_valid, error = InputValidator.validate_number_range(
                class_year, 1, 8, 'class_year'
            )
            if not is_valid:
                return False, error
        
        # Validate department (optional)
        department = profile_data.get('department', '')
        if department and len(department) > 100:
            return False, InputValidator.ERROR_MESSAGES['department_too_long']
        
        return True, None
