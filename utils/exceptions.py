"""
Custom exceptions for DERSLY Streamlit application.
Defines storage-related exceptions for error handling.
"""


class StorageError(Exception):
    """
    Base exception for storage operations.
    All storage-related exceptions inherit from this class.
    """
    pass


class StorageQuotaExceeded(StorageError):
    """
    Raised when storage quota is exceeded.
    Indicates that the browser storage limit has been reached.
    """
    def __init__(self, message="Depolama alanı doldu. Lütfen verilerinizi dışa aktarın ve gereksiz kayıtları silin."):
        self.message = message
        super().__init__(self.message)


class InvalidDataFormat(StorageError):
    """
    Raised when imported data format is invalid.
    Indicates that the JSON structure doesn't match expected format.
    """
    def __init__(self, message="Geçersiz veri formatı. Lütfen geçerli bir DERSLY yedek dosyası kullanın."):
        self.message = message
        super().__init__(self.message)


class DataCorrupted(StorageError):
    """
    Raised when data is corrupted or cannot be parsed.
    Indicates that the data integrity has been compromised.
    """
    def __init__(self, message="Veri bozuk veya okunamıyor. Lütfen farklı bir yedek dosyası deneyin."):
        self.message = message
        super().__init__(self.message)


class ProfileNotFound(StorageError):
    """
    Raised when user profile is not found.
    Indicates that the user needs to create a profile first.
    """
    def __init__(self, message="Kullanıcı profili bulunamadı. Lütfen önce profil oluşturun."):
        self.message = message
        super().__init__(self.message)


class ItemNotFound(StorageError):
    """
    Raised when a requested item (course, assignment, grade) is not found.
    """
    def __init__(self, item_type="Öğe", item_id=None):
        if item_id:
            self.message = f"{item_type} bulunamadı (ID: {item_id})."
        else:
            self.message = f"{item_type} bulunamadı."
        super().__init__(self.message)
