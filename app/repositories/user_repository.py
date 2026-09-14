"""User repository."""
from app.core.config import USERS_FILE
from app.models.user import User
from app.repositories.base_repository import BaseRepository

class UserRepository(BaseRepository[User]):
    """Persist and query users."""
    def __init__(self) -> None:
        super().__init__(USERS_FILE)

    def from_dict(self, data: dict[str, object]) -> User:
        return User.from_dict(data)

    def find_by_username(self, username: str) -> User | None:
        """Find a user by case-sensitive username."""
        return next((user for user in self.all() if user.username == username), None)
