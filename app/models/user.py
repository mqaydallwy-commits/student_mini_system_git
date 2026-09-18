"""User domain model."""
from dataclasses import dataclass

from app.models.enums import UserRole


@dataclass(slots=True)
class User:
    """Represent an authenticated application user."""
    user_id: str
    username: str
    password_hash: str
    role: UserRole = UserRole.STAFF

    def to_dict(self) -> dict[str, object]:
        """Serialize the user for JSON persistence."""
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password_hash": self.password_hash,
            "role": self.role.value,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "User":
        """Build a user from persisted JSON data."""
        return cls(
            user_id=str(data["user_id"]),
            username=str(data["username"]),
            password_hash=str(data["password_hash"]),
            role=UserRole(str(data.get("role", UserRole.STAFF.value))),
        )
