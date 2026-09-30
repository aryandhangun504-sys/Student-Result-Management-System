"""Custom exceptions used across the application."""


class SRMSError(Exception):
    """Base class for all application-specific errors."""


class ValidationError(SRMSError):
    """Raised when user-supplied data is invalid."""


class DuplicateStudentError(SRMSError):
    """Raised when adding a student whose roll number already exists."""


class StudentNotFoundError(SRMSError):
    """Raised when no student matches the given roll number."""


class StorageError(SRMSError):
    """Raised when reading or writing the data file fails."""
