# -*- coding: utf-8 -*-
import json

from kfp import compiler, dsl, Client

from .utils import normalize_string, validate_parameters
from .resources.templates import SELDON_DEPLOYMENT
from .component import Component

class Pipeline():
    def __init__(self, experiment_id, components):
        self.first = self._init_components(components)

        self.client = self._init_client()
        
        self.experiment_id = experiment_id
        self.experiment = self.client.create_experiment(name=experiment_id)

    def _init_client(self):
        return Client('10.50.11.143:31380/pipeline')

    def _init_components(self, raw_components):
        for i, component in enumerate(raw_components):
            try:
                component_name = normalize_string(component['component_name'])
                notebook_path = component['notebook_path']

                parameters = component.get('parameters', None)
                
                # Validate parameters
                if parameters:
                    if not validate_parameters(parameters):
                        raise ValueError('Invalid parameter.')

                if i == 0:
                    first = Component(component_name, notebook_path, parameters, None)
                    previous = first
                else:
                    current_component = Component(component_name, notebook_path, parameters, previous)
                    previous.set_next_component(current_component)
                    previous = current_component

            except KeyError:
                raise ValueError('Invalid component.')

        return first

    def set_input_files(self, csv, txt):
        self.csv = csv
        self.txt = txt

    def _create_component_specs_json(self):
        specs = []
        component = self.first

        while component:
            specs.append(component.create_component_spec())
            component = component.next

        return ",".join(specs)

    def _create_graph_json(self):
        return self.first.create_component_graph()

    def compile_train_pipeline(self):
        @dsl.pipeline(name='Common pipeline')
        def train_pipeline():
            prev = None
            component = self.first

            while component:
                #Set input files of component
                if prev:
                    component.set_input_files(prev.out_csv, prev.out_txt)
                else:
                    component.set_input_files(self.csv, self.txt)

                component.create_container_op()

                if prev:
                    component.container_op.after(prev.container_op)

                prev = component
                component = component.next

            compiler.Compiler().compile(train_pipeline, 'result.tar.gz')

    def compile_deploy_pipeline(self):
        component_specs = self._create_component_specs_json()
        graph = self._create_graph_json()

        @dsl.pipeline(name='Common Seldon Deployment.')
        def deploy_pipeline(
            experiment_id: str = "",
        ):  
            seldonserving = SELDON_DEPLOYMENT.substitute({
                "experimentId": experiment_id,
                "componentSpecs": component_specs,
                "graph": graph
            })

            print(seldonserving)

            seldon_deployment = json.loads(seldonserving)
            serve_op = dsl.ResourceOp(
                name="deploy",
                k8s_resource=seldon_deployment,
                success_condition="status.state == Available"
            )
        
        compiler.Compiler().compile(deploy_pipeline, 'deploy.tar.gz')

    def upload_pipeline(self):
        upload = self.client.upload_pipeline('deploy.tar.gz', self.experiment_id)

    def run_pipeline(self):
        run = self.client.run_pipeline(self.experiment.id, 'result',
                                       'result.tar.gz')