"""Enumerations used by domain models."""
from enum import Enum


class UserRole(str, Enum):
    """Supported application user roles."""
    STAFF = "staff"
    ADMIN = "admin"


class CourseLevel(str, Enum):
    """Supported course difficulty levels."""
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
