import flask_restful as restful

class Index(restful.Resource):
    def get(self):
        return {"message": "Pipeline Generator v0.1.0"}, 200

api = restful.Api()

def configure_api(app):
    api.add_resource(Index, '/')

    api.init_app(app)
