import os

from kfp import components, dsl


class Component():
    def __init__(self, id, component_name, notebook_path):
        self.id = id
        self.component_name = component_name
        self.notebook_path = notebook_path
        self.dependencies = []
        self.container_op = None

    def create_container_op(self):
        notebook_path = self.notebook_path
        output_path = self.notebook_path + ".out"

        fpath = os.path.join(os.path.dirname(__file__), 'resources',
                             'papermill.yaml')

        container = components.load_component_from_file(fpath)

        self.container_op = container(
            notebook_path=notebook_path,
            output_path=output_path).set_image_pull_policy('Always')
            
    def add_dependency(self, dependency):
        self.dependencies.append(dependency)

    def __str__(self):
        return '''id: {0}, component_name: {1}, notebook_path: {2}, dependencies: {3}'''.format(
            self.id, self.component_name, self.notebook_path,
            self.dependencies)
