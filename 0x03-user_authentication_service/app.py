#!/usr/bin/env python3
"""Basic Flask app to manage user registration."""

from flask import Flask, jsonify, request
from auth import Auth
from sqlalchemy.exc import NoResultFound

app = Flask(__name__)

AUTH = Auth()


@app.route("/", methods=["GET"])
def home():
    """Return a welcome message as a JSON payload."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """POST /users
    Register a new user.

    Returns:
        JSON payload containing:
        - email: The registered email address
        - message: A confirmation message.
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or not password:
        return jsonify({"message": "email and password required"}), 400

    try:
        # Register the user
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"}), 201
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    except NoResultFound:
        return jsonify({"message": "user not found"}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
