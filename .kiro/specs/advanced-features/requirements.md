# Requirements Document

## Introduction

This feature focuses on advanced functionality improvements including department/course suggestions, customizable GPA calculation systems, dark mode fixes, and smart data entry features. The goal is to reduce manual data entry and provide a more personalized experience.

## Glossary

- **DERSLY_App**: The student support platform Streamlit application
- **Department_Catalog**: Pre-defined list of university departments
- **Course_Catalog**: Pre-defined list of common courses by department
- **GPA_System**: Grading system configuration (4.0, 5.0, letter grades, etc.)
- **Dark_Mode**: Dark color theme for the application
- **Smart_Suggestions**: Auto-complete and suggestion features
- **Grade_Scale**: Mapping between letter grades and numeric values

## Requirements

### Requirement 1: Department Catalog and Suggestions

**User Story:** As a user, I want to select my department from a list instead of typing it manually, so that I can avoid typos and save time.

#### Acceptance Criteria

1. THE DERSLY_App SHALL provide a pre-defined list of Turkish university departments
2. WHEN the user creates or edits a profile, THE DERSLY_App SHALL display department suggestions
3. THE DERSLY_App SHALL allow users to search/filter departments
4. THE DERSLY_App SHALL support both selecting from list and custom entry
5. THE DERSLY_App SHALL include at least 50 common departments
6. THE DERSLY_App SHALL organize departments by faculty (Mühendislik, Fen, Sosyal, etc.)

### Requirement 2: Course Catalog and Smart Suggestions

**User Story:** As a user, I want course suggestions based on my department, so that I don't have to type every course name and code manually.

#### Acceptance Criteria

1. THE DERSLY_App SHALL provide common course suggestions by department
2. WHEN the user adds a course, THE DERSLY_App SHALL suggest course names and codes
3. THE DERSLY_App SHALL allow auto-complete for course names
4. THE DERSLY_App SHALL suggest typical credit values for courses
5. THE DERSLY_App SHALL support custom course entry
6. THE DERSLY_App SHALL remember user's previously entered courses

### Requirement 3: Customizable GPA Calculation System

**User Story:** As a user, I want to configure the GPA calculation system to match my university's grading scale, so that my GPA is calculated correctly.

#### Acceptance Criteria

1. THE DERSLY_App SHALL support multiple GPA systems (4.0, 5.0, 7.0, 10.0)
2. THE DERSLY_App SHALL support both single-letter and double-letter grade systems
3. WHEN the user configures GPA system, THE DERSLY_App SHALL save the preference
4. THE DERSLY_App SHALL provide pre-defined grade scales for common systems
5. THE DERSLY_App SHALL allow custom grade scale configuration
6. THE DERSLY_App SHALL recalculate GPA when system changes
7. THE DERSLY_App SHALL display the current GPA system in use

### Requirement 4: Fix Dark Mode Styling

**User Story:** As a user, I want dark mode to display text and elements clearly, so that I can use the app comfortably in low-light conditions.

#### Acceptance Criteria

1. WHEN dark mode is active, THE DERSLY_App SHALL ensure all text is readable
2. THE DERSLY_App SHALL use appropriate contrast ratios in dark mode (WCAG AA)
3. THE DERSLY_App SHALL adjust card backgrounds for dark mode
4. THE DERSLY_App SHALL adjust button colors for dark mode
5. THE DERSLY_App SHALL adjust form input colors for dark mode
6. THE DERSLY_App SHALL ensure icons and emojis are visible in dark mode
7. THE DERSLY_App SHALL provide smooth transition between light and dark modes

### Requirement 5: Smart Course Time Suggestions

**User Story:** As a user, I want the app to suggest common course time slots, so that I can quickly set up my schedule.

#### Acceptance Criteria

1. THE DERSLY_App SHALL provide common time slot suggestions (09:00-10:30, 10:40-12:10, etc.)
2. WHEN the user selects a start time, THE DERSLY_App SHALL suggest appropriate end times
3. THE DERSLY_App SHALL detect time conflicts and warn the user
4. THE DERSLY_App SHALL suggest typical course durations (50min, 80min, 110min)
5. THE DERSLY_App SHALL remember user's preferred time slots

### Requirement 6: Grade Scale Configuration Interface

**User Story:** As a user, I want an easy interface to configure my university's grading scale, so that I can ensure accurate GPA calculations.

#### Acceptance Criteria

1. THE DERSLY_App SHALL provide a settings page for GPA configuration
2. WHEN the user accesses GPA settings, THE DERSLY_App SHALL show current scale
3. THE DERSLY_App SHALL provide templates for common Turkish universities
4. THE DERSLY_App SHALL allow editing grade-to-point mappings
5. THE DERSLY_App SHALL validate grade scale configurations
6. THE DERSLY_App SHALL show preview of GPA calculation with new scale

### Requirement 7: Quick Add Features

**User Story:** As a user, I want quick-add buttons for common tasks, so that I can add data faster.

#### Acceptance Criteria

1. THE DERSLY_App SHALL provide "Quick Add Course" with minimal fields
2. THE DERSLY_App SHALL provide "Quick Add Assignment" with minimal fields
3. THE DERSLY_App SHALL use smart defaults for optional fields
4. THE DERSLY_App SHALL allow expanding to full form if needed
5. THE DERSLY_App SHALL remember user's common patterns

### Requirement 8: Data Import from Common Formats

**User Story:** As a user, I want to import my course schedule from common formats, so that I don't have to enter everything manually.

#### Acceptance Criteria

1. THE DERSLY_App SHALL support importing courses from CSV
2. THE DERSLY_App SHALL support importing courses from Excel
3. THE DERSLY_App SHALL provide CSV/Excel templates
4. THE DERSLY_App SHALL validate imported data
5. THE DERSLY_App SHALL show preview before importing
6. THE DERSLY_App SHALL handle import errors gracefully

### Requirement 9: University Presets

**User Story:** As a user, I want to select my university and have the app configure itself automatically, so that I don't have to manually set up everything.

#### Acceptance Criteria

1. THE DERSLY_App SHALL provide presets for major Turkish universities
2. WHEN the user selects a university, THE DERSLY_App SHALL configure GPA system
3. THE DERSLY_App SHALL configure department list based on university
4. THE DERSLY_App SHALL configure common course catalog
5. THE DERSLY_App SHALL configure typical semester structure
6. THE DERSLY_App SHALL allow overriding preset values

### Requirement 10: Theme Toggle and Persistence

**User Story:** As a user, I want to toggle between light and dark modes and have my preference saved, so that I don't have to change it every time.

#### Acceptance Criteria

1. THE DERSLY_App SHALL provide a theme toggle button
2. WHEN the user toggles theme, THE DERSLY_App SHALL apply changes immediately
3. THE DERSLY_App SHALL save theme preference in browser storage
4. THE DERSLY_App SHALL remember theme preference across sessions
5. THE DERSLY_App SHALL detect system theme preference as default
6. THE DERSLY_App SHALL provide smooth transition animation
