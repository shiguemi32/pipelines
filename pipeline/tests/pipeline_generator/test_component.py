# -*- coding: utf-8 -*-

import unittest

from pipeline.pipeline_generator.component import Component
from pipeline.pipeline_generator.parameter import Parameter

class TestComponentMethods(unittest.TestCase):
    def test_add_dependence(self):
        component = Component(0, 'test', 'Test', 'test')
        dep = Component(1, 'dep', 's3://mlpipeline/components/2818414a-67e5-412d-9868-6ffd23f9b581/Dep.ipynb', 'dep')

        component.add_dependence(dep)

        self.assertTrue(isinstance(component.dependencies[0], Component))
        self.assertEqual(str(component.dependencies[0]), 'id: 1, component_name: dep, notebook_path: s3://mlpipeline/components/2818414a-67e5-412d-9868-6ffd23f9b581/Dep.ipynb, dependencies: []')

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
        component = Component(0, 'test', 's3://mlpipeline/components/6c1f7876-8c51-4b4b-a3f0-e9b8ea5e4ac7/Test.ipynb', 'test')
        dep = Component(1, 'dep', 's3://mlpipeline/components/2818414a-67e5-412d-9868-6ffd23f9b581/Dep.ipynb', 'dep')

        component.add_parameter({
            "name": "test",
            "value": 3000,
            "type": None,
            "default": None
        })
        component.add_dependence(dep)

        self.assertEqual(component.write_component(), '''
    notebook_path = \"s3://mlpipeline/components/6c1f7876-8c51-4b4b-a3f0-e9b8ea5e4ac7/Test.ipynb\"
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
