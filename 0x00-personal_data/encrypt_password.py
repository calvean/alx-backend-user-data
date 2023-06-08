#!/usr/bin/env python3
"""
encrypt password module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password: password to be hashed.

    Returns:
        salted and hashed password.
    """
    pass_encoded = password.encode()
    pass_hashed = bcrypt.hashpw(pass_encoded, bcrypt.gensalt())
    return pass_hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password against a hashed password using bcrypt.

    Args:
        hashed_password: hashed password.
        password: password to be validated.

    Returns:
        bool
    """
    pass_encoded = password.encode()
    return bcrypt.checkpw(pass_encoded, hashed_password)
