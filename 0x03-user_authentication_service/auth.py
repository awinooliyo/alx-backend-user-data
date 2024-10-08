#!/usr/bin/env python3
"""
Auth module to handle user registration and authentication.
"""
from db import DB
from user import User
import bcrypt
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes a password and returns bytes.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The hashed password.
    """
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initializes the Auth class with a database instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with email and password.

        Args:
            email (str): The email of the user to register.
            password (str): The password for the user.

        Returns:
            User: The newly created User object.

        Raises:
            ValueError: If a user with the provided email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            return self._db.add_user(email=email,
                                     hashed_password=hashed_password)
