#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _private_session(self) -> Session:
        """Memoized private session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The email address of the user.
            hashed_password (str): The hashed password of the user.

        Returns:
            User: The created User object.

        """
        user = User(email=email, hashed_password=hashed_password)
        self._private_session.add(user)
        self._private_session.commit()
        return user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database based on the provided keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering the query.

        Returns:
            User: The first User object that matches the query.

        Raises:
            NoResultFound: If no user matches the query.
            InvalidRequestError: If incorrect query arguments are passed.

        """
        try:
            user = self._private_session.query(User).filter_by(**kwargs).first()
            if not user:
                raise NoResultFound("No user found for the given query.")
            return user
        except InvalidRequestError as e:
            raise InvalidRequestError("Incorrect query arguments.") from e

