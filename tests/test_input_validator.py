"""
Unit tests for InputValidator class.
Tests all validation methods and helper functions.
"""
import pytest
from datetime import datetime, timedelta
from utils.input_validator import InputValidator


class TestCourseValidation:
    """Tests for course validation."""
    
    def test_valid_course_data(self):
        """Test that valid course data passes validation."""
        course_data = {
            'course_name': 'Data Structures',
            'course_code': 'CS201',
            'start_time': '09:00',
            'end_time': '10:30',
            'credits': 3
        }
        is_valid, error = InputValidator.validate_course(course_data)
        assert is_valid is True
        assert error is None
    
    def test_course_name_too_short(self):
        """Test that short course name fails validation."""
        course_data = {
            'course_name': 'A',
            'course_code': 'CS201',
            'start_time': '09:00',
            'end_time': '10:30',
            'credits': 3
        }
        is_valid, error = InputValidator.validate_course(course_data)
        assert is_valid is False
        assert 'en az 2 karakter' in error
    
    def test_course_name_empty(self):
        """Test that empty course name fails validation."""
        course_data = {
            'course_name': '   ',
            'course_code': 'CS201',
            'start_time': '09:00',
            'end_time': '10:30',
            'credits': 3
        }
        is_valid, error = InputValidator.validate_course(course_data)
        assert is_valid is False
        assert 'boş bırakılamaz' in error
    
    def test_course_code_invalid_characters(self):
        """Test that course code with invalid characters fails."""
        course_data = {
            'course_name': 'Data Structures',
            'course_code': 'CS@201',
            'start_time': '09:00',
            'end_time': '10:30',
            'credits': 3
        }
        is_valid, error = InputValidator.validate_course(course_data)
        assert is_valid is False
        assert 'harf, rakam, boşluk ve tire' in error
    
    def test_invalid_time_range(self):
        """Test that invalid time range fails validation."""
        course_data = {
            'course_name': 'Data Structures',
            'course_code': 'CS201',
            'start_time': '10:30',
            'end_time': '09:00',
            'credits': 3
        }
        is_valid, error = InputValidator.validate_course(course_data)
        assert is_valid is False
        assert 'Başlangıç saati bitiş saatinden önce' in error
    
    def test_duration_too_short(self):
        """Test that duration less than 30 minutes fails."""
        course_data = {
            'course_name': 'Data Structures',
            'course_code': 'CS201',
            'start_time': '09:00',
            'end_time': '09:20',
            'credits': 3
        }
        is_valid, error = InputValidator.validate_course(course_data)
        assert is_valid is False
        assert 'en az 30 dakika' in error
    
    def test_invalid_credits_low(self):
        """Test that credits below 1 fail validation."""
        course_data = {
            'course_name': 'Data Structures',
            'course_code': 'CS201',
            'start_time': '09:00',
            'end_time': '10:30',
            'credits': 0
        }
        is_valid, error = InputValidator.validate_course(course_data)
        assert is_valid is False
        assert '1-15 arasında' in error
    
    def test_invalid_credits_high(self):
        """Test that credits above 15 fail validation."""
        course_data = {
            'course_name': 'Data Structures',
            'course_code': 'CS201',
            'start_time': '09:00',
            'end_time': '10:30',
            'credits': 20
        }
        is_valid, error = InputValidator.validate_course(course_data)
        assert is_valid is False
        assert '1-15 arasında' in error


class TestAssignmentValidation:
    """Tests for assignment validation."""
    
    def test_valid_assignment_data(self):
        """Test that valid assignment data passes validation."""
        due_date = (datetime.now() + timedelta(days=7)).isoformat()
        assignment_data = {
            'title': 'Homework 1',
            'description': 'Complete exercises 1-10',
            'type': 'assignment',
            'due_date': due_date,
            'priority': 'medium'
        }
        is_valid, error, warning = InputValidator.validate_assignment(assignment_data)
        assert is_valid is True
        assert error is None
        assert warning is None
    
    def test_title_too_short(self):
        """Test that short title fails validation."""
        due_date = (datetime.now() + timedelta(days=7)).isoformat()
        assignment_data = {
            'title': 'HW',
            'description': 'Complete exercises',
            'type': 'assignment',
            'due_date': due_date,
            'priority': 'medium'
        }
        is_valid, error, warning = InputValidator.validate_assignment(assignment_data)
        assert is_valid is False
        assert 'en az 3 karakter' in error
    
    def test_title_too_long(self):
        """Test that very long title fails validation."""
        due_date = (datetime.now() + timedelta(days=7)).isoformat()
        assignment_data = {
            'title': 'A' * 250,
            'description': 'Complete exercises',
            'type': 'assignment',
            'due_date': due_date,
            'priority': 'medium'
        }
        is_valid, error, warning = InputValidator.validate_assignment(assignment_data)
        assert is_valid is False
        assert 'en fazla 200 karakter' in error
    
    def test_description_too_long(self):
        """Test that very long description fails validation."""
        due_date = (datetime.now() + timedelta(days=7)).isoformat()
        assignment_data = {
            'title': 'Homework 1',
            'description': 'A' * 2500,
            'type': 'assignment',
            'due_date': due_date,
            'priority': 'medium'
        }
        is_valid, error, warning = InputValidator.validate_assignment(assignment_data)
        assert is_valid is False
        assert 'en fazla 2000 karakter' in error
    
    def test_due_date_too_far(self):
        """Test that due date more than 2 years in future fails."""
        due_date = (datetime.now() + timedelta(days=800)).isoformat()
        assignment_data = {
            'title': 'Homework 1',
            'description': 'Complete exercises',
            'type': 'assignment',
            'due_date': due_date,
            'priority': 'medium'
        }
        is_valid, error, warning = InputValidator.validate_assignment(assignment_data)
        assert is_valid is False
        assert '2 yıldan fazla' in error
    
    def test_past_due_date_warning(self):
        """Test that past due date shows warning but passes."""
        due_date = (datetime.now() - timedelta(days=1)).isoformat()
        assignment_data = {
            'title': 'Homework 1',
            'description': 'Complete exercises',
            'type': 'assignment',
            'due_date': due_date,
            'priority': 'medium'
        }
        is_valid, error, warning = InputValidator.validate_assignment(assignment_data)
        assert is_valid is True
        assert error is None
        assert warning is not None
        assert 'geçmişte' in warning
    
    def test_invalid_type(self):
        """Test that invalid type fails validation."""
        due_date = (datetime.now() + timedelta(days=7)).isoformat()
        assignment_data = {
            'title': 'Homework 1',
            'description': 'Complete exercises',
            'type': 'invalid_type',
            'due_date': due_date,
            'priority': 'medium'
        }
        is_valid, error, warning = InputValidator.validate_assignment(assignment_data)
        assert is_valid is False
        assert 'Geçersiz görev türü' in error
    
    def test_invalid_priority(self):
        """Test that invalid priority fails validation."""
        due_date = (datetime.now() + timedelta(days=7)).isoformat()
        assignment_data = {
            'title': 'Homework 1',
            'description': 'Complete exercises',
            'type': 'assignment',
            'due_date': due_date,
            'priority': 'invalid_priority'
        }
        is_valid, error, warning = InputValidator.validate_assignment(assignment_data)
        assert is_valid is False
        assert 'Geçersiz öncelik' in error


class TestGradeValidation:
    """Tests for grade validation."""
    
    def test_valid_grade_data(self):
        """Test that valid grade data passes validation."""
        grade_data = {
            'grade_value': 3.5,
            'credits': 3
        }
        is_valid, error = InputValidator.validate_grade(grade_data)
        assert is_valid is True
        assert error is None
    
    def test_grade_value_too_low(self):
        """Test that grade value below 0 fails validation."""
        grade_data = {
            'grade_value': -0.5,
            'credits': 3
        }
        is_valid, error = InputValidator.validate_grade(grade_data)
        assert is_valid is False
        assert '0.0-4.0 arasında' in error
    
    def test_grade_value_too_high(self):
        """Test that grade value above 4.0 fails validation."""
        grade_data = {
            'grade_value': 4.5,
            'credits': 3
        }
        is_valid, error = InputValidator.validate_grade(grade_data)
        assert is_valid is False
        assert '0.0-4.0 arasında' in error
    
    def test_valid_letter_grade(self):
        """Test that valid letter grade passes validation."""
        grade_data = {
            'letter_grade': 'AA',
            'credits': 3
        }
        is_valid, error = InputValidator.validate_grade(grade_data)
        assert is_valid is True
        assert error is None
    
    def test_invalid_letter_grade(self):
        """Test that invalid letter grade fails validation."""
        grade_data = {
            'letter_grade': 'ZZ',
            'credits': 3
        }
        is_valid, error = InputValidator.validate_grade(grade_data)
        assert is_valid is False
        assert 'Geçersiz harf notu' in error
    
    def test_invalid_credits(self):
        """Test that invalid credits fail validation."""
        grade_data = {
            'grade_value': 3.5,
            'credits': 20
        }
        is_valid, error = InputValidator.validate_grade(grade_data)
        assert is_valid is False
        assert '1-15 arasında' in error


class TestProfileValidation:
    """Tests for profile validation."""
    
    def test_valid_profile_data(self):
        """Test that valid profile data passes validation."""
        profile_data = {
            'name': 'John Doe',
            'email': 'john@university.edu',
            'student_id': '2020123456',
            'class_year': 3
        }
        is_valid, error = InputValidator.validate_profile(profile_data)
        assert is_valid is True
        assert error is None
    
    def test_name_too_short(self):
        """Test that short name fails validation."""
        profile_data = {
            'name': 'A',
            'email': 'john@university.edu'
        }
        is_valid, error = InputValidator.validate_profile(profile_data)
        assert is_valid is False
        assert 'en az 2 karakter' in error
    
    def test_invalid_email(self):
        """Test that invalid email fails validation."""
        profile_data = {
            'name': 'John Doe',
            'email': 'invalid-email'
        }
        is_valid, error = InputValidator.validate_profile(profile_data)
        assert is_valid is False
        assert 'Geçerli bir e-posta' in error
    
    def test_empty_email(self):
        """Test that empty email fails validation."""
        profile_data = {
            'name': 'John Doe',
            'email': '   '
        }
        is_valid, error = InputValidator.validate_profile(profile_data)
        assert is_valid is False
        assert 'E-posta boş bırakılamaz' in error
    
    def test_invalid_student_id(self):
        """Test that student ID with special characters fails."""
        profile_data = {
            'name': 'John Doe',
            'email': 'john@university.edu',
            'student_id': '2020-123456'
        }
        is_valid, error = InputValidator.validate_profile(profile_data)
        assert is_valid is False
        assert 'sadece harf ve rakam' in error
    
    def test_student_id_too_long(self):
        """Test that very long student ID fails validation."""
        profile_data = {
            'name': 'John Doe',
            'email': 'john@university.edu',
            'student_id': '1' * 25
        }
        is_valid, error = InputValidator.validate_profile(profile_data)
        assert is_valid is False
        assert 'en fazla 20 karakter' in error
    
    def test_invalid_class_year(self):
        """Test that invalid class year fails validation."""
        profile_data = {
            'name': 'John Doe',
            'email': 'john@university.edu',
            'class_year': 10
        }
        is_valid, error = InputValidator.validate_profile(profile_data)
        assert is_valid is False
        assert '1-8 arasında' in error


class TestHelperMethods:
    """Tests for helper validation methods."""
    
    def test_valid_email(self):
        """Test that valid email passes validation."""
        assert InputValidator.validate_email('user@example.com') is True
        assert InputValidator.validate_email('john.doe@university.edu.tr') is True
    
    def test_invalid_email(self):
        """Test that invalid email fails validation."""
        assert InputValidator.validate_email('invalid') is False
        assert InputValidator.validate_email('user@') is False
        assert InputValidator.validate_email('@example.com') is False
        assert InputValidator.validate_email('') is False
    
    def test_valid_time_range(self):
        """Test that valid time range passes validation."""
        is_valid, error = InputValidator.validate_time_range('09:00', '10:30')
        assert is_valid is True
        assert error is None
    
    def test_invalid_time_range_reversed(self):
        """Test that reversed time range fails validation."""
        is_valid, error = InputValidator.validate_time_range('10:30', '09:00')
        assert is_valid is False
        assert error is not None
    
    def test_time_range_too_short(self):
        """Test that time range less than 30 minutes fails."""
        is_valid, error = InputValidator.validate_time_range('09:00', '09:20')
        assert is_valid is False
        assert 'en az 30 dakika' in error
    
    def test_valid_string_length(self):
        """Test that valid string length passes validation."""
        is_valid, error = InputValidator.validate_string_length('Test', 2, 10, 'test_field')
        assert is_valid is True
        assert error is None
    
    def test_string_too_short(self):
        """Test that short string fails validation."""
        is_valid, error = InputValidator.validate_string_length('A', 2, 10, 'test_field')
        assert is_valid is False
        assert error is not None
    
    def test_string_too_long(self):
        """Test that long string fails validation."""
        is_valid, error = InputValidator.validate_string_length('A' * 20, 2, 10, 'test_field')
        assert is_valid is False
        assert error is not None
    
    def test_valid_number_range(self):
        """Test that valid number range passes validation."""
        is_valid, error = InputValidator.validate_number_range(5, 1, 10, 'test_field')
        assert is_valid is True
        assert error is None
    
    def test_number_below_range(self):
        """Test that number below range fails validation."""
        is_valid, error = InputValidator.validate_number_range(0, 1, 10, 'test_field')
        assert is_valid is False
        assert error is not None
    
    def test_number_above_range(self):
        """Test that number above range fails validation."""
        is_valid, error = InputValidator.validate_number_range(15, 1, 10, 'test_field')
        assert is_valid is False
        assert error is not None
