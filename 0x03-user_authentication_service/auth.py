#!/usr/bin/env python3
"""
Encrypt a string
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound, InvalidRequestError
from uuid import uuid4


def _hash_password(password: str) -> str:
    """
    Hashes the password.

    Args:
        password: String to be hashed.

    Returns:
        Hashed password as a string.
    """
    hashed = bcrypt.hashpw(
      password.encode('utf-8'), bcrypt.gensalt(prefix=b"2b"))
    return hashed.decode()


def _generate_uuid() -> str:
    """
    Generates a UUID.

    Returns:
        Generated UUID as a string.
    """
    UUID = uuid4()
    return str(UUID)


class Auth:
    """Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a user.

        Args:
            email: Email of the user.
            password: Password to be hashed.

        Returns:
            The registered User object.

        Raises:
            ValueError: If the user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f'User with email <{email}> already exists.')
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validates the login credentials.

        Args:
            email: Email of the user.
            password: Password to be checked.

        Returns:
            True if the login credentials are valid, False otherwise.
        """
        if email is None or password is None:
            return False

        try:
            user = self._db.find_user_by(email=email)
            hashed_password = str.encode(user.hashed_password)
            valid = bcrypt.checkpw(password.encode('utf-8'), hashed_password)
            return valid
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """
        Creates a session ID for the user and updates it in the database.

        Args:
            email: Email of the user.

        Returns:
            The session ID generated.

        Raises:
            NoResultFound: If the user with the given email is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Finds a user based on the session ID.

        Args:
            session_id: Session identifier.

        Returns:
            The User object if found, None otherwise.
        """
        if not session_id:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except (NoResultFound, InvalidRequestError):
            return None

    def destroy_session(self, user_id: str) -> None:
        """
        Destroys the session for the user.

        Args:
            user_id: User ID to destroy the session.

        Returns:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except ValueError:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a reset password token for the user.

        Args:
            email: Email of the user.

        Returns:
            The reset password token generated.

        Raises:
            ValueError: If the email is None
             or the user with the given email is not found.
        """
        if email is None:
            raise ValueError

        try:
            user = self._db.find_user_by(email=email)
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except (NoResultFound, InvalidRequestError):
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates the password for the user.

        Args:
            reset_token: Reset password token.
            password: New password.

        Returns:
            None

        Raises:
            ValueError: If the reset_token or password is None
             or the user with the given reset_token is not found.
        """
        if reset_token is None or password is None:
            return None

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except (NoResultFound, InvalidRequestError):
            raise ValueError

        hashed_password = _hash_password(password)
        self._db.update_user(
          user.id, hashed_password=hashed_password, reset_token=None)
        return None
