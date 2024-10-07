#!/usr/bin/env python3
"""Auth module for handling authentication-related tasks."""


from db import DB
from user import User  # Assuming User is the model class for users
import bcrypt
from sqlalchemy.orm.exc import NoResultFound  # Import the correct exception


class Auth:
    """Auth class to interact with the authentication database.

    This class provides methods for user registration, including hashing
    passwords and storing user details in the database.
    """

    def __init__(self):
        """
        Initializes the Auth class with a private instance of the database
        object.

        The database object (_db) is responsible for interacting with the
        user data.

        Attributes:
            _db (DB): A private instance of the database class to handle
                      user-related database operations.
        """
        self._db = DB()

    def _hash_password(self, password: str) -> str:
        """
        Hashes a password using bcrypt.

        This method securely hashes the password provided by the user before
        storing it in the database, using bcrypt to ensure the password is
        hashed with a salt.

        Args:
            password (str): The plain text password to be hashed.

        Returns:
            str: The hashed version of the password.
        """
        return bcrypt.hashpw(password.encode('utf-8'),
                             bcrypt.gensalt()).decode('utf-8')

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user with the given email and password.

        This method checks if a user already exists in the database by email.
        If the user exists, a ValueError is raised. If the user doesn't exist,
        the password is hashed and the new user is saved to the database.

        Args:
            email (str): The email address of the user to register.
            password (str): The plain text password of the user to register.

        Returns:
            User: The newly created user object.

        Raises:
            ValueError: If a user with the provided email already exists in
                        the database.
        """
        try:
            # Try to find a user by email
            self._db.find_user_by(email=email)
            # If a user is found, raise ValueError
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            # If no user is found, proceed to create a new user
            hashed_password = self._hash_password(password)
            # Add the new user to the database
            new_user = self._db.add_user(email=email,
                                         hashed_password=hashed_password)
            return new_user
