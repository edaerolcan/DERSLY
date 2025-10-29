# Implementation Plan

- [x] 1. Create core storage infrastructure

  - [x] 1.1 Implement StorageManager class with session state initialization


    - Create `utils/storage_manager.py` with `StorageManager` class
    - Implement `initialize_storage()` method to set up empty data structures in session state
    - Implement `get_storage_info()` method to track storage usage
    - Implement `clear_all_data()` method with proper cleanup
    - _Requirements: 1.1, 1.2, 6.4, 6.5_



  - [ ] 1.2 Implement export functionality
    - Add `export_data()` method to serialize all session state data to dictionary
    - Include metadata (version, timestamp) in export format
    - Handle datetime serialization to ISO format strings


    - Ensure all data types are JSON-serializable
    - _Requirements: 2.2, 2.3, 2.4_

  - [ ] 1.3 Implement import functionality with validation
    - Add `import_data()` method to deserialize and load data into session state
    - Implement JSON schema validation for imported data
    - Add data integrity checks (required fields, data types)
    - Handle version compatibility checks
    - Return success/failure status with error messages
    - _Requirements: 3.3, 3.4, 3.6_

  - [ ]* 1.4 Write unit tests for StorageManager
    - Test initialization of empty storage

    - Test export with various data scenarios
    - Test import with valid and invalid data
    - Test clear all data functionality
    - _Requirements: 1.1, 2.2, 3.3, 6.4_

- [x] 2. Create data manager classes

  - [x] 2.1 Implement UserManager for profile management

    - Create `utils/user_manager.py` with `UserManager` class
    - Implement `create_profile()` method to store user profile in session state
    - Implement `get_profile()` method to retrieve current profile
    - Implement `update_profile()` method for profile updates
    - Implement `is_profile_exists()` method to check profile existence
    - _Requirements: 1.1, 1.2_

  - [x] 2.2 Implement CourseManager for course operations


    - Create `utils/course_manager.py` with `CourseManager` class
    - Implement `add_course()` method with auto-increment ID generation
    - Implement `get_course()` and `get_all_courses()` methods
    - Implement `update_course()` and `delete_course()` methods
    - Implement `get_courses_by_day()` for schedule filtering
    - Store courses as dictionary with ID keys in session state
    - _Requirements: 1.2, 1.3_

  - [x] 2.3 Implement AssignmentManager for assignment operations


    - Create `utils/assignment_manager.py` with `AssignmentManager` class
    - Implement `add_assignment()` method with auto-increment ID generation
    - Implement `get_assignment()` and `get_all_assignments()` methods
    - Implement `update_assignment()` and `delete_assignment()` methods
    - Implement `get_assignments_by_status()` for filtering
    - Implement `get_upcoming_assignments()` for deadline tracking
    - _Requirements: 1.2, 1.3_

  - [x] 2.4 Implement GradeManager for grade operations and GPA calculation


    - Create `utils/grade_manager.py` with `GradeManager` class
    - Implement `add_grade()`, `get_all_grades()`, `update_grade()`, `delete_grade()` methods
    - Implement `calculate_gpa()` method for overall GPA calculation
    - Implement `calculate_semester_gpa()` for semester-specific GPA
    - Implement `get_grades_by_semester()` for filtering
    - _Requirements: 1.2, 1.3_

  - [ ]* 2.5 Write unit tests for manager classes
    - Test CRUD operations for each manager
    - Test ID generation and uniqueness
    - Test filtering and calculation methods
    - Test edge cases (empty data, invalid IDs)
    - _Requirements: 1.2, 1.3_

- [x] 3. Implement export/import UI components

  - [x] 3.1 Create export UI component


    - Create `utils/export_import_ui.py` file
    - Implement `show_export_button()` function
    - Generate filename with timestamp (e.g., "dersly_backup_2025-10-29_10-30.json")
    - Use `st.download_button()` to trigger JSON file download
    - Display success message after export
    - Update metadata with last export timestamp
    - _Requirements: 2.1, 2.2, 2.4, 2.5_

  - [x] 3.2 Create import UI component with confirmation dialog


    - Implement `show_import_button()` function
    - Use `st.file_uploader()` for JSON file upload
    - Check if existing data exists in session state
    - Display confirmation dialog with warning if data exists
    - Validate uploaded JSON format and structure
    - Display appropriate error messages for invalid files
    - Update session state with imported data on confirmation
    - Display success message and trigger page rerun
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 4.1, 4.2, 4.3, 4.4, 4.5_

  - [x] 3.3 Create clear data UI component


    - Implement `show_clear_data_button()` function
    - Display button in settings/profile section
    - Show strong warning confirmation dialog
    - Require explicit user confirmation before clearing
    - Call `StorageManager.clear_all_data()` on confirmation
    - Display success message and reset UI
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

  - [x] 3.4 Create storage info display component


    - Implement `show_storage_info()` function
    - Display current storage usage statistics
    - Show number of courses, assignments, grades
    - Estimate storage size in KB/MB
    - Display warning if approaching limits (>80%)
    - Provide guidance on exporting data if needed
    - _Requirements: 5.1, 5.2, 5.3_

- [x] 4. Update application pages to use new storage system

  - [x] 4.1 Simplify app.py authentication


    - Remove database connection test from startup
    - Remove `AuthManager` import and authentication logic
    - Simplify main page to check for user profile existence
    - Redirect to profile setup if no profile exists
    - Remove login/registration forms
    - Update navigation to show main app directly
    - _Requirements: 1.1, 1.5_

  - [x] 4.2 Update Home page (pages/1_🏠_Home.py)


    - Replace database operations with `StorageManager` initialization
    - Use `CourseManager` and `AssignmentManager` for data retrieval
    - Update statistics display to use session state data
    - Remove database session management
    - _Requirements: 1.2, 1.3, 1.4_

  - [x] 4.3 Update Courses page (pages/2_📚_Courses.py)


    - Replace database operations with `CourseManager` methods
    - Update course creation to use `add_course()`
    - Update course editing to use `update_course()`
    - Update course deletion to use `delete_course()`
    - Update schedule display to use `get_courses_by_day()`
    - Remove database session management
    - _Requirements: 1.2, 1.3_

  - [x] 4.4 Update Assignments page (pages/3_📝_Assignments.py)


    - Replace database operations with `AssignmentManager` methods
    - Update assignment creation to use `add_assignment()`
    - Update assignment editing to use `update_assignment()`
    - Update assignment deletion to use `delete_assignment()`
    - Update status filtering to use `get_assignments_by_status()`
    - Update upcoming assignments to use `get_upcoming_assignments()`
    - Remove database session management
    - _Requirements: 1.2, 1.3_

  - [x] 4.5 Update GPA page (pages/6_📊_GPA.py)


    - Replace database operations with `GradeManager` methods
    - Update grade entry creation to use `add_grade()`
    - Update grade editing to use `update_grade()`
    - Update grade deletion to use `delete_grade()`
    - Update GPA calculation to use `calculate_gpa()` and `calculate_semester_gpa()`
    - Remove database session management
    - _Requirements: 1.2, 1.3_

  - [x] 4.6 Update Profile page (pages/7_👤_Profile.py)


    - Replace database operations with `UserManager` methods
    - Update profile display to use `get_profile()`
    - Update profile editing to use `update_profile()`
    - Add export/import UI components using `show_export_button()` and `show_import_button()`
    - Add storage info display using `show_storage_info()`
    - Add clear data button using `show_clear_data_button()`
    - Remove database session management
    - _Requirements: 1.2, 1.3, 2.1, 2.5, 3.1, 3.2, 5.1, 6.1_

  - [x] 4.7 Update Calendar page (pages/4_📅_Calendar.py)


    - Replace database operations with `AssignmentManager` methods
    - Update calendar display to use session state data
    - Remove database session management
    - _Requirements: 1.2, 1.3_

  - [x] 4.8 Update Reminders page (pages/5_🔔_Reminders.py)


    - Replace database operations with session state access
    - Update reminder display and management
    - Remove database session management
    - _Requirements: 1.2, 1.3_

- [x] 5. Remove database dependencies

  - [x] 5.1 Delete database module files


    - Delete `database/models.py`
    - Delete `database/connection.py`
    - Delete `database/operations.py` (if exists)
    - Delete entire `database/` directory
    - _Requirements: 1.5_

  - [x] 5.2 Update configuration files


    - Remove database-related settings from `config.py`
    - Remove `DATABASE_URL`, `BCRYPT_ROUNDS` from config
    - Keep only necessary app configuration
    - Update `.env` file to remove database credentials
    - _Requirements: 1.5_

  - [x] 5.3 Update dependencies


    - Remove `sqlalchemy` from `requirements.txt`
    - Remove `pymysql` or database drivers from `requirements.txt`
    - Remove `bcrypt` from `requirements.txt` (no longer needed for password hashing)
    - Remove `python-dotenv` if no longer needed
    - _Requirements: 1.5_

  - [x] 5.4 Clean up authentication utilities


    - Delete `utils/auth.py` (no longer needed)
    - Remove password hashing and verification functions
    - Remove authentication-related imports from other files
    - _Requirements: 1.5_

- [x] 6. Add error handling and user feedback

  - [x] 6.1 Implement custom exception classes


    - Create `utils/exceptions.py` file
    - Define `StorageError`, `StorageQuotaExceeded`, `InvalidDataFormat`, `DataCorrupted` exceptions
    - Add descriptive error messages
    - _Requirements: 5.4, 5.5_

  - [x] 6.2 Add error handling to storage operations

    - Wrap storage operations in try-except blocks
    - Catch and handle storage quota exceeded errors
    - Display user-friendly error messages using `st.error()`
    - Suggest export when storage is full
    - Log errors for debugging
    - _Requirements: 5.2, 5.3, 5.4, 5.5_

  - [x] 6.3 Add validation error handling for import

    - Validate JSON structure before importing
    - Check for required fields and data types
    - Display specific error messages for validation failures
    - Prevent corrupted data from being imported
    - _Requirements: 3.4, 3.5_

  - [x] 6.4 Add user feedback for all operations

    - Display success messages with `st.success()` for completed operations
    - Display info messages with `st.info()` for guidance
    - Display warning messages with `st.warning()` for confirmations
    - Use `st.balloons()` or `st.snow()` for major successes
    - _Requirements: 2.5, 3.6, 4.3, 4.4, 6.5_

- [x] 7. Final testing and documentation


  - [x] 7.1 Perform end-to-end testing


    - Test complete user workflow from profile creation to data export
    - Test import on fresh session
    - Test all CRUD operations for courses, assignments, grades
    - Test GPA calculations
    - Test data persistence across page navigation
    - Verify data loss on browser close (expected behavior)
    - _Requirements: All_

  - [x] 7.2 Update README documentation


    - Document new browser storage approach
    - Add instructions for export/import workflow
    - Add warning about data persistence
    - Add troubleshooting section
    - Update deployment instructions (no database needed)
    - _Requirements: All_

  - [x] 7.3 Create user guide for data management


    - Document how to export data regularly
    - Document how to import data on new device/browser
    - Document storage limitations
    - Document clear data functionality
    - Add best practices for data backup
    - _Requirements: 2.1, 2.2, 3.1, 3.2, 5.1, 6.1_
