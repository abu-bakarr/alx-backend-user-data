#!/usr/bin/env python3
""" log message obfuscated
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ password encrypted
    """
    password = password.encode()
    hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ check if a  password encrypted is valid
    """
    password = password.encode('utf-8')
    if bcrypt.checkpw(password, hashed_password):
        return True
    else:
        return False
