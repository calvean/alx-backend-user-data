#!/usr/bin/env python3
""" Module of Basic Authentication
"""
import base64
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar, Tuple


class BasicAuth(Auth):
    """ Basic Authentication Class """
    def extract_base64_authorization_header(
      self,
      authorization_header: str) -> str:
        """ base64 authorization header """
        if authorization_header is None or not isinstance(
          authorization_header,
          str):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
      self,
      base64_authorization_header: str) -> str:
        """ decode the base64 """
        if base64_authorization_header is None or not isinstance(
          base64_authorization_header, str):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
      self,
      decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """ Extracts the user credentials
         from the decoded base64 authorization header
        """
        if decoded_base64_authorization_header is None or not isinstance(
          decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password

    def user_object_from_credentials(
      self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ return user object """
        if user_email is None or not isinstance(user_email, str):
            return None

        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})

        if len(users) == 0:
            return None

        for user in users:
            if user.is_valid_password(user_pwd):
                return user

        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieves the User instance for a request
        """
        if request is None:
            return None
        authorization_header = self.authorization_header(request)
        if authorization_header is None:
            return None
        base64_header = self.extract_base64_authorization_header(
          authorization_header)
        if base64_header is None:
            return None
        decoded_header = self.decode_base64_authorization_header(base64_header)
        if decoded_header is None:
            return None
        email, password = self.extract_user_credentials(decoded_header)
        if email is None or password is None:
            return None
        user = self.user_object_from_credentials(email, password)
        return user
