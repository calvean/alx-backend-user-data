#!/usr/bin/env python3
""" Module of Authentication
"""
from flask import request
from typing import List, TypeVar
import fnmatch


class Auth:
    """ Authentication class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Checks if authentication is required for the given path
        """
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for pattern in excluded_paths:
            if fnmatch.fnmatch(path, pattern):
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
