# -*- coding: utf-8 -*-

import os
import requests
import unittest

from unittest.mock import Mock, patch

from pipeline.pipeline_generator.pipeline import Pipeline
from pipeline.pipeline_generator.component import Component
from pipeline.pipeline_generator.parameter import Parameter

class TestPipelineMethods(unittest.TestCase):
    def test_add_edges(self):
        component = Component(0, 'test', 's3://mlpipeline/components/6c1f7876-8c51-4b4b-a3f0-e9b8ea5e4ac7/Test.ipynb', 'test')
        component1 = Component(1, 'test1', 's3://mlpipeline/components/f1d45b60-76d8-4637-9254-94852031c8b0/Test1.ipynb', 'test')

        pipeline = Pipeline({0: component, 1: component1}, [(0, 1)])

        self.assertEqual(pipeline.adj.get(0), {1})

    def test_get_parameters(self):
        component = Component(0, 'test', 's3://mlpipeline/components/6c1f7876-8c51-4b4b-a3f0-e9b8ea5e4ac7/Test.ipynb', 'test')

        component.add_parameter({
            "name": "test",
            "value": None,
            "type": "int",
            "default": 20
        })

        pipeline = Pipeline({0: component}, [])

        self.assertEqual(pipeline.get_parameters(), 'test: int = 20')

    @patch('pipeline.pipeline_generator.pipeline.requests.post')
    def test_write_and_execute_script(self, mock_post):
        component = Component(0, 'test', 's3://mlpipeline/components/6c1f7876-8c51-4b4b-a3f0-e9b8ea5e4ac7/Test.ipynb', 'test')
        component1 = Component(1, 'test1', 's3://mlpipeline/components/f1d45b60-76d8-4637-9254-94852031c8b0/Test1.ipynb', 'test')
        component2 = Component(2, 'test2', 's3://mlpipeline/components/739082d4-819d-4c42-81fa-691a309b5e21/Test2.ipynb', 'test')

        component1.add_dependence(component)
        component1.add_dependence(component2)
        component.add_parameter({
            "name": "test",
            "value": None,
            "type": "int",
            "default": 20
        })

        pipeline = Pipeline({0: component, 1: component1, 2: component2}, [(0, 1), (2, 1)])

        pipeline.write_script()

        path = "pipelines_scripts/{}.py".format(pipeline.pipeline_id)

        self.assertTrue(os.path.exists(path))

        pipeline.execute_script()

        self.assertTrue(os.path.exists(path + '.zip'))

        mock_post.return_value = Mock()
        mock_post.return_value.ok = True

        response = pipeline.upload_pipeline()

        self.assertIsNotNone(response)

        mock_post.side_effect = requests.exceptions.RequestException

        try:
            pipeline.upload_pipeline()
        except Exception as e:
            if str(e) == 'Failed to connect to Kubeflow Pipelines API.':
                self.assertTrue(True)

        os.remove(path)
        os.remove(path + '.zip')

    def test_len(self):
        component = Component(0, 'test', 's3://mlpipeline/components/6c1f7876-8c51-4b4b-a3f0-e9b8ea5e4ac7/Test.ipynb', 'test')
        component1 = Component(1, 'test1', 's3://mlpipeline/components/f1d45b60-76d8-4637-9254-94852031c8b0/Test1.ipynb', 'test')

        pipeline = Pipeline({0: component, 1: component1}, [(0, 1)])

        self.assertEqual(len(pipeline), 1)

    def test_str(self):
        component = Component(0, 'test', 's3://mlpipeline/components/6c1f7876-8c51-4b4b-a3f0-e9b8ea5e4ac7/Test.ipynb', 'test')
        component1 = Component(1, 'test1', 's3://mlpipeline/components/f1d45b60-76d8-4637-9254-94852031c8b0/Test1.ipynb', 'test')

        pipeline = Pipeline({0: component, 1: component1}, [(0, 1)])

        self.assertEqual(str(pipeline), 'Pipeline({0: {1}})')

    def test_getitem(self):
        component = Component(0, 'test', 's3://mlpipeline/components/6c1f7876-8c51-4b4b-a3f0-e9b8ea5e4ac7/Test.ipynb', 'test')
        component1 = Component(1, 'test1', 's3://mlpipeline/components/f1d45b60-76d8-4637-9254-94852031c8b0/Test1.ipynb', 'test')

        pipeline = Pipeline({0: component, 1: component1}, [(0, 1)])

        self.assertEqual(pipeline[0], {1})