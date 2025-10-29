# Requirements Document

## Introduction

Bu doküman, mevcut React/PWA tabanlı DERSLY üniversite öğrenci destek platformunun Streamlit framework'üne dönüştürülmesi için gereksinimleri tanımlar. Platform, öğrencilerin ders programlarını yönetmelerine, ödev ve sınavları takip etmelerine, not ortalamalarını hesaplamalarına ve hatırlatıcılar almalarına olanak tanır. Dönüşüm, mevcut tüm özellikleri koruyarak Streamlit'in basit ve hızlı web uygulama geliştirme yeteneklerinden fararlanmayı amaçlar.

## Glossary

- **Streamlit Application**: Python tabanlı web uygulama framework'ü kullanılarak oluşturulan sistem
- **User Session**: Streamlit'in session_state mekanizması ile yönetilen kullanıcı oturumu
- **Database Layer**: MySQL/TiDB veritabanı ile etkileşim için Python ORM katmanı
- **Page Component**: Streamlit'te her bir ana özellik için ayrı sayfa modülü
- **GNO**: Dönem Not Ortalaması (Grade Point Average)
- **DNO**: Genel Not Ortalaması (Cumulative GPA)
- **Authentication System**: Kullanıcı kimlik doğrulama ve yetkilendirme sistemi

## Requirements

### Requirement 1

**User Story:** Bir öğrenci olarak, mevcut tüm özelliklerime Streamlit tabanlı bir arayüzden erişebilmek istiyorum, böylece Python ekosisteminin avantajlarından faydalanabilirim.

#### Acceptance Criteria

1. THE Streamlit Application SHALL provide all functional features present in the original React application
2. THE Streamlit Application SHALL maintain data compatibility with the existing MySQL/TiDB database schema
3. THE Streamlit Application SHALL support multi-page navigation for Home, Courses, Assignments, Calendar, Reminders, GPA, and Profile sections
4. THE Streamlit Application SHALL render responsive layouts that adapt to different screen sizes
5. THE Streamlit Application SHALL maintain session state across page navigations

### Requirement 2

**User Story:** Bir öğrenci olarak, güvenli bir şekilde giriş yapabilmek ve verilerimin korunduğundan emin olmak istiyorum.

#### Acceptance Criteria

1. THE Authentication System SHALL provide secure user login functionality
2. THE Authentication System SHALL store user credentials securely in the database
3. WHEN a user attempts to access protected pages, THE Streamlit Application SHALL verify authentication status
4. IF a user is not authenticated, THEN THE Streamlit Application SHALL redirect to the login page
5. THE Authentication System SHALL maintain user session data using Streamlit's session_state

### Requirement 3

**User Story:** Bir öğrenci olarak, derslerimi ekleyip yönetebilmek istiyorum, böylece haftalık programımı takip edebilirim.

#### Acceptance Criteria

1. THE Streamlit Application SHALL display a course management interface with add, edit, and delete operations
2. WHEN a user adds a new course, THE Streamlit Application SHALL validate required fields (course name, code, day, time)
3. THE Streamlit Application SHALL display courses in a weekly schedule view organized by day and time
4. THE Streamlit Application SHALL allow users to assign colors to courses for visual distinction
5. THE Database Layer SHALL persist all course data to the courses table

### Requirement 4

**User Story:** Bir öğrenci olarak, ödev ve sınavlarımı takip edebilmek istiyorum, böylece son teslim tarihlerini kaçırmam.

#### Acceptance Criteria

1. THE Streamlit Application SHALL provide an assignment management interface supporting assignments, exams, projects, and quizzes
2. THE Streamlit Application SHALL display assignments sorted by due date with status indicators
3. WHEN a user marks an assignment as completed, THE Streamlit Application SHALL update the status in the database
4. THE Streamlit Application SHALL allow filtering assignments by type and status
5. THE Streamlit Application SHALL display upcoming assignments with visual warnings for approaching deadlines

### Requirement 5

**User Story:** Bir öğrenci olarak, not ortalamalarımı hesaplayabilmek istiyorum, böylece akademik performansımı izleyebilirim.

#### Acceptance Criteria

1. THE Streamlit Application SHALL calculate GNO (semester GPA) based on course grades and credits
2. THE Streamlit Application SHALL calculate DNO (cumulative GPA) across all semesters
3. THE Streamlit Application SHALL display grade entries grouped by semester
4. WHEN a user adds a new grade entry, THE Streamlit Application SHALL recalculate GNO and DNO automatically
5. THE Streamlit Application SHALL validate grade values to be between 0 and 4

### Requirement 6

**User Story:** Bir öğrenci olarak, hatırlatıcılar oluşturabilmek istiyorum, böylece önemli tarihleri unutmam.

#### Acceptance Criteria

1. THE Streamlit Application SHALL provide a reminder creation interface linked to assignments or courses
2. THE Streamlit Application SHALL display active reminders sorted by date and time
3. THE Streamlit Application SHALL allow users to mark reminders as sent or inactive
4. THE Streamlit Application SHALL support different reminder types (notification, email, push)
5. THE Database Layer SHALL store reminder data with proper associations to assignments and courses

### Requirement 7

**User Story:** Bir öğrenci olarak, profil bilgilerimi görüntüleyip güncelleyebilmek istiyorum.

#### Acceptance Criteria

1. THE Streamlit Application SHALL display user profile information including student ID, department, and class year
2. THE Streamlit Application SHALL allow users to edit profile fields
3. WHEN a user updates profile information, THE Streamlit Application SHALL validate and save changes to the database
4. THE Streamlit Application SHALL display current GNO and DNO values on the profile page
5. THE Streamlit Application SHALL show account information including name and email

### Requirement 8

**User Story:** Bir geliştirici olarak, veritabanı işlemlerini Python ile yönetebilmek istiyorum, böylece mevcut şemayı kullanabilirim.

#### Acceptance Criteria

1. THE Database Layer SHALL use SQLAlchemy or similar Python ORM for database operations
2. THE Database Layer SHALL implement all CRUD operations for users, courses, assignments, reminders, and grade entries
3. THE Database Layer SHALL maintain connection pooling for efficient database access
4. THE Database Layer SHALL handle database errors gracefully with appropriate error messages
5. THE Database Layer SHALL support the existing MySQL/TiDB schema without modifications

### Requirement 9

**User Story:** Bir kullanıcı olarak, uygulamanın hızlı ve responsive olmasını istiyorum.

#### Acceptance Criteria

1. THE Streamlit Application SHALL load pages within 2 seconds under normal network conditions
2. THE Streamlit Application SHALL use caching mechanisms for frequently accessed data
3. THE Streamlit Application SHALL minimize unnecessary database queries through efficient state management
4. THE Streamlit Application SHALL provide loading indicators during data fetch operations
5. THE Streamlit Application SHALL handle concurrent user sessions without performance degradation

### Requirement 10

**User Story:** Bir öğrenci olarak, ana sayfada genel istatistiklerimi ve yaklaşan görevlerimi görebilmek istiyorum.

#### Acceptance Criteria

1. THE Streamlit Application SHALL display total course count on the home page
2. THE Streamlit Application SHALL display pending assignments and exams count
3. THE Streamlit Application SHALL display active reminders count
4. THE Streamlit Application SHALL display current GNO and DNO values
5. THE Streamlit Application SHALL provide quick navigation links to detailed sections
