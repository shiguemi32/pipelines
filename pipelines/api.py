# -*- coding: utf-8 -*-
"""WSGI server."""
import argparse
import sys

from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.exceptions import BadRequest, InternalServerError

from .train import train_pipeline, train_pipeline_status
from .deploy import deploy_pipeline

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    """Handles GET requests to /."""
    return jsonify(message='PlatIAgro Pipelines v0.0.1')

@app.route("/train/<run_id>", methods=["GET"])
def handle_train_pipeline_status(run_id):
    """Handles GET requests to /train/<run_id>."""
    return jsonify(train_pipeline_status(run_id))

@app.route('/train', methods=['POST'])
def handle_train_pipeline():
    """Handles POST requests to /train."""
    req_data = request.get_json()
    run_id = train_pipeline(req_data)
    return jsonify({"message": "Pipeline running.", "runId": run_id})

@app.route('/deploy', methods=['POST'])
def handle_deploy_pipeline():
    """Handles POST requests to /deploy."""
    req_data = request.get_json()
    experiment_id = req_data.get('experiment_id')
    components = req_data.get('components')
    dataset = req_data.get('dataset')
    target = req_data.get('target')
    return jsonify(
        deploy_pipeline(experiment_id, components, dataset, target)
    )

@app.errorhandler(BadRequest)
@app.errorhandler(InternalServerError)
def handle_errors(err):
    """Handles exceptions raised by the API."""
    return jsonify({"message": err.description}), err.code

def parse_args(args):
    """Takes argv and parses API options."""
    parser = argparse.ArgumentParser(
        description="Datasets API"
    )
    parser.add_argument(
        "--port", type=int, default=8080, help="Port for HTTP server (default: 8080)"
    )
    parser.add_argument("--enable-cors", action="count")
    return parser.parse_args(args)

if __name__ == "__main__":
    args = parse_args(sys.argv[1:])

    # Enable CORS if required
    if args.enable_cors:
        CORS(app)

    app.run(host="0.0.0.0", port=args.port)
