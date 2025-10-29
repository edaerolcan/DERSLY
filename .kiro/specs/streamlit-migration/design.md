# Design Document

## Overview

Bu doküman, DERSLY platformunun React/PWA mimarisinden Streamlit tabanlı Python web uygulamasına dönüşümü için teknik tasarımı tanımlar. Streamlit'in deklaratif ve basit yapısı kullanılarak, mevcut tüm özellikler korunacak ve Python ekosisteminin avantajlarından faydalanılacaktır.

### Technology Stack

- **Frontend Framework**: Streamlit 1.30+
- **Backend Language**: Python 3.10+
- **Database**: MySQL/TiDB (mevcut şema korunacak)
- **ORM**: SQLAlchemy 2.0+
- **Authentication**: Custom session-based auth with bcrypt
- **State Management**: Streamlit session_state
- **Styling**: Streamlit native components + custom CSS

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Streamlit Application                  │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Multi-Page Navigation                 │  │
│  │  Home | Courses | Assignments | GPA | Profile     │  │
│  └───────────────────────────────────────────────────┘  │
│                          │                               │
│  ┌───────────────────────▼───────────────────────────┐  │
│  │           Session State Management                 │  │
│  │  - User authentication                             │  │
│  │  - Form states                                     │  │
│  │  - Cache management                                │  │
│  └───────────────────────┬───────────────────────────┘  │
│                          │                               │
│  ┌───────────────────────▼───────────────────────────┐  │
│  │            Business Logic Layer                    │  │
│  │  - Course management                               │  │
│  │  - Assignment tracking                             │  │
│  │  - GPA calculations                                │  │
│  │  - Reminder management                             │  │
│  └───────────────────────┬───────────────────────────┘  │
│                          │                               │
│  ┌───────────────────────▼───────────────────────────┐  │
│  │         Database Access Layer (SQLAlchemy)         │  │
│  │  - ORM Models                                      │  │
│  │  - CRUD Operations                                 │  │
│  │  - Connection pooling                              │  │
│  └───────────────────────┬───────────────────────────┘  │
│                          │                               │
│  ┌───────────────────────▼───────────────────────────┐  │
│                  MySQL/TiDB Database                    │
│  - users, courses, assignments, reminders, grades       │
└─────────────────────────────────────────────────────────┘
```

### Directory Structure

```
dersly-streamlit/
├── app.py                      # Ana Streamlit entry point
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── pages/                     # Streamlit multi-page structure
│   ├── 1_🏠_Home.py
│   ├── 2_📚_Courses.py
│   ├── 3_📝_Assignments.py
│   ├── 4_📅_Calendar.py
│   ├── 5_🔔_Reminders.py
│   ├── 6_📊_GPA.py
│   └── 7_👤_Profile.py
├── database/
│   ├── __init__.py
│   ├── connection.py          # Database connection setup
│   ├── models.py              # SQLAlchemy ORM models
│   └── operations.py          # CRUD operations
├── utils/
│   ├── __init__.py
│   ├── auth.py                # Authentication utilities
│   ├── calculations.py        # GPA calculation logic
│   └── validators.py          # Input validation
└── components/
    ├── __init__.py
    ├── course_card.py         # Reusable course display
    ├── assignment_card.py     # Reusable assignment display
    └── stats_widget.py        # Dashboard statistics
```

## Components and Interfaces

### 1. Authentication System

**Module**: `utils/auth.py`

```python
class AuthManager:
    """Handles user authentication and session management"""
    
    @staticmethod
    def login(email: str, password: str) -> Optional[User]
        """Authenticate user and return user object"""
    
    @staticmethod
    def logout() -> None:
        """Clear session state"""
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is logged in"""
    
    @staticmethod
    def get_current_user() -> Optional[User]:
        """Get current logged-in user from session"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash password using bcrypt"""
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        """Verify password against hash"""
```

**Session State Keys**:
- `authenticated`: bool
- `user_id`: int
- `user_email`: str
- `user_name`: str

### 2. Database Layer

**Module**: `database/models.py`

SQLAlchemy ORM models matching existing schema:

```python
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password_hash = Column(String(255))
    student_id = Column(String(50))
    department = Column(String(100))
    class_year = Column(Integer)
    created_at = Column(DateTime)

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_name = Column(String(200))
    course_code = Column(String(50))
    day = Column(String(20))
    start_time = Column(Time)
    end_time = Column(Time)
    color = Column(String(7))
    credits = Column(Integer)

class Assignment(Base):
    __tablename__ = 'assignments'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_id = Column(Integer, ForeignKey('courses.id'))
    title = Column(String(200))
    description = Column(Text)
    type = Column(String(50))  # assignment, exam, project, quiz
    due_date = Column(DateTime)
    status = Column(String(20))  # pending, completed
    priority = Column(String(20))

class Reminder(Base):
    __tablename__ = 'reminders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    assignment_id = Column(Integer, ForeignKey('assignments.id'))
    reminder_date = Column(DateTime)
    reminder_type = Column(String(50))
    is_sent = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)

class GradeEntry(Base):
    __tablename__ = 'grade_entries'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    course_name = Column(String(200))
    grade = Column(Float)
    credits = Column(Integer)
    semester = Column(String(50))
    year = Column(Integer)
```

**Module**: `database/operations.py`

```python
class DatabaseOperations:
    """CRUD operations for all entities"""
    
    # User operations
    def create_user(user_data: dict) -> User
    def get_user_by_email(email: str) -> Optional[User]
    def update_user(user_id: int, updates: dict) -> bool
    
    # Course operations
    def create_course(course_data: dict) -> Course
    def get_user_courses(user_id: int) -> List[Course]
    def update_course(course_id: int, updates: dict) -> bool
    def delete_course(course_id: int) -> bool
    
    # Assignment operations
    def create_assignment(assignment_data: dict) -> Assignment
    def get_user_assignments(user_id: int, filters: dict) -> List[Assignment]
    def update_assignment(assignment_id: int, updates: dict) -> bool
    def delete_assignment(assignment_id: int) -> bool
    
    # Reminder operations
    def create_reminder(reminder_data: dict) -> Reminder
    def get_user_reminders(user_id: int) -> List[Reminder]
    def update_reminder(reminder_id: int, updates: dict) -> bool
    
    # Grade operations
    def create_grade_entry(grade_data: dict) -> GradeEntry
    def get_user_grades(user_id: int) -> List[GradeEntry]
    def delete_grade_entry(grade_id: int) -> bool
```

### 3. Page Components

**Home Page** (`pages/1_🏠_Home.py`):
- Dashboard with statistics (total courses, pending assignments, active reminders)
- Current GNO/DNO display
- Quick navigation cards
- Upcoming assignments widget

**Courses Page** (`pages/2_📚_Courses.py`):
- Weekly schedule view (grid layout by day/time)
- Add/Edit/Delete course forms
- Color picker for course visualization
- Course list with filtering

**Assignments Page** (`pages/3_📝_Assignments.py`):
- Assignment list with filters (type, status, date range)
- Add/Edit assignment forms
- Status toggle (pending/completed)
- Due date warnings
- Link to course

**Calendar Page** (`pages/4_📅_Calendar.py`):
- Monthly calendar view showing assignments and exams
- Day detail view
- Integration with assignments data

**Reminders Page** (`pages/5_🔔_Reminders.py`):
- Active reminders list
- Create reminder form linked to assignments
- Mark as sent/inactive
- Reminder type selection

**GPA Page** (`pages/6_📊_GPA.py`):
- Semester-based grade entry
- GNO calculation per semester
- DNO calculation across all semesters
- Grade visualization (charts)
- Add/Edit/Delete grade entries

**Profile Page** (`pages/7_👤_Profile.py`):
- User information display
- Edit profile form
- Account statistics
- Password change functionality

### 4. Reusable Components

**Module**: `components/course_card.py`
- Display course information in card format
- Color-coded visual representation
- Edit/Delete actions

**Module**: `components/assignment_card.py`
- Display assignment with status badge
- Due date with countdown
- Priority indicator
- Complete/Edit/Delete actions

**Module**: `components/stats_widget.py`
- Metric display with icons
- Trend indicators
- Clickable navigation

## Data Models

### User Data Flow

```
Login Form → AuthManager.login() → DatabaseOperations.get_user_by_email()
    ↓
Session State (user_id, email, name)
    ↓
All Pages (access via st.session_state)
```

### Course Management Flow

```
Course Form → Validation → DatabaseOperations.create_course()
    ↓
Database (courses table)
    ↓
DatabaseOperations.get_user_courses() → Course Display
```

### GPA Calculation Flow

```
Grade Entries (by semester) → calculations.calculate_gno()
    ↓
All Grade Entries → calculations.calculate_dno()
    ↓
Display on GPA Page and Home Dashboard
```

## Error Handling

### Database Errors

```python
try:
    # Database operation
    result = db_operations.create_course(data)
except SQLAlchemyError as e:
    st.error("Veritabanı hatası: İşlem gerçekleştirilemedi")
    logger.error(f"Database error: {str(e)}")
except Exception as e:
    st.error("Beklenmeyen bir hata oluştu")
    logger.error(f"Unexpected error: {str(e)}")
```

### Authentication Errors

```python
if not AuthManager.is_authenticated():
    st.warning("Bu sayfayı görüntülemek için giriş yapmalısınız")
    st.stop()
```

### Validation Errors

```python
def validate_course_data(data: dict) -> Tuple[bool, str]:
    if not data.get('course_name'):
        return False, "Ders adı gereklidir"
    if not data.get('course_code'):
        return False, "Ders kodu gereklidir"
    # ... more validations
    return True, ""
```

### User-Friendly Error Messages

- Database errors: "Veritabanı bağlantı hatası. Lütfen tekrar deneyin."
- Validation errors: Specific field-level messages
- Authentication errors: "Oturum süreniz doldu. Lütfen tekrar giriş yapın."
- Not found errors: "İstenen kayıt bulunamadı."

## Testing Strategy

### Unit Tests

**Module**: `tests/test_auth.py`
- Test password hashing and verification
- Test login with valid/invalid credentials
- Test session state management

**Module**: `tests/test_calculations.py`
- Test GNO calculation with various grade combinations
- Test DNO calculation across semesters
- Test edge cases (no grades, invalid values)

**Module**: `tests/test_database.py`
- Test CRUD operations for each model
- Test database connection handling
- Test transaction rollback on errors

### Integration Tests

**Module**: `tests/test_pages.py`
- Test page rendering with authenticated user
- Test form submissions
- Test navigation between pages
- Test data persistence across page changes

### Testing Approach

1. Use pytest for test framework
2. Mock database connections for unit tests
3. Use test database for integration tests
4. Test with sample data matching production schema
5. Validate Streamlit component rendering
6. Test session state persistence

### Test Data

```python
# Sample test user
test_user = {
    'name': 'Test Student',
    'email': 'test@university.edu',
    'password': 'TestPass123',
    'student_id': '2020123456',
    'department': 'Computer Engineering',
    'class_year': 3
}

# Sample test course
test_course = {
    'course_name': 'Data Structures',
    'course_code': 'CS201',
    'day': 'Monday',
    'start_time': '09:00',
    'end_time': '11:00',
    'color': '#FF5733',
    'credits': 4
}
```

## Performance Considerations

### Caching Strategy

```python
@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_user_courses(user_id: int):
    return DatabaseOperations.get_user_courses(user_id)

@st.cache_resource
def get_database_connection():
    return create_engine(DATABASE_URL, pool_size=10)
```

### Database Optimization

- Use connection pooling (SQLAlchemy pool_size=10)
- Index frequently queried columns (user_id, due_date, semester)
- Lazy loading for relationships
- Batch operations where possible

### Session State Management

- Store only essential user data in session state
- Clear unused session keys
- Minimize session state updates to prevent reruns

### Loading Indicators

```python
with st.spinner('Veriler yükleniyor...'):
    courses = get_user_courses(user_id)
```

## Security Considerations

### Password Security

- Use bcrypt for password hashing (cost factor: 12)
- Never store plain text passwords
- Implement password strength requirements

### SQL Injection Prevention

- Use SQLAlchemy ORM (parameterized queries)
- Validate all user inputs
- Sanitize data before database operations

### Session Security

- Use Streamlit's built-in session management
- Implement session timeout (30 minutes)
- Clear sensitive data on logout

### Input Validation

- Validate all form inputs on server side
- Sanitize HTML/JavaScript in text fields
- Limit file upload sizes and types (if applicable)

## Deployment Considerations

### Environment Configuration

```python
# config.py
import os

DATABASE_URL = os.getenv('DATABASE_URL', 'mysql://localhost/dersly')
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

### Streamlit Configuration

`.streamlit/config.toml`:
```toml
[theme]
primaryColor = "#FF5733"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 5
```

### Requirements

```
streamlit>=1.30.0
sqlalchemy>=2.0.0
pymysql>=1.1.0
bcrypt>=4.0.0
python-dotenv>=1.0.0
pandas>=2.0.0
```

### Deployment Options

1. **Local Development**: `streamlit run app.py`
2. **Streamlit Cloud**: Direct GitHub integration
3. **Docker**: Containerized deployment
4. **Cloud Platforms**: AWS, Azure, GCP with Streamlit

## Migration Strategy

### Phase 1: Database Setup
- Verify existing MySQL/TiDB schema
- Create SQLAlchemy models matching schema
- Test database connections

### Phase 2: Core Features
- Implement authentication system
- Build database operations layer
- Create home page with dashboard

### Phase 3: Feature Pages
- Implement courses page
- Implement assignments page
- Implement GPA page

### Phase 4: Additional Features
- Implement reminders page
- Implement calendar page
- Implement profile page

### Phase 5: Testing & Refinement
- Conduct integration testing
- Performance optimization
- UI/UX improvements

### Data Migration

- No data migration needed (using existing database)
- Verify data compatibility
- Test with production data subset

## Future Enhancements

- Email notifications for reminders
- Export data to PDF/Excel
- Mobile-responsive improvements
- Dark mode support
- Multi-language support (Turkish/English)
- Integration with university systems
- Collaborative features (study groups)
