"""
Integration tests for authentication removal.
Tests that all pages are accessible without profile and validation works correctly.
"""
import pytest
from datetime import datetime, timedelta
from utils.user_manager import UserManager
from utils.course_manager import CourseManager
from utils.assignment_manager import AssignmentManager
from utils.grade_manager import GradeManager
from utils.storage_manager import StorageManager
from utils.input_validator import InputValidator


class TestPageAccessWithoutProfile:
    """Tests that pages are accessible without profile."""
    
    def test_user_manager_no_profile(self):
        """Test that UserManager works without profile."""
        # Should return None when no profile exists
        profile = UserManager.get_profile()
        assert profile is None or isinstance(profile, dict)
        
        # Should return False when no profile exists
        exists = UserManager.is_profile_exists()
        assert isinstance(exists, bool)
    
    def test_course_manager_without_profile(self):
        """Test that CourseManager works without profile."""
        # Should be able to get courses without profile
        courses = CourseManager.get_all_courses()
        assert isinstance(courses, list)
        
        # Should be able to get course count without profile
        count = CourseManager.get_course_count()
        assert isinstance(count, int)
    
    def test_assignment_manager_without_profile(self):
        """Test that AssignmentManager works without profile."""
        # Should be able to get assignments without profile
        assignments = AssignmentManager.get_all_assignments()
        assert isinstance(assignments, list)
        
        # Should be able to get assignment count without profile
        count = AssignmentManager.get_assignment_count()
        assert isinstance(count, int)
    
    def test_grade_manager_without_profile(self):
        """Test that GradeManager works without profile."""
        # Should be able to calculate GPA without profile
        gpa = GradeManager.calculate_gpa()
        assert isinstance(gpa, (int, float))
        
        # Should be able to get grade count without profile
        count = GradeManager.get_grade_count()
        assert isinstance(count, int)


class TestFormValidationWithInvalidData:
    """Tests that forms show errors with invalid data."""
    
    def test_course_form_invalid_data(self):
        """Test that course form validation catches invalid data."""
        # Test with short course name
        course_data = {
            'course_name': 'A',
            'course_code': 'CS201',
            'start_time': '09:00',
            'end_time': '10:30',
            'credits': 3
        }
        is_valid, error = InputValidator.validate_course(course_data)
        assert is_valid is False
        assert error is not None
        
        # Test with invalid time range
        course_data = {
            'course_name': 'Data Structures',
            'course_code': 'CS201',
            'start_time': '10:30',
            'end_time': '09:00',
            'credits': 3
        }
        is_valid, error = InputValidator.validate_course(course_data)
        assert is_valid is False
        assert error is not None
    
    def test_assignment_form_invalid_data(self):
        """Test that assignment form validation catches invalid data."""
        # Test with short title
        due_date = (datetime.now() + timedelta(days=7)).isoformat()
        assignment_data = {
            'title': 'HW',
            'type': 'assignment',
            'due_date': due_date,
            'priority': 'medium'
        }
        is_valid, error, warning = InputValidator.validate_assignment(assignment_data)
        assert is_valid is False
        assert error is not None
        
        # Test with invalid type
        assignment_data = {
            'title': 'Homework 1',
            'type': 'invalid_type',
            'due_date': due_date,
            'priority': 'medium'
        }
        is_valid, error, warning = InputValidator.validate_assignment(assignment_data)
        assert is_valid is False
        assert error is not None
    
    def test_grade_form_invalid_data(self):
        """Test that grade form validation catches invalid data."""
        # Test with invalid grade value
        grade_data = {
            'grade_value': 5.0,
            'credits': 3
        }
        is_valid, error = InputValidator.validate_grade(grade_data)
        assert is_valid is False
        assert error is not None
        
        # Test with invalid letter grade
        grade_data = {
            'letter_grade': 'ZZ',
            'credits': 3
        }
        is_valid, error = InputValidator.validate_grade(grade_data)
        assert is_valid is False
        assert error is not None
    
    def test_profile_form_invalid_data(self):
        """Test that profile form validation catches invalid data."""
        # Test with invalid email
        profile_data = {
            'name': 'John Doe',
            'email': 'invalid-email'
        }
        is_valid, error = InputValidator.validate_profile(profile_data)
        assert is_valid is False
        assert error is not None
        
        # Test with short name
        profile_data = {
            'name': 'A',
            'email': 'john@university.edu'
        }
        is_valid, error = InputValidator.validate_profile(profile_data)
        assert is_valid is False
        assert error is not None


class TestFormValidationWithValidData:
    """Tests that forms accept valid data."""
    
    def test_course_form_valid_data(self):
        """Test that course form validation accepts valid data."""
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
    
    def test_assignment_form_valid_data(self):
        """Test that assignment form validation accepts valid data."""
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
    
    def test_grade_form_valid_data(self):
        """Test that grade form validation accepts valid data."""
        grade_data = {
            'grade_value': 3.5,
            'credits': 3
        }
        is_valid, error = InputValidator.validate_grade(grade_data)
        assert is_valid is True
        assert error is None
    
    def test_profile_form_valid_data(self):
        """Test that profile form validation accepts valid data."""
        profile_data = {
            'name': 'John Doe',
            'email': 'john@university.edu',
            'student_id': '2020123456',
            'class_year': 3
        }
        is_valid, error = InputValidator.validate_profile(profile_data)
        assert is_valid is True
        assert error is None


class TestDataOperationsWithoutProfile:
    """Tests that data operations work without profile."""
    
    def test_add_course_without_profile(self):
        """Test that courses can be added without profile."""
        course_data = {
            'course_name': 'Test Course',
            'course_code': 'TEST101',
            'day': 'Monday',
            'start_time': '09:00',
            'end_time': '10:30',
            'credits': 3
        }
        
        # Validate first
        is_valid, error = InputValidator.validate_course(course_data)
        assert is_valid is True
        
        # Should be able to add course
        course_id = CourseManager.add_course(course_data)
        assert isinstance(course_id, int)
        
        # Should be able to retrieve course
        course = CourseManager.get_course(course_id)
        assert course is not None
        assert course['course_name'] == 'Test Course'
    
    def test_add_assignment_without_profile(self):
        """Test that assignments can be added without profile."""
        due_date = (datetime.now() + timedelta(days=7)).isoformat()
        assignment_data = {
            'title': 'Test Assignment',
            'type': 'assignment',
            'due_date': due_date,
            'priority': 'medium',
            'status': 'pending'
        }
        
        # Validate first
        is_valid, error, warning = InputValidator.validate_assignment(assignment_data)
        assert is_valid is True
        
        # Should be able to add assignment
        assignment_id = AssignmentManager.add_assignment(assignment_data)
        assert isinstance(assignment_id, int)
        
        # Should be able to retrieve assignment
        assignment = AssignmentManager.get_assignment(assignment_id)
        assert assignment is not None
        assert assignment['title'] == 'Test Assignment'
    
    def test_add_grade_without_profile(self):
        """Test that grades can be added without profile."""
        grade_data = {
            'course_name': 'Test Course',
            'grade': 3.5,
            'credits': 3,
            'semester': 'Fall',
            'year': 2024
        }
        
        # Validate first (using grade_value for validation)
        validation_data = grade_data.copy()
        validation_data['grade_value'] = validation_data.pop('grade')
        is_valid, error = InputValidator.validate_grade(validation_data)
        assert is_valid is True
        
        # Should be able to add grade
        grade_id = GradeManager.add_grade(grade_data)
        assert isinstance(grade_id, int)
        
        # Should be able to retrieve grade
        grade = GradeManager.get_grade(grade_id)
        assert grade is not None
        assert grade['course_name'] == 'Test Course'


class TestProfileCreationOptional:
    """Tests that profile creation is optional."""
    
    def test_profile_creation_is_optional(self):
        """Test that app works without creating profile."""
        # Should be able to check if profile exists
        exists = UserManager.is_profile_exists()
        assert isinstance(exists, bool)
        
        # Should be able to get profile (returns None if not exists)
        profile = UserManager.get_profile()
        assert profile is None or isinstance(profile, dict)
        
        # Should be able to use all managers without profile
        courses = CourseManager.get_all_courses()
        assignments = AssignmentManager.get_all_assignments()
        gpa = GradeManager.calculate_gpa()
        
        assert isinstance(courses, list)
        assert isinstance(assignments, list)
        assert isinstance(gpa, (int, float))
    
    def test_profile_can_be_created_later(self):
        """Test that profile can be created at any time."""
        # Create profile
        profile_data = {
            'name': 'Test User',
            'email': 'test@university.edu'
        }
        
        # Validate first
        is_valid, error = InputValidator.validate_profile(profile_data)
        assert is_valid is True
        
        # Create profile
        profile = UserManager.create_profile(
            name='Test User',
            email='test@university.edu'
        )
        
        assert profile is not None
        assert profile['name'] == 'Test User'
        assert profile['email'] == 'test@university.edu'
        
        # Should now exist
        exists = UserManager.is_profile_exists()
        assert exists is True
