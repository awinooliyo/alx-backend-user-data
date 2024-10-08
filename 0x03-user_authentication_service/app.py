#!/usr/bin/env python3
"""A simple Flask app with user authentication features."""

import logging
from flask import Flask, abort, jsonify, redirect, request
from auth import Auth

# Disable warning logging for cleaner output
logging.disable(logging.WARNING)

AUTH = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """GET /
    Return:
        JSON payload containing a welcome message.
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    """
    POST /users route to register a new user.
    Expects 'email' and 'password' in the form data.
    Returns:
        - JSON response {"email": "<email>", "message": "user created"}
          if the user is created.
        - JSON response {"message": "email already registered"}
          with status 400 if the user already exists.
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        # Register the user using the Auth object
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        # If the user already exists, return the appropriate response
        return jsonify({"message": "email already registered"}), 200


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """POST /sessions
    Log in a user and create a session.

    Returns:
        JSON payload containing:
        - email: The user's email address
        - message: A login confirmation message.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """DELETE /sessions
    Log out a user by destroying their session.

    Returns:
        A redirect to the home route if successful.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """GET /profile
    Return the user's email if authenticated.

    Returns:
        JSON payload containing:
        - email: The user's email address.
    """
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """POST /reset_password
    Generate a reset password token.

    Returns:
        JSON payload containing:
        - email: The user's email address
        - reset_token: The generated reset token.
    """
    email = request.form.get("email")
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token})


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """PUT /reset_password
    Update the user's password.

    Returns:
        JSON payload containing:
        - email: The user's email address
        - message: Confirmation of the password update.
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
