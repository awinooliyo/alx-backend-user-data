#!/usr/bin/env python3
"""Auth module for handling authentication-related tasks."""

from db import DB
from user import User
from sqlalchemy.exc import NoResultFound
import bcrypt


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Hash a password using bcrypt and return the salted hash.

        Args:
            password (str): The password to hash.

        Returns:
            bytes: The salted hash of the password.
        """
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt)

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the given email and password.

        Args:
            email (str): The email address of the new user.
            password (str): The password for the new user.

        Returns:
            User: A User object representing the newly created user.

        Raises:
            ValueError: If a user with the provided email already exists.
        """
        # Check if user already exists
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            # User does not exist, proceed with registration
            hashed_password = self._hash_password(password)
            return self._db.add_user(email, hashed_password)
