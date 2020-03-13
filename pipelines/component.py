# -*- coding: utf-8 -*-
import os
import yaml

from kfp import components, dsl
from nbconvert import PythonExporter

from .minio import load_notebook
from .resources.templates import COMPONENT_SPEC, GRAPH

class Component():
    def __init__(self, component_name, notebook_path, parameters, prev):
        self.component_name = component_name
        self.notebook_path = notebook_path

        self.parameters = parameters
        self.container_op = None

        self.image = "platiagro/datascience-notebook:latest"

        self.next = None
        self.prev = prev

        self.set_output_files()

    def _generate_component_image(self):
        notebook = load_notebook(self.notebook_path)
        
        pass

    def create_component_spec(self):
        self._generate_component_image()

        component_spec = COMPONENT_SPEC.substitute({
            "image": self.image,
            "name": self.component_name
        })
        
        return component_spec

    def create_component_graph(self):
        component_graph = GRAPH.substitute({
            "name": self.component_name,
            "type": "TRANSFORMER" if self.next else "MODEL",
            "children": self.next.create_component_graph() if self.next else ""
        })

        return component_graph


    def _create_component_yaml(self):
        path = lambda file: os.path.join(os.path.dirname(__file__), 'resources', file)

        template_path = path('papermill.yaml')

        if (self.parameters):
            with open(template_path, 'r') as f:
                template = yaml.full_load(f.read())

            for parameter in self.parameters:
                template['inputs'].append({"name": parameter['name'], "type": parameter['type'], "default": ""})

                template['implementation']['container']['command'].extend(['-p', parameter['name'], str(parameter['value'])])

            template['name'] = self.component_name

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
        
    def set_next_component(self, next_component):
        self.next = next_component
            
    def set_input_files(self, csv, txt):
        self.in_csv = csv
        self.in_txt = txt

    def set_output_files(self):
        self.out_csv = self.component_name + '.csv'
        self.out_txt = self.component_name + '.txt'
