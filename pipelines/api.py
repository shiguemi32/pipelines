"""WSGI server."""
import sys

from flask import Flask, jsonify, request

from .train import create_train_pipeline

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return make_response(jsonify(message='PlatIAgro Pipelines v0.0.1'), 200)


@app.route('/pipelines', methods=['POST'])
def handle_create_train_pipeline():
    return jsonify(create_train_pipeline(request))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
