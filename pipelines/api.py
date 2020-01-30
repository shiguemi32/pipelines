"""WSGI server."""
import sys

from flask import Flask, jsonify, make_response, request

from .utils import normalize_string
from .component import Component
from .pipeline import Pipeline

app = Flask(__name__)

@app.route('/')
def index():
    return make_response(jsonify(message='PlatIAgro Pipelines v0.0.1'), 200)


@app.route('/pipelines', methods=['POST'])
def train_pipeline():
    req_data = request.get_json() or None

    components = req_data.get('components', None)

    if not components:
        return make_response(jsonify(message='Invalid request.'), 400)
    
    components_objects = [None for x in range(len(components))]

    for index, component in enumerate(components):
        try:
            component_name = normalize_string(component['component_name'])
            notebook_path = component['notebook_path']
        except KeyError:
            return make_response(jsonify(message='Invalid data.'), 400)
        
        components_objects[index] = Component(index, component_name, notebook_path)

    pipeline = Pipeline(components_objects)
    
    pipeline.compile_pipeline()
    pipeline.run_pipeline()

    return make_response(jsonify(message='Pipeline Running.'), 200)
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
