# Design Document

## Overview

This design document outlines the implementation strategy for removing authentication barriers and implementing comprehensive input validation across the DERSLY application. The solution focuses on two main areas:

1. **Authentication Removal**: Eliminate profile existence checks from all pages, making the app immediately usable without setup
2. **Input Validation**: Create a centralized validation system with clear, user-friendly error messages in Turkish

The design prioritizes user experience by removing friction points while ensuring data integrity through robust validation.

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     DERSLY Application                       │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   app.py     │  │  Page Files  │  │ Profile Page │      │
│  │              │  │              │  │              │      │
│  │ - No Auth    │  │ - No Auth    │  │ - Optional   │      │
│  │   Required   │  │   Checks     │  │   Profile    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│         │                  │                  │              │
│         └──────────────────┴──────────────────┘              │
│                            │                                 │
│                            ▼                                 │
│              ┌──────────────────────────┐                    │
│              │   Validation Layer       │                    │
│              │                          │                    │
│              │  - InputValidator        │                    │
│              │  - Validation Rules      │                    │
│              │  - Error Messages (TR)   │                    │
│              └──────────────────────────┘                    │
│                            │                                 │
│                            ▼                                 │
│              ┌──────────────────────────┐                    │
│              │   Manager Layer          │                    │
│              │                          │                    │
│              │  - CourseManager         │                    │
│              │  - AssignmentManager     │                    │
│              │  - GradeManager          │                    │
│              │  - UserManager           │                    │
│              └──────────────────────────┘                    │
│                            │                                 │
│                            ▼                                 │
│              ┌──────────────────────────┐                    │
│              │   Storage Layer          │                    │
│              │                          │                    │
│              │  - StorageManager        │                    │
│              │  - Session State         │                    │
│              └──────────────────────────┘                    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Components and Interfaces

### 1. Input Validator Component

**Location**: `utils/input_validator.py`

**Purpose**: Centralized validation logic for all user inputs with Turkish error messages

**Interface**:

```python
class InputValidator:
    """Centralized input validation with Turkish error messages."""
    
    @staticmethod
    def validate_course(course_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate course input data.
        
        Args:
            course_data: Dictionary with course fields
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass
    
    @staticmethod
    def validate_assignment(assignment_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate assignment input data.
        
        Args:
            assignment_data: Dictionary with assignment fields
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass
    
    @staticmethod
    def validate_grade(grade_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate grade input data.
        
        Args:
            grade_data: Dictionary with grade fields
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass
    
    @staticmethod
    def validate_profile(profile_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate profile input data.
        
        Args:
            profile_data: Dictionary with profile fields
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        pass
    
    # Helper validation methods
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format."""
        pass
    
    @staticmethod
    def validate_time_range(start_time: str, end_time: str) -> Tuple[bool, Optional[str]]:
        """Validate time range (start before end, minimum duration)."""
        pass
    
    @staticmethod
    def validate_string_length(value: str, min_len: int, max_len: int, field_name: str) -> Tuple[bool, Optional[str]]:
        """Validate string length with Turkish error message."""
        pass
    
    @staticmethod
    def validate_number_range(value: float, min_val: float, max_val: float, field_name: str) -> Tuple[bool, Optional[str]]:
        """Validate number range with Turkish error message."""
        pass
```

### 2. Validation Rules

**Course Validation Rules**:
- `course_name`: 2-100 characters, non-empty after strip
- `course_code`: 2-20 characters, alphanumeric with optional spaces/dashes
- `start_time` < `end_time`: Time range validation
- Duration: Minimum 30 minutes
- `credits`: 1-15 integer value

**Assignment Validation Rules**:
- `title`: 3-200 characters, non-empty after strip
- `description`: 0-2000 characters (optional)
- `due_date`: Not more than 2 years in future
- `due_date` in past: Warning only, allow submission
- `type`: Must be one of ['assignment', 'exam', 'project', 'quiz']
- `priority`: Must be one of ['low', 'medium', 'high']

**Grade Validation Rules**:
- `grade_value`: 0.0-4.0 float
- `letter_grade`: Must be one of ['AA', 'BA', 'BB', 'CB', 'CC', 'DC', 'DD', 'FD', 'FF']
- `credits`: 1-15 integer value

**Profile Validation Rules**:
- `name`: 2-100 characters, non-empty after strip
- `email`: Valid email format (regex pattern)
- `student_id`: 0-20 alphanumeric characters (optional)
- `class_year`: 1-8 integer value (optional)
- `department`: 0-100 characters (optional)

### 3. Error Message Templates

**Turkish Error Messages**:

```python
ERROR_MESSAGES = {
    # Course errors
    'course_name_too_short': '❌ Ders adı en az 2 karakter olmalıdır',
    'course_name_too_long': '❌ Ders adı en fazla 100 karakter olabilir',
    'course_code_too_short': '❌ Ders kodu en az 2 karakter olmalıdır',
    'course_code_invalid': '❌ Ders kodu sadece harf, rakam, boşluk ve tire içerebilir',
    'time_range_invalid': '❌ Başlangıç saati bitiş saatinden önce olmalıdır',
    'duration_too_short': '❌ Ders süresi en az 30 dakika olmalıdır',
    'credits_invalid': '❌ Kredi değeri 1-15 arasında olmalıdır',
    
    # Assignment errors
    'title_too_short': '❌ Başlık en az 3 karakter olmalıdır',
    'title_too_long': '❌ Başlık en fazla 200 karakter olabilir',
    'description_too_long': '❌ Açıklama en fazla 2000 karakter olabilir',
    'due_date_too_far': '❌ Bitiş tarihi 2 yıldan fazla ileri olamaz',
    'due_date_past_warning': '⚠️ Uyarı: Bitiş tarihi geçmişte',
    'type_invalid': '❌ Geçersiz görev türü',
    'priority_invalid': '❌ Geçersiz öncelik değeri',
    
    # Grade errors
    'grade_value_invalid': '❌ Not değeri 0.0-4.0 arasında olmalıdır',
    'letter_grade_invalid': '❌ Geçersiz harf notu',
    'grade_credits_invalid': '❌ Kredi değeri 1-15 arasında olmalıdır',
    
    # Profile errors
    'name_too_short': '❌ Ad Soyad en az 2 karakter olmalıdır',
    'name_too_long': '❌ Ad Soyad en fazla 100 karakter olabilir',
    'email_invalid': '❌ Geçerli bir e-posta adresi girin',
    'student_id_invalid': '❌ Öğrenci numarası sadece harf ve rakam içerebilir',
    'class_year_invalid': '❌ Sınıf 1-8 arasında olmalıdır',
    
    # Generic errors
    'required_field': '❌ Bu alan zorunludur',
    'invalid_input': '❌ Geçersiz giriş'
}
```

### 4. Modified Page Files

**Changes Required**:

1. **app.py**:
   - Remove `show_profile_setup()` function call
   - Remove profile existence check
   - Make profile display in sidebar conditional (only if exists)
   - Keep profile creation optional

2. **All Page Files** (`pages/*.py`):
   - Remove profile existence checks
   - Remove redirect to profile creation
   - Remove `st.stop()` calls after profile checks
   - Keep functionality accessible without profile

3. **Form Submissions**:
   - Add validation before data submission
   - Display validation errors using `st.error()`
   - Prevent form submission if validation fails
   - Maintain form data when validation fails

## Data Models

### Validation Result Model

```python
@dataclass
class ValidationResult:
    """Result of input validation."""
    is_valid: bool
    error_message: Optional[str] = None
    warning_message: Optional[str] = None
    field_errors: Dict[str, str] = field(default_factory=dict)
```

### Validation Context Model

```python
@dataclass
class ValidationContext:
    """Context for validation operations."""
    entity_type: str  # 'course', 'assignment', 'grade', 'profile'
    data: Dict[str, Any]
    strict_mode: bool = True  # If False, warnings don't block submission
```

## Error Handling

### Validation Error Flow

```
User Input → Form Submission → Validation Layer
                                      │
                                      ├─ Valid → Manager Layer → Storage
                                      │
                                      └─ Invalid → Error Display → Form Retained
```

### Error Display Strategy

1. **Immediate Feedback**: Show errors immediately after form submission
2. **Specific Messages**: Each validation rule has a specific Turkish error message
3. **Visual Indicators**: Use emoji icons (❌, ⚠️) for visual clarity
4. **Helpful Guidance**: Error messages explain what's wrong and how to fix it
5. **Form Preservation**: Keep user input in form when validation fails

### Warning vs Error

- **Errors**: Block form submission (e.g., invalid email, negative credits)
- **Warnings**: Show message but allow submission (e.g., past due date)

## Testing Strategy

### Unit Tests

**Test File**: `tests/test_input_validator.py`

**Test Coverage**:

1. **Course Validation Tests**:
   - Valid course data passes validation
   - Short course name fails validation
   - Invalid time range fails validation
   - Invalid credits fail validation
   - Minimum duration validation

2. **Assignment Validation Tests**:
   - Valid assignment data passes validation
   - Short title fails validation
   - Long description fails validation
   - Far future date fails validation
   - Past date shows warning but passes

3. **Grade Validation Tests**:
   - Valid grade data passes validation
   - Out of range grade value fails
   - Invalid letter grade fails
   - Invalid credits fail

4. **Profile Validation Tests**:
   - Valid profile data passes validation
   - Invalid email format fails
   - Short name fails validation
   - Invalid student ID fails

5. **Helper Method Tests**:
   - Email validation regex
   - Time range validation
   - String length validation
   - Number range validation

### Integration Tests

**Test File**: `tests/test_auth_removal.py`

**Test Coverage**:

1. **Page Access Tests**:
   - All pages accessible without profile
   - No redirects to profile creation
   - No `st.stop()` calls blocking access

2. **Form Submission Tests**:
   - Invalid data shows error and blocks submission
   - Valid data passes and creates entity
   - Form data preserved on validation failure

### Manual Testing Checklist

- [ ] Access each page without creating profile
- [ ] Submit course form with invalid data (verify error messages)
- [ ] Submit assignment form with invalid data (verify error messages)
- [ ] Submit grade form with invalid data (verify error messages)
- [ ] Submit profile form with invalid data (verify error messages)
- [ ] Verify Turkish error messages display correctly
- [ ] Verify form data is preserved on validation failure
- [ ] Verify warnings (past due date) allow submission
- [ ] Verify app functions correctly without profile
- [ ] Verify profile display in sidebar when profile exists

## Implementation Notes

### Phase 1: Create Validation Infrastructure
- Create `InputValidator` class with all validation methods
- Define error message constants
- Implement helper validation methods

### Phase 2: Remove Authentication
- Remove profile checks from `app.py`
- Remove profile checks from all page files
- Make profile display conditional in sidebar

### Phase 3: Integrate Validation
- Add validation to course forms
- Add validation to assignment forms
- Add validation to grade forms
- Add validation to profile forms

### Phase 4: Testing
- Write unit tests for validation logic
- Write integration tests for auth removal
- Perform manual testing
- Fix any issues discovered

## Security Considerations

1. **Input Sanitization**: All string inputs are stripped of leading/trailing whitespace
2. **Type Validation**: Ensure numeric inputs are within expected ranges
3. **Format Validation**: Email and other formatted fields use regex validation
4. **Length Limits**: Prevent excessively long inputs that could cause issues
5. **XSS Prevention**: Streamlit handles HTML escaping, but avoid raw HTML in user inputs

## Performance Considerations

1. **Validation Speed**: All validation operations are synchronous and fast (< 1ms)
2. **No External Calls**: Validation is purely local, no API calls
3. **Minimal Overhead**: Validation adds negligible overhead to form submission
4. **Caching**: No caching needed for validation logic

## Accessibility Considerations

1. **Clear Error Messages**: Turkish messages are clear and specific
2. **Visual Indicators**: Emoji icons provide visual cues
3. **Form Preservation**: Users don't lose their input on validation failure
4. **Consistent Patterns**: All forms follow the same validation pattern

## Future Enhancements

1. **Real-time Validation**: Add client-side validation as user types (if Streamlit supports)
2. **Custom Validation Rules**: Allow users to define custom validation rules
3. **Validation Profiles**: Different validation strictness levels
4. **Internationalization**: Support multiple languages for error messages
5. **Validation Logging**: Log validation failures for analytics
