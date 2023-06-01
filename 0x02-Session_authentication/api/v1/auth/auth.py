#!/usr/bin/env python3
""" Module of Authentication
"""
from flask import request, Request
from typing import List, TypeVar, Optional
import fnmatch
import os

class Auth:
    """ Authentication class """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if authentication is required for the given path
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                pattern = excluded_path.rstrip('*')
                if path.startswith(pattern):
                    return False
            elif path.rstrip('/') == excluded_path.rstrip('/'):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ authorization header """
        if request is None:
            return None
        if 'Authorization' not in request.headers:
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ method to return the user """
        return None

    def session_cookie(self, request: Optional[Request] = None) -> Optional[str]:
        """ Return a cookie value from a request """
        if request is None:
            return None
        session_cookie_name = os.getenv("SESSION_NAME", "_my_session_id")
        return request.cookies.get(session_cookie_name)
