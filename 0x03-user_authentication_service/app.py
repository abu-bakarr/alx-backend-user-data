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
