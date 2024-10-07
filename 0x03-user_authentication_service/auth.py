#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """
    Hash a password using bcrypt with a salt.
    Args:
        password (str): The password to be hashed.
    Returns:
        bytes: The salted hash of the password.
    """
    # Generate a salt
    salt = bcrypt.gensalt()
    # Hash the password with the salt
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
