#!/usr/bin/env python3
"""
Auth class for the API
"""
from api.v1.auth.auth import Auth
from api.v1.views import app_views
import base64
from flask import request
from models.user import User
from typing import List, TypeVar


class BasicAuth(Auth):
    """ Auth class
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Returns the Base64 part of the Authorization
        header for a Basic Authentication
        """
        if (not authorization_header or
                type(authorization_header) != str):
            return None
        ll = authorization_header.split(' ')
        if ll[0] == "Basic":
            return ll[1]
        return None

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """Returns the decoded value of a Base64 string
        """
        if (not base64_authorization_header or
                type(base64_authorization_header) != str):
            return None

        def isBase64(sb):
            try:
                if isinstance(sb, str):
                    sb_bytes = bytes(sb, 'ascii')
                elif isinstance(sb, bytes):
                    sb_bytes = sb
                else:
                    return False
                return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
            except Exception:
                return False

        if isBase64(base64_authorization_header):
            b = base64.b64decode(base64_authorization_header)
            return b.decode("utf-8")
        return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> (str, str):
        """returns the user email and password
        from the Base64 decoded value.
        """
        if (not decoded_base64_authorization_header or
                type(decoded_base64_authorization_header) != str
                or ':' not in decoded_base64_authorization_header):
            return None, None
        x = decoded_base64_authorization_header.split(":")
        if len(x) > 2:
            pwd = ':'.join(x[1:])
            x = [
                x[0],
                pwd]
        return tuple(x)

    def user_object_from_credentials(self,
                                     user_email: str, user_pwd: str
                                     ) -> TypeVar('User'):
        """ Returns the User instance based on his email and password.
        """
        x = User()
        if (not user_email or
                type(user_email) != str or
                not user_pwd or
                type(user_pwd) != str or
                not len(x.all())):
            return None
        result = x.search({'email': user_email})
        if not result:
            return None
        user = result[0]
        if not user.is_valid_password(user_pwd):
            return None
        return user

    def current_user(self, request=None) -> TypeVar('User'):
        """overloads Auth and retrieves
        the User instance for a request
        """
        head = self.authorization_header(request)
        aut = self.extract_base64_authorization_header(head)
        dec = self.decode_base64_authorization_header(aut)
        crend = self.extract_user_credentials(dec)
        return self.user_object_from_credentials(crend[0], crend[1])
