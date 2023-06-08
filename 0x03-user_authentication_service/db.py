#!/usr/bin/env python3
"""
Database module
"""
from sqlalchemy import create_engine
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User


class DB:
    """Model Database"""

    def __init__(self):
        """
        Initialize a new DB instance.
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> sessionmaker:
        """
        Memoized session object.
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
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user in the database based on the provided keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments for filtering the query.

        Returns:
            User: The first User object that matches the query.

        Raises:
            InvalidRequestError: If no keyword arguments are provided
             or if any provided argument is invalid.
            NoResultFound: If no user matches the query.
        """
        if not kwargs:
            raise InvalidRequestError("No keyword arguments provided.")

        cols_keys = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in cols_keys:
                raise InvalidRequestError(f"Invalid keyword argument: {key}")

        user = self._session.query(User).filter_by(**kwargs).first()
        if not user:
            raise NoResultFound("No user found for the given query.")
        return user

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user in the database.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments
             representing the fields to update.

        Returns:
            None

        Raises:
            ValueError: If any provided keyword argument is invalid.
            NoResultFound: If the user with the specified ID is not found.
        """
        if not kwargs:
            return None

        user = self.find_user_by(id=user_id)

        cols_keys = User.__table__.columns.keys()
        for key in kwargs.keys():
            if key not in cols_keys:
                raise ValueError(f"Invalid keyword argument: {key}")

        for key, value in kwargs.items():
            setattr(user, key, value)

        self._session.commit()
