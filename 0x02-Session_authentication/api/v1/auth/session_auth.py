#!/usr/bin/env python3
""" Module of Session Authentication
"""
from api.v1.auth.auth import Auth
from models.user import User
from os import getenv
from typing import List, TypeVar, Optional
import uuid


class SessionAuth(Auth):
    """ Session Authentication """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create a Session ID for a user_id """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Return a User ID based on a Session ID """
        if session_id is None or not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id)

    def session_cookie(self, request=None) -> Optional[str]:
        """ Return a cookie value from a request """
        if request is None:
            return None
        session_name = getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_name)

    def current_user(self, request=None) -> Optional[User]:
        """ Return a User instance based on a cookie value """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        if user_id is not None:
            return User.get(user_id)
        return None

    def destroy_session(self, request=None):
        """ Deletes the user session / logout """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        self.user_id_by_session_id.pop(session_id, None)
        return True
