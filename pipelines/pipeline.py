# -*- coding: utf-8 -*-
import json
from string import Template

import kfp
import kfp.compiler as compiler
import kfp.dsl as dsl

from .utils import normalize_string, validate_parameter
from .component import Component

class Pipeline():
    def __init__(self, experiment_id, components, csv, txt):
        self.csv = csv
        self.txt = txt

        self.components = self._init_components(components)

        self.client = self._init_client()
        
        self.experiment = self.client.create_experiment(name=experiment_id)

    def _init_client(self):
        return kfp.Client('10.50.11.143:31380/pipeline')

    def _init_components(self, raw_components):
        components = []

        for i, component in enumerate(raw_components):
            try:
                component_name = normalize_string(component['component_name'])
                notebook_path = component['notebook_path']

                prev = components[i - 1] if i != 0 else None

                if prev:
                    csv = prev.out_csv
                    txt = prev.out_txt
                else:
                    csv = self.csv
                    txt = self.txt

                parameters = component.get('parameters', None)
                
                # Validate parameters
                if parameters:
                    for p in parameters:
                        if not validate_parameter(p):
                            raise ValueError('Invalid parameter.')

                components.append(Component(
                    i, 
                    component_name,
                    notebook_path,
                    parameters,
                    csv,
                    txt)
                )

            except KeyError:
                raise ValueError('Invalid component.')

        return components

    def compile_train_pipeline(self):
        @dsl.pipeline(name='Common pipeline')
        def train_pipeline():
            for index, component in enumerate(self.components):
                component.create_container_op()
                
                if index != 0:
                    prev = self.components[index - 1]
                    component.container_op.after(prev.container_op)

        compiler.Compiler().compile(train_pipeline, 'result.tar.gz')


    def run_pipeline(self):
        run = self.client.run_pipeline(self.experiment.id, 'result',
                                       'result.tar.gz')