"""Student domain model."""
from dataclasses import dataclass, field

from app.core.exceptions import InvalidGradeError, StudentAlreadyEnrolledError


@dataclass(slots=True)
class Student:
    """Represent a student, enrollments, and validated grades."""
    student_id: str
    name: str
    age: int
    major: str
    enrolled_course_ids: list[str] = field(default_factory=list)
    _grades: dict[str, float] = field(default_factory=dict, repr=False)

    def __str__(self) -> str:
        return f"{self.student_id} | {self.name} | {self.major}"

    @property
    def grades(self) -> dict[str, float]:
        """Return a copy of the student's grades."""
        return dict(self._grades)

    @grades.setter
    def grades(self, values: dict[str, float]) -> None:
        checked: dict[str, float] = {}
        for course_id, grade in values.items():
            checked[str(course_id)] = self._validate_grade(float(grade))
        self._grades = checked

    @staticmethod
    def _validate_grade(grade: float) -> float:
        if not 0 <= grade <= 100:
            raise InvalidGradeError("Grade must be between 0 and 100.")
        return grade

    def enroll(self, course_id: str) -> None:
        """Enroll the student in a course once."""
        if course_id in self.enrolled_course_ids:
            raise StudentAlreadyEnrolledError("Student is already enrolled in this course.")
        self.enrolled_course_ids.append(course_id)

    def set_grade(self, course_id: str, grade: float, /) -> None:
        """Set or update one course grade after validation."""
        self._grades[course_id] = self._validate_grade(float(grade))

    def average(self) -> float:
        """Return the arithmetic mean of recorded grades, or zero when empty."""
        return sum(self._grades.values()) / len(self._grades) if self._grades else 0.0

    def to_dict(self) -> dict[str, object]:
        """Serialize the student for JSON persistence."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "major": self.major,
            "enrolled_course_ids": list(self.enrolled_course_ids),
            "grades": dict(self._grades),
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Student":
        """Build a student from persisted JSON data."""
        student = cls(
            student_id=str(data["student_id"]),
            name=str(data["name"]),
            age=int(data["age"]),
            major=str(data["major"]),
            enrolled_course_ids=[str(value) for value in data.get("enrolled_course_ids", [])],
        )
        raw_grades = data.get("grades", {})
        if isinstance(raw_grades, dict):
            student.grades = {str(key): float(value) for key, value in raw_grades.items()}
        return student
