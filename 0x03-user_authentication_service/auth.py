#!/usr/bin/env python3
"""Auth module for handling authentication-related tasks."""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password with bcrypt and return the salted hash.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
