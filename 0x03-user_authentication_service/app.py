#!/usr/bin/env python3
"""Basic Flask app to return a JSON message."""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    """Return a welcome message as a JSON payload."""
    return jsonify({"message": "Bienvenue"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
