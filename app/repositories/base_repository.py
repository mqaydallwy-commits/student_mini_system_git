"""Generic JSON repository base class."""
import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Generic, TypeVar

from app.core.exceptions import DataStorageError

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Provide reusable JSON persistence for domain repositories."""
    def __init__(self, file_path: Path) -> None:
        self.file_path = file_path

    @abstractmethod
    def from_dict(self, data: dict[str, object]) -> T:
        """Convert persisted data to a domain object."""

    @staticmethod
    def _id_of(item: object) -> str:
        for attribute in ("user_id", "student_id", "course_id"):
            value = getattr(item, attribute, None)
            if value is not None:
                return str(value)
        raise DataStorageError("Persisted object has no supported ID field.")

    def _read_raw(self) -> list[dict[str, object]]:
        try:
            self.file_path.parent.mkdir(parents=True, exist_ok=True)
            if not self.file_path.exists():
                self.file_path.write_text("[]", encoding="utf-8")
            raw = json.loads(self.file_path.read_text(encoding="utf-8"))
            if not isinstance(raw, list):
                raise DataStorageError(f"Expected a JSON list in {self.file_path.name}.")
            return [item for item in raw if isinstance(item, dict)]
        except (OSError, json.JSONDecodeError) as exc:
            raise DataStorageError(f"Could not read {self.file_path.name}.") from exc

    def _write(self, items: list[T]) -> None:
        try:
            payload = [getattr(item, "to_dict")() for item in items]
            self.file_path.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except (OSError, TypeError) as exc:
            raise DataStorageError(f"Could not write {self.file_path.name}.") from exc

    def all(self) -> list[T]:
        """Return all persisted domain objects."""
        return [self.from_dict(item) for item in self._read_raw()]

    def add(self, item: T) -> None:
        """Append one domain object to storage."""
        items = self.all()
        items.append(item)
        self._write(items)

    def update(self, item: T) -> None:
        """Replace an existing object with the same identifier."""
        item_id = self._id_of(item)
        items = self.all()
        for index, existing in enumerate(items):
            if self._id_of(existing) == item_id:
                items[index] = item
                self._write(items)
                return
        raise DataStorageError(f"Object not found for update: {item_id}")

    def find_by_id(self, object_id: str) -> T | None:
        """Find a domain object by its identifier."""
        return next((item for item in self.all() if self._id_of(item) == object_id), None)
