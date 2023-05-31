#!/usr/bin/env python3
""" Module of Authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """ Authentication class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return True
        for excluded_path in excluded_paths:
            if path.endswith(excluded_path):
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ method for authentication header """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ method to return the user """
        return None
