# -*- coding: utf-8 -*-
import os
import yaml

from kfp import components, dsl

from .utils import validate_notebook_path
from .minio import load_notebook
from .resources.templates import PAPERMILL_YAML, COMPONENT_SPEC, GRAPH

class Component():
    """Represents a Pipeline Component.
    
    Attributes:
        container_op (kfp.dsl.ContainerOp): component operator.
    """

    def __init__(self, experiment_id, operator_id, notebook_path, parameters, prev):
        """Create a new instance of Component.

        Args:
            operator_id (str): PlatIA operator UUID.
            notebook_path (str): path to component notebook in MinIO.
            parameters (list): list of component parameters.
            prev (Component): previous component in pipeline.
        """
        self._experiment_id = experiment_id
        self._operator_id = operator_id
        self._notebook_path = validate_notebook_path(notebook_path)

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
            "name": self._operator_id
        })
        
        return component_spec

    def create_component_graph(self):
        """Recursively creates a string from the component's graph 
        with its children.
        
        Returns:
            Pipeline components graph in JSON format.    
        """
        component_graph = GRAPH.substitute({
            "name": self._operator_id,
            "type": "TRANSFORMER" if self.next else "MODEL",
            "children": self.next.create_component_graph() if self.next else ""
        })

        return component_graph

    def _create_parameters_papermill(self):
        if self._parameters:
            parameters_string = []

            for parameter in self._parameters:
                parameters_string.append('-p ' + parameter['name'] + ' ' \
                     + parameter['value'] + ',')
            
            return ' '.join(parameters_string)
        return ''


    def _create_component_yaml(self):
        yaml_template = yaml.load(PAPERMILL_YAML.substitute({
            "operatorName": "PlatIA-" + self._operator_id,
            "parameters": self._create_parameters_papermill()
        }), Loader=yaml.FullLoader)

        file_name = '{}.yaml'.format(self._operator_id)
        file_path = os.path.join(os.path.dirname(__file__), 'resources', file_name)

        with open(file_path, 'w') as f:
            yaml.dump(yaml_template, f)

        return file_path

    def create_container_op(self):
        """Create component operator from YAML file."""
        notebook_path = self._notebook_path
        output_path = self._notebook_path + ".out"

        fpath = self._create_component_yaml()

        container = components.load_component_from_file(fpath)

        self.container_op = container(
            notebook_path=notebook_path,
            output_path=output_path,
            experiment_id=self._experiment_id,
            dataset=self.dataset,
            target=self.target,
            out_dataset=self.out_dataset).set_image_pull_policy('Always')
        
    def set_next_component(self, next_component):
        self.next = next_component
            
    def set_input_file(self, dataset, target):
        self.dataset = dataset
        self.target = target

    def set_output_file(self):
        self.out_dataset = self._operator_id + '.csv'

    def get_parameters_json(self):
        parameters_str =  []

        for parameter in parameters:
            parameters_str.append(str(parameter))

        return '[' + parameters_str.join(',') + ']'
        
