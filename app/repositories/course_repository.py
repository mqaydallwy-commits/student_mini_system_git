"""Course repository."""
from app.core.config import COURSES_FILE
from app.models.course import Course
from app.repositories.base_repository import BaseRepository


class CourseRepository(BaseRepository[Course]):
    """Persist and query courses."""
    def __init__(self) -> None:
        super().__init__(COURSES_FILE)

    def from_dict(self, data: dict[str, object]) -> Course:
        return Course.from_dict(data)
