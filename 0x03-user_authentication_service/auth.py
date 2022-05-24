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
