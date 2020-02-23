import os
import yaml

from kfp import components, dsl


class Component():
    def __init__(self, id, component_name, notebook_path, parameters):
        self.id = id
        self.component_name = component_name
        self.notebook_path = notebook_path

        self.parameters = parameters
        self.container_op = None

        self.set_output_files()

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
            output_path=output_path,
            in_csv=self.in_csv,
            in_txt=self.in_txt,
            out_csv=self.out_csv,
            out_txt=self.out_txt).set_image_pull_policy('Always')
            
    def set_output_files(self):
        self.out_csv = self.component_name + '.csv'
        self.out_txt = self.component_name + '.txt'

    def set_input_files(self, csv, txt):
        self.in_csv = csv
        self.in_txt = txt

    def __str__(self):
        return '''id: {0}, component_name: {1}, notebook_path: {2}, dependencies: {3}'''.format(
            self.id, self.component_name, self.notebook_path,
            self.dependencies)
