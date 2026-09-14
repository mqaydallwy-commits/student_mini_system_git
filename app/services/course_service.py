"""Course business logic."""
import secrets
from datetime import datetime
from app.core.decorators import log_action, requires_auth
from app.core.exceptions import CourseNotFoundError, EnrollmentError
from app.models.course import Course
from app.models.enums import CourseLevel
from app.repositories.course_repository import CourseRepository

def _course_name_validator(min_length: int):
    """Return a closure that validates a course name length."""
    def validator(value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < min_length:
            raise ValueError(f"Course name must contain at least {min_length} characters.")
        return cleaned
    return validator

validate_course_name = _course_name_validator(2)

class CourseService:
    """Manage course creation and retrieval."""
    def __init__(self, course_repository: CourseRepository, auth_service: object) -> None:
        self.course_repository = course_repository
        self.auth_service = auth_service

    @property
    def is_authenticated(self) -> bool:
        """Expose authentication state to the requires_auth decorator."""
        return bool(getattr(self.auth_service, "is_authenticated", False))

    @requires_auth
    @log_action
    def add_course(self, name: str, hours: int, start_date: str, *, level: CourseLevel = CourseLevel.BEGINNER) -> Course:
        """Create and persist a course after validating its fields."""
        clean_name = validate_course_name(name)
        try:
            datetime.strptime(start_date.strip(), "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("Start date must use YYYY-MM-DD format.") from exc
        if hours <= 0:
            raise ValueError("Hours must be greater than zero.")
        course = Course(f"CRS-{secrets.token_hex(3).upper()}", clean_name, int(hours), start_date.strip(), level)
        self.course_repository.add(course)
        return course

    @requires_auth
    def get_all_courses(self) -> list[Course]:
        """Return all courses."""
        return self.course_repository.all()

    def get_course(self, course_id: str) -> Course:
        """Return one course or raise CourseNotFoundError."""
        course = self.course_repository.find_by_id(course_id)
        if course is None:
            raise CourseNotFoundError(f"Course not found: {course_id}")
        return course
