"""Student business logic."""
import secrets

from app.core.decorators import log_action, requires_auth
from app.core.exceptions import EnrollmentError, StudentNotFoundError
from app.models.student import Student
from app.repositories.course_repository import CourseRepository
from app.repositories.student_repository import StudentRepository


class StudentService:
    """Manage students, enrollment, grades, averages, and ranking."""
    def __init__(
        self,
        student_repository: StudentRepository,
        course_repository: CourseRepository,
        auth_service: object,
    ) -> None:
        self.student_repository = student_repository
        self.course_repository = course_repository
        self.auth_service = auth_service

    @property
    def is_authenticated(self) -> bool:
        """Expose authentication state to the requires_auth decorator."""
        return bool(getattr(self.auth_service, "is_authenticated", False))

    def _get_student(self, student_id: str) -> Student:
        student = self.student_repository.find_by_id(student_id.strip())
        if student is None:
            raise StudentNotFoundError(f"Student not found: {student_id}")
        return student

    @requires_auth
    @log_action
    def add_student(self, name: str, age: int, *, major: str) -> Student:
        """Validate, create, and persist a student."""
        clean_name = name.strip()
        clean_major = major.strip()
        if not clean_name or not clean_major:
            raise ValueError("Name and major are required.")
        if age <= 0:
            raise ValueError("Age must be greater than zero.")
        student = Student(
            f"STD-{secrets.token_hex(3).upper()}",
            clean_name,
            int(age),
            clean_major,
        )
        self.student_repository.add(student)
        return student

    @requires_auth
    def get_all_students(self) -> list[Student]:
        """Return all students."""
        return self.student_repository.all()

    @requires_auth
    @log_action
    def enroll_student(self, student_id: str, course_id: str) -> None:
        """Enroll a student after validating both records."""
        student = self._get_student(student_id)
        course_id = course_id.strip()
        if self.course_repository.find_by_id(course_id) is None:
            raise EnrollmentError(f"Course not found: {course_id}")
        student.enroll(course_id)
        self.student_repository.update(student)

    @requires_auth
    @log_action
    def set_grade(self, student_id: str, course_id: str, grade: float) -> None:
        """Set a grade only for an enrolled course."""
        student = self._get_student(student_id)
        course_id = course_id.strip()
        if course_id not in student.enrolled_course_ids:
            raise EnrollmentError("Student must be enrolled before a grade can be recorded.")
        student.set_grade(course_id, float(grade))
        self.student_repository.update(student)

    @requires_auth
    def calculate_average(self, student_id: str) -> float:
        """Calculate one student's grade average."""
        return self._get_student(student_id).average()

    @requires_auth
    def get_top_students(self, limit: int = 3) -> list[Student]:
        """Return students ordered by average grade, highest first."""
        students = self.student_repository.all()
        return sorted(students, key=lambda student: student.average(), reverse=True)[:limit]
