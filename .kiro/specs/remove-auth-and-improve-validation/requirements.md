# Requirements Document

## Introduction

This feature focuses on two critical improvements to the DERSLY application:
1. Removing unnecessary authentication/profile checks that prevent users from using the app
2. Implementing comprehensive input validation to prevent invalid data from entering the system

The current system requires profile creation before accessing any features, which is unnecessary since the app works entirely in browser storage. Additionally, the app lacks robust validation, allowing users to enter nonsensical data (negative credits, invalid time ranges, empty strings, etc.) that can break functionality.

## Glossary

- **DERSLY_App**: The student support platform Streamlit application
- **Browser_Storage**: Client-side data storage mechanism using Streamlit session state
- **Profile_Check**: Authentication mechanism that verifies user profile existence before allowing page access
- **Input_Validation**: Process of verifying user input meets expected format, type, and business rules before storage
- **Course_Entity**: Data structure representing a university course with code, name, schedule, and credits
- **Assignment_Entity**: Data structure representing student tasks (homework, exams, projects, quizzes)
- **User_Input_Form**: Streamlit form component accepting user data entry

## Requirements

### Requirement 1: Remove Authentication Barriers

**User Story:** As a user, I want to access all DERSLY features immediately without creating a profile, so that I can start using the app without unnecessary steps.

#### Acceptance Criteria

1. WHEN the user navigates to any page, THE DERSLY_App SHALL display the page content without requiring profile existence
2. THE DERSLY_App SHALL remove all profile existence checks from page files
3. THE DERSLY_App SHALL make profile creation optional and accessible only from the profile page
4. THE DERSLY_App SHALL continue to function correctly when no profile exists in Browser_Storage
5. WHERE a profile exists, THE DERSLY_App SHALL display profile information in the sidebar

### Requirement 2: Validate Course Input Data

**User Story:** As a user, I want the system to prevent me from entering invalid course data, so that my course schedule remains accurate and functional.

#### Acceptance Criteria

1. WHEN the user submits a course form, THE DERSLY_App SHALL verify the course name contains at least 2 characters
2. WHEN the user submits a course form, THE DERSLY_App SHALL verify the course code contains at least 2 characters and matches academic format patterns
3. WHEN the user submits a course form, THE DERSLY_App SHALL verify the start time occurs before the end time
4. WHEN the user submits a course form, THE DERSLY_App SHALL verify the credit value is between 1 and 15
5. WHEN the user submits a course form, THE DERSLY_App SHALL verify the time duration is at least 30 minutes
6. IF the user enters invalid course data, THEN THE DERSLY_App SHALL display a specific error message explaining the validation failure
7. THE DERSLY_App SHALL prevent submission of course forms containing invalid data

### Requirement 3: Validate Assignment Input Data

**User Story:** As a user, I want the system to prevent me from entering invalid assignment data, so that my task tracking remains reliable and deadlines are meaningful.

#### Acceptance Criteria

1. WHEN the user submits an assignment form, THE DERSLY_App SHALL verify the title contains at least 3 characters
2. WHEN the user submits an assignment form, THE DERSLY_App SHALL verify the title does not exceed 200 characters
3. WHEN the user submits an assignment form, THE DERSLY_App SHALL verify the due date is not more than 2 years in the future
4. WHEN the user submits an assignment form, THE DERSLY_App SHALL verify the description does not exceed 2000 characters
5. IF the user enters a due date in the past, THEN THE DERSLY_App SHALL display a warning but allow submission
6. IF the user enters invalid assignment data, THEN THE DERSLY_App SHALL display a specific error message explaining the validation failure
7. THE DERSLY_App SHALL prevent submission of assignment forms containing invalid data

### Requirement 4: Validate Grade Input Data

**User Story:** As a user, I want the system to prevent me from entering invalid grade data, so that my GPA calculations are accurate and meaningful.

#### Acceptance Criteria

1. WHEN the user submits a grade form, THE DERSLY_App SHALL verify the grade value is between 0.0 and 4.0
2. WHEN the user submits a grade form, THE DERSLY_App SHALL verify the letter grade matches valid options (AA, BA, BB, CB, CC, DC, DD, FD, FF)
3. WHEN the user submits a grade form, THE DERSLY_App SHALL verify the credit value is between 1 and 15
4. IF the user enters invalid grade data, THEN THE DERSLY_App SHALL display a specific error message explaining the validation failure
5. THE DERSLY_App SHALL prevent submission of grade forms containing invalid data

### Requirement 5: Validate Profile Input Data

**User Story:** As a user, I want the system to validate my profile information when I choose to create one, so that my profile data is properly formatted.

#### Acceptance Criteria

1. WHEN the user submits a profile form, THE DERSLY_App SHALL verify the name contains at least 2 characters
2. WHEN the user submits a profile form, THE DERSLY_App SHALL verify the email matches standard email format patterns
3. WHEN the user submits a profile form, THE DERSLY_App SHALL verify the student ID contains only alphanumeric characters
4. WHEN the user submits a profile form, THE DERSLY_App SHALL verify the class year is between 1 and 8
5. IF the user enters invalid profile data, THEN THE DERSLY_App SHALL display a specific error message explaining the validation failure
6. THE DERSLY_App SHALL prevent submission of profile forms containing invalid data

### Requirement 6: Provide User-Friendly Validation Feedback

**User Story:** As a user, I want to receive clear and helpful error messages when my input is invalid, so that I understand what needs to be corrected.

#### Acceptance Criteria

1. WHEN validation fails, THE DERSLY_App SHALL display error messages in Turkish language
2. WHEN validation fails, THE DERSLY_App SHALL display error messages with appropriate emoji icons for visual clarity
3. WHEN validation fails, THE DERSLY_App SHALL display error messages that specify exactly what is wrong
4. WHEN validation fails, THE DERSLY_App SHALL display error messages that suggest how to fix the issue
5. THE DERSLY_App SHALL display validation errors immediately upon form submission
6. THE DERSLY_App SHALL maintain user-entered data in the form when validation fails
