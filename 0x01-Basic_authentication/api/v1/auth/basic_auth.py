#!/usr/bin/env python3
""" Module of Basic Authentication
"""
import base64
from api.v1.auth.auth import Auth


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
      decoded_base64_authorization_header: str) -> (str, str):
        """ extract user credentials """
        if decoded_base64_authorization_header is None or not isinstance(
          decoded_base64_authorization_header, str):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        email, password = decoded_base64_authorization_header.split(':', 1)
        return email, password
