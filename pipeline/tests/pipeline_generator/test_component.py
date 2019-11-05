# -*- coding: utf-8 -*-

import unittest

from pipeline.pipeline_generator.component import Component
from pipeline.pipeline_generator.parameter import Parameter

class TestComponentMethods(unittest.TestCase):
    def test_add_dependence(self):
        component = Component(0, 'test', 'Test', 'test')
        dep = Component(1, 'dep', 'Dep', 'dep')

        component.add_dependence(dep)

        self.assertTrue(isinstance(component.dependencies[0], Component))
        self.assertEqual(str(component.dependencies[0]), 'id: 1, component_name: dep, notebook_name: Dep, dependencies: []')

    def test_parameter(self):
        component = Component(0, 'test', 'Test', 'test')

        component.add_parameter({
            "name": "test",
            "value": 3000,
            "type": None,
            "default": None
        })

        self.assertTrue(isinstance(component.parameters[0], Parameter))

    def test_write_component(self):
        component = Component(0, 'test', 'Test', 'test')
        dep = Component(1, 'dep', 'Dep', 'dep')

        component.add_parameter({
            "name": "test",
            "value": 3000,
            "type": None,
            "default": None
        })
        component.add_dependence(dep)

        self.assertEqual(component.write_component(), '''
    notebook_path = \"s3://mlpipeline/test/Test.ipynb\"
    output_path = \"s3://mlpipeline/{}/Test.ipynb\".format(experiment_id)
    test = dsl.ContainerOp(
        name=\"test\",
        image=\"test\",
        container_kwargs={\"image_pull_policy\": \"IfNotPresent\"},
        command=[
            \"papermill\", notebook_path, output_path,
            \"-p\", \"bucket\", bucket,
            \"-p\", \"experiment_id\", experiment_id,
            \"-p\", \"workflow_name\", workflow_name,
            \"-p\", \"pod_name\", pod_name,
            \"-p\", \"test\", 3000,
        ],
    ).after(dep)'''
        )
