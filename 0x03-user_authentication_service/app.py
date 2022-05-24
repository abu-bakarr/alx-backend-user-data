#!/usr/bin/env python3
"""
FLask module
"""
from auth import Auth
from flask import Flask, jsonify, request, abort, redirect


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def main() -> str:
    """
    main route
    Returns:
    a Welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def reg_user() -> str:
    """
    reg_user route
    Registers a new User
    in the db
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
