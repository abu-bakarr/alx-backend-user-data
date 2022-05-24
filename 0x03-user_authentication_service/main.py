#!/usr/bin/env python3
"""
Main file
"""
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
URL = "http://127.0.0.1:5000"


def register_user(email: str, password: str) -> None:
    """
    check register_user module
    """
    url = URL + "/users"
    data = {
        'email': email,
        'password': password
    }
    resp = requests.post(url, data=data)
    assert resp.status_code == 200
    assert resp.json() == {'email': email, 'message': 'user created'}


def log_in_wrong_password(email: str, password: str) -> None:
    """
    check login with wrong password
    """
    url = URL + "/sessions"
    data = {
        'email': email,
        'password': password
    }
    resp = requests.post(url, data=data)
    assert resp.status_code == 401


def log_in(email: str, password: str) -> str:
    """
    check login module
    """
    url = URL + "/sessions"
    data = {'email': email,
            'password': password
            }
    resp = requests.post(url, data=data)
    assert resp.status_code == 200
    assert resp.json() == {'email': email, 'message': 'logged in'}
    session_id = resp.cookies.get('session_id')
    return session_id


def profile_unlogged() -> None:
    """
    check profile without being logged in
    """
    url = URL + "/profile"
    ck = {'session_id': None}
    resp = requests.get(url, cookies=ck)
    assert resp.status_code == 403


def profile_logged(session_id: str) -> None:
    """
    check profile with a logged in user
    """
    url = URL + "/profile"
    ck = {'session_id': session_id}
    resp = requests.get(url, cookies=ck)
    assert resp.status_code == 200
    assert resp.json() == {'email': EMAIL}


def log_out(session_id: str) -> None:
    """
    check logout
    """
    url = URL + "/sessions"
    ck = {'session_id': session_id}
    resp = requests.delete(url, cookies=ck)
    assert resp.status_code == 200
    assert resp.json() == {'message': 'Bienvenue'}


def reset_password_token(email: str) -> str:
    """
    check reset token
    """
    url = URL + "/reset_password"
    data = {'email': email}
    resp = requests.post(url, data=data)
    assert resp.status_code == 200
    return resp.json().get('reset_token')


def update_password(email: str, reset_token: str,
                    new_password: str) -> None:
    """
    check update token
    """
    url = URL + "/reset_password"
    data = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password
    }
    resp = requests.put(url, data=data)
    assert resp.status_code == 200
    assert resp.json() == {'email': email, 'message': 'Password updated'}


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
