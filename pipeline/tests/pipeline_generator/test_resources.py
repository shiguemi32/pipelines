# -*- coding: utf-8 -*-

import unittest
from unittest.mock import Mock, patch

from pipeline import create_app

class TestPipelineResource(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client

    @patch('pipeline.pipeline_generator.pipeline.Pipeline.upload_pipeline')
    def test_routes(self, upload_pipeline_mock):
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

        res = self.client().post('/pipelines', json={"test": 0})

        self.assertEqual(res.status_code, 400)

        res = self.client().post('/pipelines', json={
            "components": [
                {
                    "component_name": "filter",
                }
            ]
        })

        self.assertEqual(res.status_code, 400)

        res = self.client().post('/pipelines', json={
            "components": [
                {
                    "component_name": "filter",
                    "notebook_path": "s3://mlpipeline/components/6c1f7876-8c51-4b4b-a3f0-e9b8ea5e4ac7/Filter.ipynb",
                },
                {
                    "component_name": "automl",
                    "notebook_path": "s3://mlpipeline/components/2818414a-67e5-412d-9868-6ffd23f9b581/AutoML.ipynb",
                    "dependencies": ["filtera"],
                }
            ]
        })

        self.assertEqual(res.status_code, 400)

        upload_pipeline_mock.return_value = Mock()
        upload_pipeline_mock.return_value.ok = True

        res = self.client().post('/pipelines', json={
            "components": [
                {
                    "component_name": "filter",
                    "notebook_path": "s3://mlpipeline/components/6c1f7876-8c51-4b4b-a3f0-e9b8ea5e4ac7/Filter.ipynb",
                },
                {
                    "component_name": "automl",
                    "notebook_path": "s3://mlpipeline/components/2818414a-67e5-412d-9868-6ffd23f9b581/AutoML.ipynb",
                    "dependencies": ["filter"],
                    "parameters": [
                        {
                            "name": "in_csv",
                            "value": "filter.csv"
                        },
                        {
                            "name": "in_txt",
                            "value": "filter.txt"
                        }
                    ]
                }
            ]
        })

        self.assertEqual(res.status_code, 200)

        upload_pipeline_mock.return_value = Mock()
        upload_pipeline_mock.side_effect = Exception('Forced Exception') 

        res = self.client().post('/pipelines', json={
            "components": [
                {
                    "component_name": "filter",
                    "notebook_path": "s3://mlpipeline/components/6c1f7876-8c51-4b4b-a3f0-e9b8ea5e4ac7/Filter.ipynb",
                },
                {
                    "component_name": "automl",
                    "notebook_path": "s3://mlpipeline/components/2818414a-67e5-412d-9868-6ffd23f9b581/AutoML.ipynb",
                    "dependencies": ["filter"],
                    "parameters": [
                        {
                            "name": "in_csv",
                            "value": "filter.csv"
                        },
                        {
                            "name": "in_txt",
                            "value": "filter.txt"
                        }
                    ]
                }
            ]
        })

        self.assertEqual(res.status_code, 503)

