"""Application-specific exception hierarchy."""

class StudentSystemError(Exception):
    """Base exception for expected application errors."""

class AuthenticationError(StudentSystemError):
    """Raised when authentication fails or is required."""

class UserAlreadyExistsError(StudentSystemError):
    """Raised when a username is already registered."""

class StudentNotFoundError(StudentSystemError):
    """Raised when a student cannot be found."""

class CourseNotFoundError(StudentSystemError):
    """Raised when a course cannot be found."""

class StudentAlreadyEnrolledError(StudentSystemError):
    """Raised when a student is already enrolled in a course."""

class InvalidGradeError(StudentSystemError):
    """Raised when a grade is outside the range 0..100."""

class EnrollmentError(StudentSystemError):
    """Raised for invalid enrollment operations."""

class DataStorageError(StudentSystemError):
    """Raised when persisted data cannot be read or written safely."""
