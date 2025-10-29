# Requirements Document

## Introduction

Bu özellik, DERSLY uygulamasının veri depolama mimarisini veritabanı tabanlı sistemden tarayıcı tabanlı (client-side) depolamaya dönüştürmeyi amaçlamaktadır. Kullanıcılar verilerini kendi tarayıcılarında saklayacak ve istedikleri zaman yedekleme/geri yükleme yapabileceklerdir. Bu yaklaşım, Streamlit Cloud deployment'ını basitleştirecek ve veritabanı bağımlılığını ortadan kaldıracaktır.

## Glossary

- **DERSLY System**: Ders programı ve not yönetimi için kullanılan Streamlit tabanlı web uygulaması
- **Browser Storage**: Kullanıcının tarayıcısında yerel olarak veri saklama mekanizması (Streamlit session state)
- **Export Function**: Kullanıcının verilerini JSON formatında indirmesini sağlayan fonksiyon
- **Import Function**: Kullanıcının daha önce dışa aktardığı verileri sisteme yüklemesini sağlayan fonksiyon
- **Session State**: Streamlit'in sayfa yenilemeleri arasında veri saklamak için kullandığı mekanizma
- **Data Persistence**: Verilerin kalıcı olarak saklanması durumu

## Requirements

### Requirement 1

**User Story:** Bir kullanıcı olarak, verilerimin kendi tarayıcımda saklanmasını istiyorum, böylece veritabanı kurulumu ve yönetimi ile uğraşmak zorunda kalmam.

#### Acceptance Criteria

1. WHEN the DERSLY System starts, THE DERSLY System SHALL initialize empty data structures in browser storage if no data exists
2. WHEN a user adds or modifies data, THE DERSLY System SHALL store the changes immediately in browser storage
3. THE DERSLY System SHALL maintain all existing functionality (courses, grades, schedule) using browser storage instead of database
4. WHEN a user closes and reopens the application in the same browser session, THE DERSLY System SHALL preserve all previously entered data
5. THE DERSLY System SHALL remove all database dependencies from the codebase

### Requirement 2

**User Story:** Bir kullanıcı olarak, verilerimi JSON dosyası olarak indirmek istiyorum, böylece yedek alabilirim ve verilerimi kaybetme riskini azaltabilirim.

#### Acceptance Criteria

1. THE DERSLY System SHALL provide an export button in the user interface
2. WHEN a user clicks the export button, THE DERSLY System SHALL generate a JSON file containing all user data
3. THE DERSLY System SHALL include all courses, grades, schedule entries, and settings in the exported JSON file
4. WHEN generating the export file, THE DERSLY System SHALL use a filename format that includes the current date and time
5. THE DERSLY System SHALL trigger an automatic download of the JSON file to the user's device

### Requirement 3

**User Story:** Bir kullanıcı olarak, daha önce dışa aktardığım verileri sisteme yüklemek istiyorum, böylece farklı tarayıcılarda veya cihazlarda verilerimi kullanabileyim.

#### Acceptance Criteria

1. THE DERSLY System SHALL provide an import button in the user interface
2. WHEN a user clicks the import button, THE DERSLY System SHALL display a file upload interface
3. WHEN a user uploads a JSON file, THE DERSLY System SHALL validate the file format and structure
4. IF the uploaded file is invalid or corrupted, THEN THE DERSLY System SHALL display an error message and reject the import
5. WHEN a valid JSON file is uploaded, THE DERSLY System SHALL replace current browser storage data with the imported data
6. WHEN import is successful, THE DERSLY System SHALL display a success message and refresh the interface to show imported data

### Requirement 4

**User Story:** Bir kullanıcı olarak, verilerimi yüklerken mevcut verilerimin üzerine yazılacağı konusunda uyarı almak istiyorum, böylece yanlışlıkla veri kaybı yaşamam.

#### Acceptance Criteria

1. WHEN a user initiates an import operation, THE DERSLY System SHALL check if existing data is present in browser storage
2. IF existing data is present, THEN THE DERSLY System SHALL display a confirmation dialog before proceeding with import
3. THE DERSLY System SHALL include a clear warning message in the confirmation dialog stating that current data will be replaced
4. WHEN a user confirms the import operation, THE DERSLY System SHALL proceed with replacing the data
5. WHEN a user cancels the import operation, THE DERSLY System SHALL abort the import and preserve existing data

### Requirement 5

**User Story:** Bir kullanıcı olarak, tarayıcı depolama alanının sınırlamaları hakkında bilgilendirilmek istiyorum, böylece ne kadar veri saklayabileceğimi bilebilirim.

#### Acceptance Criteria

1. THE DERSLY System SHALL display storage usage information in the settings or help section
2. WHEN storage usage exceeds 80 percent of available space, THE DERSLY System SHALL display a warning message to the user
3. THE DERSLY System SHALL provide guidance on exporting data to free up space if storage is nearly full
4. THE DERSLY System SHALL handle storage quota exceeded errors gracefully without crashing
5. IF storage quota is exceeded, THEN THE DERSLY System SHALL display an error message and suggest exporting data

### Requirement 6

**User Story:** Bir kullanıcı olarak, verilerimi temizleme seçeneğine sahip olmak istiyorum, böylece baştan başlamak istediğimde tüm verileri kolayca silebilirim.

#### Acceptance Criteria

1. THE DERSLY System SHALL provide a "Clear All Data" button in the settings section
2. WHEN a user clicks the clear data button, THE DERSLY System SHALL display a confirmation dialog with a strong warning
3. THE DERSLY System SHALL require explicit user confirmation before clearing any data
4. WHEN a user confirms data clearing, THE DERSLY System SHALL remove all data from browser storage
5. WHEN data is cleared, THE DERSLY System SHALL display a success message and reset the interface to initial state
