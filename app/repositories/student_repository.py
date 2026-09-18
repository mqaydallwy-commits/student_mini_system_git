"""Student repository."""
from app.core.config import STUDENTS_FILE
from app.models.student import Student
from app.repositories.base_repository import BaseRepository


class StudentRepository(BaseRepository[Student]):
    """Persist and query students."""
    def __init__(self) -> None:
        super().__init__(STUDENTS_FILE)

    def from_dict(self, data: dict[str, object]) -> Student:
        return Student.from_dict(data)
