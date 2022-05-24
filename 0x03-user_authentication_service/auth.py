#!/usr/bin/env python3
"""Module: Authentication"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> str:
    """Function: Return a string hash of the input password"""
    passwd = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(passwd, salt)
    return hashed


def _generate_uuid() -> str:
    """Function: Generate UUIDs"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Method: Constructor"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Method: Register new User"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed = _hash_password(password)
            new_user = self._db.add_user(email, hashed)
            return new_user
        raise ValueError('User {} already exists'.format(user.email))

    def valid_login(self, email: str, password: str) -> bool:
        """Method: Credentials Validation"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Method: Get session ID """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        user.session_id = _generate_uuid()
        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> None:
        """Method: Find user by session ID"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Method: Destroy Session"""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None
        user.session_id = None

    def get_reset_password_token(self, email: str) -> str:
        """Method: Reset Password Token"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        new_uuid = _generate_uuid()
        user.reset_token = new_uuid
        return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Method: Update Password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed = _hash_password(password)
        user.hashed_password = hashed
        user.reset_token = None
