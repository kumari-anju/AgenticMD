import secrets
import string

def generate_random_token(length: int = 40) -> str:
    """Generate a random token string for session management."""
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))
