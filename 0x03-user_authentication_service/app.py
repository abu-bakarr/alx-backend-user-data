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


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    Login route
    Logs a user in
    and sets the session id's cookie
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if AUTH.valid_login(email, password):
        s_id = AUTH.create_session(email)
        resp = jsonify({"email": email, "message": "logged in"})
        resp.set_cookie('session_id', s_id)
        return resp
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """
    Logout route
    logs a User out
    and removes its session ID
    """
    s_id = request.cookies.get("session_id")
    if not s_id:
        abort(403)
    u = AUTH.get_user_from_session_id(s_id)
    if not u:
        abort(403)
    AUTH.destroy_session(u.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    Profile route
    checks if the User have a session ID
    and then provides its info
    """
    s_id = request.cookies.get("session_id")
    if not s_id:
        abort(403)
    u = AUTH.get_user_from_session_id(s_id)
    if u:
        return jsonify({"email": u.email})
    else:
        abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    Get reset password token
    checks if the email provided has a User
    and provides a reset token
    """
    email = request.form.get('email')
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": token}), 200
    except Exception:
        abort(403)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """
    Update password end-point
    check if the user exists
    and then updates it's password
    """
    email = request.form.get('email')
    npass = request.form.get('new_password')
    token = request.form.get('reset_token')
    try:
        AUTH.update_password(token, npass)
        return (
            jsonify({"email": email,
                     "message": "Password updated"}),
            200)
    except Exception:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
