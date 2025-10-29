# Implementation Plan

- [x] 1. Set up project structure and dependencies



  - Create directory structure (database/, utils/, components/, pages/)
  - Create requirements.txt with all dependencies (streamlit, sqlalchemy, pymysql, bcrypt)
  - Create .streamlit/config.toml for Streamlit configuration
  - Create config.py for environment variables
  - _Requirements: 1.1, 1.2, 8.1_



- [ ] 2. Implement database layer with SQLAlchemy ORM
  - [ ] 2.1 Create database connection module
    - Write database/connection.py with SQLAlchemy engine setup
    - Implement connection pooling configuration
    - Add error handling for connection failures
    - _Requirements: 8.1, 8.3, 8.4, 8.5_
  
  - [x] 2.2 Define ORM models matching existing schema


    - Create database/models.py with User, Course, Assignment, Reminder, GradeEntry models
    - Define relationships between models
    - Add table mappings for existing MySQL/TiDB schema
    - _Requirements: 1.2, 8.2, 8.5_
  
  - [x] 2.3 Implement CRUD operations


    - Create database/operations.py with DatabaseOperations class
    - Implement user operations (create, get_by_email, update)
    - Implement course operations (create, get_user_courses, update, delete)
    - Implement assignment operations (create, get_user_assignments, update, delete)
    - Implement reminder operations (create, get_user_reminders, update)
    - Implement grade operations (create, get_user_grades, delete)
    - _Requirements: 8.2, 8.4_
  
  - [x] 2.4 Write unit tests for database operations


    - Create tests/test_database.py
    - Test CRUD operations for each model
    - Test error handling and transaction rollback
    - _Requirements: 8.2, 8.4_

- [ ] 3. Implement authentication system
  - [x] 3.1 Create authentication utilities


    - Write utils/auth.py with AuthManager class
    - Implement password hashing with bcrypt
    - Implement password verification
    - Implement login function with database lookup
    - Implement logout function to clear session
    - Implement is_authenticated and get_current_user helpers
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_
  
  - [x] 3.2 Create login page


    - Create app.py as main entry point
    - Implement login form with email and password fields
    - Add form validation
    - Handle authentication success/failure with appropriate messages
    - Store user data in session_state on successful login
    - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5_
  
  - [x] 3.3 Write unit tests for authentication


    - Create tests/test_auth.py
    - Test password hashing and verification
    - Test login with valid and invalid credentials
    - Test session state management
    - _Requirements: 2.1, 2.2, 2.5_

- [ ] 4. Create utility modules
  - [x] 4.1 Implement GPA calculation utilities


    - Create utils/calculations.py
    - Implement calculate_gno function for semester GPA
    - Implement calculate_dno function for cumulative GPA
    - Add validation for grade values (0-4 range)
    - _Requirements: 5.1, 5.2, 5.4, 5.5_
  
  - [x] 4.2 Implement input validation utilities


    - Create utils/validators.py
    - Implement validate_course_data function
    - Implement validate_assignment_data function
    - Implement validate_grade_data function
    - Add field-level validation with error messages
    - _Requirements: 3.2, 4.2, 5.5_
  
  - [x] 4.3 Write unit tests for calculations


    - Create tests/test_calculations.py
    - Test GNO calculation with various grade combinations
    - Test DNO calculation across semesters
    - Test edge cases (no grades, invalid values)
    - _Requirements: 5.1, 5.2, 5.4, 5.5_

- [ ] 5. Build reusable UI components
  - [x] 5.1 Create course card component


    - Create components/course_card.py
    - Implement display_course_card function with color-coded styling
    - Add edit and delete action buttons
    - _Requirements: 3.1, 3.3, 3.4_
  

  - [x] 5.2 Create assignment card component

    - Create components/assignment_card.py
    - Implement display_assignment_card function with status badge
    - Add due date countdown display
    - Add priority indicator
    - Add complete, edit, and delete actions
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5_
  

  - [x] 5.3 Create statistics widget component


    - Create components/stats_widget.py
    - Implement display_stat_widget function with metric display
    - Add icons and trend indicators
    - Add clickable navigation
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [x] 6. Implement Home page


  - Create pages/1_🏠_Home.py
  - Add authentication check at page start
  - Display dashboard statistics (total courses, pending assignments, active reminders)
  - Display current GNO and DNO values
  - Add quick navigation cards to other sections
  - Display upcoming assignments widget
  - Implement data caching for performance
  - _Requirements: 1.1, 1.3, 2.3, 9.1, 9.2, 9.4, 10.1, 10.2, 10.3, 10.4, 10.5_

- [ ] 7. Implement Courses page
  - [x] 7.1 Create course list and weekly schedule view


    - Create pages/2_📚_Courses.py
    - Add authentication check
    - Fetch user courses from database
    - Display courses in weekly schedule grid (organized by day and time)
    - Display course list with filtering options
    - Use course_card component for display
    - _Requirements: 1.1, 1.3, 3.1, 3.3, 3.4_
  

  - [ ] 7.2 Implement add/edit course functionality
    - Create add course form with fields (name, code, day, time, color, credits)
    - Implement form validation using validators
    - Add color picker for course visualization
    - Create edit course form with pre-filled data
    - Handle form submission with database operations
    - Display success/error messages
    - _Requirements: 3.1, 3.2, 3.4, 3.5_

  
  - [ ] 7.3 Implement delete course functionality
    - Add delete confirmation dialog
    - Handle course deletion with database operation
    - Refresh course list after deletion
    - _Requirements: 3.1, 3.5_

- [ ] 8. Implement Assignments page
  - [x] 8.1 Create assignment list with filtering


    - Create pages/3_📝_Assignments.py
    - Add authentication check
    - Fetch user assignments from database
    - Display assignments sorted by due date
    - Implement filters (type, status, date range)
    - Use assignment_card component for display
    - Add visual warnings for approaching deadlines
    - _Requirements: 1.1, 1.3, 4.1, 4.2, 4.4, 4.5_
  

  - [ ] 8.2 Implement add/edit assignment functionality
    - Create add assignment form (title, description, type, due date, course link, priority)
    - Implement form validation
    - Create edit assignment form with pre-filled data
    - Handle form submission with database operations
    - Display success/error messages
    - _Requirements: 4.1, 4.2_

  
  - [ ] 8.3 Implement assignment status management
    - Add status toggle button (pending/completed)
    - Update assignment status in database
    - Refresh assignment list after status change
    - _Requirements: 4.3_

  
  - [ ] 8.4 Implement delete assignment functionality
    - Add delete confirmation dialog
    - Handle assignment deletion with database operation
    - Refresh assignment list after deletion
    - _Requirements: 4.1_

- [ ] 9. Implement GPA page
  - [x] 9.1 Create grade entry display


    - Create pages/6_📊_GPA.py
    - Add authentication check
    - Fetch user grade entries from database
    - Display grades grouped by semester
    - Show course name, grade, and credits for each entry
    - _Requirements: 1.1, 1.3, 5.3_
  

  - [ ] 9.2 Implement GPA calculations and display
    - Calculate GNO for each semester using calculations utility
    - Calculate overall DNO using calculations utility
    - Display GNO and DNO prominently
    - Add grade visualization (charts using Streamlit charts)
    - _Requirements: 5.1, 5.2, 5.4_
  

  - [ ] 9.3 Implement add/edit grade entry functionality
    - Create add grade form (course name, grade, credits, semester, year)
    - Implement grade validation (0-4 range)
    - Create edit grade form with pre-filled data
    - Handle form submission with database operations
    - Recalculate GNO and DNO automatically after changes
    - _Requirements: 5.4, 5.5_
  

  - [ ] 9.4 Implement delete grade entry functionality
    - Add delete confirmation dialog
    - Handle grade deletion with database operation
    - Recalculate GNO and DNO after deletion
    - _Requirements: 5.4_

- [ ] 10. Implement Reminders page
  - [x] 10.1 Create reminder list display

    - Create pages/5_🔔_Reminders.py
    - Add authentication check
    - Fetch user reminders from database
    - Display active reminders sorted by date and time
    - Show linked assignment information
    - _Requirements: 1.1, 1.3, 6.2_
  

  - [ ] 10.2 Implement add reminder functionality
    - Create add reminder form (assignment link, date, time, type)
    - Implement form validation
    - Handle form submission with database operations
    - Display success/error messages
    - _Requirements: 6.1, 6.4_
  

  - [ ] 10.3 Implement reminder status management
    - Add mark as sent button
    - Add mark as inactive button
    - Update reminder status in database
    - Refresh reminder list after status change
    - _Requirements: 6.3_


- [ ] 11. Implement Calendar page
  - Create pages/4_📅_Calendar.py
  - Add authentication check
  - Fetch assignments and exams from database
  - Display monthly calendar view with assignment markers
  - Implement day detail view showing assignments for selected day
  - Add navigation between months
  - _Requirements: 1.1, 1.3_


- [ ] 12. Implement Profile page
  - [ ] 12.1 Create profile information display
    - Create pages/7_👤_Profile.py
    - Add authentication check
    - Display user information (name, email, student ID, department, class year)
    - Display current GNO and DNO values
    - Show account statistics
    - _Requirements: 1.1, 1.3, 7.1, 7.4, 7.5_

  
  - [ ] 12.2 Implement edit profile functionality
    - Create edit profile form with pre-filled data
    - Implement form validation
    - Handle form submission with database operations
    - Display success/error messages
    - _Requirements: 7.2, 7.3_

- [x] 13. Implement performance optimizations

  - Add caching decorators to frequently accessed data functions
  - Implement loading indicators for all data fetch operations
  - Optimize database queries to minimize round trips
  - Configure session state management to prevent unnecessary reruns
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_


- [ ] 14. Add error handling and user feedback
  - Implement try-catch blocks for all database operations
  - Add user-friendly error messages in Turkish
  - Implement authentication error handling with redirects
  - Add validation error messages for all forms
  - Implement graceful handling of database connection errors
  - _Requirements: 8.4, 9.4_


- [x] 15. Configure deployment settings

  - Create .env.example file with required environment variables
  - Update .streamlit/config.toml with production settings
  - Create README.md with setup and deployment instructions
  - Document database schema requirements
  - Add deployment guide for Streamlit Cloud
  - _Requirements: 1.1, 1.2_

- [x] 16. Conduct integration testing

  - [ ] 16.1 Create integration test suite
    - Create tests/test_pages.py
    - Test page rendering with authenticated user
    - Test form submissions across all pages
    - Test navigation between pages
    - Test data persistence across page changes
    - _Requirements: 1.1, 1.3, 1.5_


  
  - [ ] 16.2 Test with production-like data
    - Create test database with sample data
    - Test all CRUD operations with realistic data
    - Verify GPA calculations with multiple semesters
    - Test assignment filtering and sorting
    - Validate reminder creation and management
    - _Requirements: 1.2, 8.5_
