import flask_restful as restful

from pipeline.pipeline_generator.resources import PipelineResource
class Index(restful.Resource):
    def get(self):
        return {"message": "Pipeline Generator v0.1.0"}, 200

api = restful.Api()

def configure_api(app):
    api.add_resource(Index, '/')
    api.add_resource(PipelineResource, '/pipelines')

    api.init_app(app)
