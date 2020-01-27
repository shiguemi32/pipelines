"""WSGI server."""
import sys

from flask import Flask, jsonify, make_response

app = Flask(__name__)


@app.route('/')
def index():
    return make_response(jsonify(['PlatIAgro Pipelines v0.0.1']), 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
