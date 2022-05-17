#!/usr/bin/env python3
"""
Auth class for the API
"""
from api.v1.views import app_views
from flask import request
from models.user import User
from typing import List, TypeVar


class Auth:
    """ Auth class
    """

    def require_auth(self, path: str, extra_paths: List[str]) -> bool:
        """ Define which routes don't need authentication
        """
        if (path is None or extra_paths is None
                or len(extra_paths) == 0 or len(path) == 0):
            return True
        for x in extra_paths:
            if x[-1] == '/':
                x = x[:-1]
            if x[-1] == '*':
                x = x[:-1]
            if x in path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Return the value of the header request
        """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """ current_user
        """
        return None
