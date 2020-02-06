import os
import yaml

from kfp import components, dsl


class Component():
    def __init__(self, id, component_name, notebook_path, parameters):
        self.id = id
        self.component_name = component_name
        self.notebook_path = notebook_path
        self.parameters = parameters
        self.dependencies = []
        self.container_op = None

    def _create_component_yaml(self):
        path = lambda file: os.path.join(os.path.dirname(__file__), 'resources', file)

        template_path = path('papermill.yaml')

        if (self.parameters):
            with open(template_path, 'r') as f:
                template = yaml.full_load(f.read())

            for parameter in self.parameters:
                template['implementation']['container']['command'].append('-p')
                template['implementation']['container']['command'].append(parameter['name'])
                template['implementation']['container']['command'].append(str(parameter['value']))


            file_path = path('{}.yaml'.format(self.component_name))

            with open(file_path, 'w') as f:
                f.write(yaml.dump(template))

            return file_path
        return template_path

    def create_container_op(self):
        notebook_path = self.notebook_path
        output_path = self.notebook_path + ".out"

        fpath = self._create_component_yaml()

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
