# Implementation Plan

- [x] 1. Create centralized input validation system


  - Create `utils/input_validator.py` with `InputValidator` class
  - Implement error message constants in Turkish with emoji icons
  - Implement helper validation methods (email, time range, string length, number range)
  - _Requirements: 2.6, 3.6, 4.4, 5.5, 6.1, 6.2, 6.3, 6.4_

- [x] 1.1 Implement course validation method

  - Write `validate_course()` method with all course validation rules
  - Validate course name (2-100 characters)
  - Validate course code (2-20 characters, alphanumeric)
  - Validate time range (start before end, minimum 30 minutes)
  - Validate credits (1-15)
  - Return tuple of (is_valid, error_message)
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7_

- [x] 1.2 Implement assignment validation method

  - Write `validate_assignment()` method with all assignment validation rules
  - Validate title (3-200 characters)
  - Validate description (max 2000 characters)
  - Validate due date (not more than 2 years in future)
  - Handle past due date as warning (allow submission)
  - Validate type and priority enums
  - Return tuple of (is_valid, error_message)
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7_

- [x] 1.3 Implement grade validation method

  - Write `validate_grade()` method with all grade validation rules
  - Validate grade value (0.0-4.0)
  - Validate letter grade (AA, BA, BB, CB, CC, DC, DD, FD, FF)
  - Validate credits (1-15)
  - Return tuple of (is_valid, error_message)
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_

- [x] 1.4 Implement profile validation method

  - Write `validate_profile()` method with all profile validation rules
  - Validate name (2-100 characters)
  - Validate email format using regex
  - Validate student ID (alphanumeric, optional)
  - Validate class year (1-8, optional)
  - Return tuple of (is_valid, error_message)
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [x] 2. Remove authentication barriers from main app


  - Remove profile existence check from `app.py`
  - Remove `show_profile_setup()` function call
  - Make profile display in sidebar conditional (only show if profile exists)
  - Ensure app loads directly to main content without profile requirement
  - _Requirements: 1.1, 1.4, 1.5_

- [x] 3. Remove authentication checks from all page files


  - Remove profile existence checks from `pages/1_🏠_Ana_Sayfa.py`
  - Remove profile existence checks from `pages/2_📚_Dersler.py`
  - Remove profile existence checks from `pages/3_📝_Ödevler.py`
  - Remove profile existence checks from `pages/4_📅_Takvim.py`
  - Remove profile existence checks from `pages/5_🔔_Hatirlaticilar.py`
  - Remove profile existence checks from `pages/6_📊_Not_Ortalamasi.py`
  - Remove all `st.stop()` calls that block page access
  - Remove redirect buttons to profile creation
  - _Requirements: 1.1, 1.2, 1.3_

- [x] 4. Integrate validation into course forms


  - Import `InputValidator` in `pages/2_📚_Dersler.py`
  - Add validation call before `CourseManager.add_course()`
  - Display validation errors using `st.error()` with Turkish messages
  - Prevent form submission if validation fails
  - Add validation to course edit form
  - Ensure form data is preserved on validation failure
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 6.5, 6.6_

- [x] 5. Integrate validation into assignment forms


  - Import `InputValidator` in `pages/3_📝_Ödevler.py`
  - Add validation call before `AssignmentManager.add_assignment()`
  - Display validation errors using `st.error()` with Turkish messages
  - Display warnings using `st.warning()` for past due dates
  - Prevent form submission if validation fails (but allow warnings)
  - Ensure form data is preserved on validation failure
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 6.5, 6.6_

- [x] 6. Integrate validation into grade forms


  - Import `InputValidator` in `pages/6_📊_Not_Ortalamasi.py`
  - Add validation call before `GradeManager.add_grade()`
  - Display validation errors using `st.error()` with Turkish messages
  - Prevent form submission if validation fails
  - Ensure form data is preserved on validation failure
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 6.5, 6.6_

- [x] 7. Integrate validation into profile forms


  - Import `InputValidator` in `pages/7_👤_Profil.py`
  - Add validation call before `UserManager.create_profile()`
  - Add validation call before `UserManager.update_profile()`
  - Display validation errors using `st.error()` with Turkish messages
  - Prevent form submission if validation fails
  - Ensure form data is preserved on validation failure
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 6.5, 6.6_

- [x] 8. Write unit tests for validation logic


  - Create `tests/test_input_validator.py`
  - Write tests for course validation (valid data, invalid name, invalid time range, invalid credits)
  - Write tests for assignment validation (valid data, invalid title, invalid description, far future date, past date warning)
  - Write tests for grade validation (valid data, invalid grade value, invalid letter grade, invalid credits)
  - Write tests for profile validation (valid data, invalid email, invalid name, invalid student ID)
  - Write tests for helper methods (email regex, time range, string length, number range)
  - _Requirements: All requirements_

- [x] 9. Write integration tests for authentication removal


  - Create `tests/test_auth_removal.py`
  - Write tests to verify all pages are accessible without profile
  - Write tests to verify no redirects to profile creation occur
  - Write tests to verify form submissions with invalid data show errors
  - Write tests to verify form submissions with valid data succeed
  - _Requirements: 1.1, 1.2, 1.3, 1.4_

- [x] 10. Manual testing and verification



  - Test accessing each page without creating a profile
  - Test submitting course form with various invalid inputs
  - Test submitting assignment form with various invalid inputs
  - Test submitting grade form with various invalid inputs
  - Test submitting profile form with various invalid inputs
  - Verify all Turkish error messages display correctly
  - Verify form data is preserved when validation fails
  - Verify warnings allow submission while errors block it
  - Verify app functions correctly without profile
  - Verify profile displays in sidebar when it exists
  - _Requirements: All requirements_
