"""Password hashing helpers based only on the Python standard library."""
import hashlib
import hmac
import secrets

def hash_password(password: str, *, salt: str | None = None) -> str:
    """Return a salted PBKDF2 password representation."""
    if not password:
        raise ValueError("Password cannot be empty.")
    salt_value = salt or secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt_value.encode(), 120_000)
    return f"pbkdf2_sha256$120000${salt_value}${digest.hex()}"

def verify_password(password: str, stored_hash: str) -> bool:
    """Verify a plain password against a stored PBKDF2 representation."""
    try:
        algorithm, iterations, salt, expected = stored_hash.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        actual = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), int(iterations)).hex()
        return hmac.compare_digest(actual, expected)
    except (ValueError, TypeError):
        return False
