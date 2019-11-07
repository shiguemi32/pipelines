from flask import request
from flask_restful import Resource

from .pipeline import Pipeline
from .component import Component
from .utils import normalize_string

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
                component_name = normalize_string(t['component_name'])
                notebook_path = t['notebook_path']          
            except KeyError:
                return {"message": "Invalid data."}, 400
            image = t.get('image', 'platiagro/datascience-notebook:latest')
            object_components[i] = Component(i, component_name, notebook_path, image)

        for i, t in enumerate(components):
            try:
                dependencies = t['dependencies']
                for d in dependencies:
                    d = normalize_string(d)
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

        for i, t in enumerate(components):
            try:
                parameters = t['parameters']
                for p in parameters:
                    object_components[i].add_parameter(p)
            except KeyError:
                continue

        pipeline = Pipeline(object_components, edges)
        pipeline.write_script()
        pipeline.execute_script()
        try:
            pipeline.upload_pipeline()
            return {"message": "Pipeline successfully created!"}, 200
        except:
            return {"message": "Failed to connect to Kubeflow Pipelines API."}, 503
