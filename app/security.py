import base64
import hashlib
import hmac
import os
import secrets
from typing import Optional

SECRET_KEY = os.getenv('SECRET_KEY', 'replace_this_before_production')
ITERATIONS = 100_000


def hash_password(password: str, salt: Optional[str] = None) -> str:
    """Store passwords as salt$hash."""
    final_salt = salt or secrets.token_hex(16)
    password_hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        final_salt.encode('utf-8'),
        ITERATIONS,
    )
    return f'{final_salt}${password_hash.hex()}'



def verify_password(plain_password: str, stored_password: str) -> bool:
    try:
        salt, expected_hash = stored_password.split('$', 1)
    except ValueError:
        return False

    calculated_hash = hashlib.pbkdf2_hmac(
        'sha256',
        plain_password.encode('utf-8'),
        salt.encode('utf-8'),
        ITERATIONS,
    ).hex()

    return hmac.compare_digest(calculated_hash, expected_hash)



def generate_session_token() -> str:
    """Simple signed token for demo / assessment use."""
    random_piece = secrets.token_urlsafe(32)
    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        random_piece.encode('utf-8'),
        hashlib.sha256,
    ).digest()
    encoded_signature = base64.urlsafe_b64encode(signature).decode().rstrip('=')
    return f'{random_piece}.{encoded_signature}'
