# -*- coding: utf-8 -*-
import os
import yaml

from kfp import components, dsl

from .minio import load_notebook
from .resources.templates import COMPONENT_SPEC, GRAPH

class Component():
    """Represents a Pipeline Component.
    
    Attributes:
        container_op (kfp.dsl.ContainerOp): component operator.
    """

    def __init__(self, component_name, notebook_path, parameters, prev):
        """Create a new instance of Component.

        Args:
            component_name (str): component name.
            notebook_path (str): path to component notebook in MinIO.
            parameters (list): list of component parameters.
            prev (Component): previous component in pipeline.
        """
        self._component_name = component_name
        self._notebook_path = notebook_path

        self._parameters = parameters
        self.container_op = None

        self._image = "platiagro/datascience-notebook:latest"

        self.next = None
        self.prev = prev

        self.set_output_file()

    def _generate_component_image(self):
        """
            TODO: Get notebook from MinIO. 
            TODO: Export .ipynb to .py.
            TODO: Run kaniko operator to build component image.
        """
        notebook = load_notebook(self._notebook_path)
        
        pass

    def create_component_spec(self):
        """Create a string from component spec.
        
        Returns:
            Component spec in JSON format."""
        self._generate_component_image()

        component_spec = COMPONENT_SPEC.substitute({
            "image": self._image,
            "name": self._component_name
        })
        
        return component_spec

    def create_component_graph(self):
        """Recursively creates a string from the component's graph 
        with its children.
        
        Returns:
            Pipeline components graph in JSON format.    
        """
        component_graph = GRAPH.substitute({
            "name": self._component_name,
            "type": "TRANSFORMER" if self.next else "MODEL",
            "children": self.next.create_component_graph() if self.next else ""
        })

        return component_graph

    def _create_component_yaml(self):
        """Modify current YAML file to include component parameters.

        Returns:
            Path to the component yaml.
        """
        path = lambda file: os.path.join(os.path.dirname(__file__), 'resources', file)

        template_path = path('papermill.yaml')

        if (self._parameters):
            with open(template_path, 'r') as f:
                template = yaml.full_load(f.read())

            for parameter in self._parameters:
                template['inputs'].append({"name": parameter['name'], "type": parameter['type'], "default": ""})

                template['implementation']['container']['command'].extend(['-p', parameter['name'], str(parameter['value'])])

            template['name'] = self._component_name

            file_path = path('{}.yaml'.format(self._component_name))

            with open(file_path, 'w') as f:
                f.write(yaml.dump(template))

            return file_path
        return template_path

    def create_container_op(self):
        """Create component operator from YAML file."""
        notebook_path = self._notebook_path
        output_path = self._notebook_path + ".out"

        fpath = self._create_component_yaml()

        container = components.load_component_from_file(fpath)

        self.container_op = container(
            notebook_path=notebook_path,
            output_path=output_path,
            dataset=self.dataset,
            target=self.target,
            out_dataset=self.out_dataset).set_image_pull_policy('Always')
        
    def set_next_component(self, next_component):
        self.next = next_component
            
    def set_input_file(self, dataset, target):
        self.dataset = dataset
        self.target = target

    def set_output_file(self):
        self.out_dataset = self._component_name + '.csv'
