"""Course domain model."""
from dataclasses import dataclass

from app.models.enums import CourseLevel


@dataclass(slots=True)
class Course:
    """Represent a course offered to students."""
    course_id: str
    course_name: str
    hours: int
    start_date: str
    level: CourseLevel = CourseLevel.BEGINNER

    def __str__(self) -> str:
        return f"{self.course_id} | {self.course_name} | {self.hours} hours"

    def to_dict(self) -> dict[str, object]:
        """Serialize the course for JSON persistence."""
        return {
            "course_id": self.course_id,
            "course_name": self.course_name,
            "hours": self.hours,
            "start_date": self.start_date,
            "level": self.level.value,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Course":
        """Build a course from persisted JSON data."""
        return cls(
            course_id=str(data["course_id"]),
            course_name=str(data["course_name"]),
            hours=int(data["hours"]),
            start_date=str(data["start_date"]),
            level=CourseLevel(str(data.get("level", CourseLevel.BEGINNER.value))),
        )
