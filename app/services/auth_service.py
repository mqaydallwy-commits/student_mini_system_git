"""Authentication business logic."""
import secrets
from app.core.decorators import log_action
from app.core.exceptions import AuthenticationError, UserAlreadyExistsError
from app.core.security import hash_password, verify_password
from app.models.user import User
from app.repositories.user_repository import UserRepository

class AuthService:
    """Manage registration, login, logout, and authentication state."""
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository
        self.current_user: User | None = None

    @property
    def is_authenticated(self) -> bool:
        """Return whether a user is currently logged in."""
        return self.current_user is not None

    @log_action
    def register(self, username: str, password: str, *, role: str = "staff") -> User:
        """Register a new user with a hashed password."""
        username = username.strip()
        if not username or not password:
            raise ValueError("Username and password are required.")
        if self.user_repository.find_by_username(username):
            raise UserAlreadyExistsError("Username already exists.")
        user = User(f"USR-{secrets.token_hex(4).upper()}", username, hash_password(password))
        self.user_repository.add(user)
        return user

    @log_action
    def login(self, username: str, password: str) -> User:
        """Authenticate a user and set the current session."""
        user = self.user_repository.find_by_username(username.strip())
        if user is None or not verify_password(password, user.password_hash):
            raise AuthenticationError("Invalid username or password.")
        self.current_user = user
        return user

    def logout(self) -> None:
        """End the current authenticated session."""
        self.current_user = None
