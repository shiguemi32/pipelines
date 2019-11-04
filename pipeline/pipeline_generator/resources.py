from flask import request
from flask_restful import Resource

from .pipeline import Pipeline
from .component import Component
from .utils import key_exists

# pylint: disable = inconsistent-return-statements

class PipelineResource(Resource):
    def post(self):
        req_data = request.get_json() or None

        components = req_data.get('components', None)

        if not components:
            return {"message": "Invalid request."}, 400

        object_components = {}
        edges = []

        for i, t in enumerate(components):
            try:
                component_name = t['component_name']
                notebook_name = t['notebook_name']
            except KeyError:
                return {"message": "Invalid data."}, 400
            if not key_exists(object_components, component_name):
                object_components[i] = Component(i, component_name, notebook_name)
            else:
                return {"message": "Duplicate component."}, 400

        for i, t in enumerate(components):
            try:
                dependencies = t['dependencies']
                for d in dependencies:
                    dependence_id = None
                    dependence = None
                    for key, value in object_components.items():
                        if value.component_name == d:
                            dependence_id = key
                            dependence = value 
                            break
                    if dependence_id is None:
                        return {"message": "Invalid dependence: {}.".format(d)}, 400
                    object_components[i].add_dependence(dependence)
                    edges.append((dependence_id, i))
            except KeyError:
                continue

        pipeline = Pipeline(object_components, edges)
        pipeline.write_script()
        pipeline.execute_script()
