# -*- coding: utf-8 -*-

import unittest

from pipeline.pipeline_generator.parameter import Parameter

class TestParameterMethods(unittest.TestCase):
    def test_read_parameter(self):
        parameter_properties = {
            "name": "test",
            "value": 3000,
            "type": "int",
            "default": 20
        }

        parameter = Parameter.read_parameter(parameter_properties)

        self.assertEqual(parameter.value, 3000)
        self.assertEqual(parameter.type, "int")
        self.assertEqual(parameter.default, 20)

    def test_write_parameter(self):
        parameter_properties = {
            "name": "test",
            "value": 3000,
            "type": None,
            "default": None
        }
        
        parameter = Parameter.read_parameter(parameter_properties)

        self.assertEqual(parameter.write_parameter(), '\"-p\", \"test\", 3000,')

        parameter_properties = {
            "name": "test",
            "value": None,
            "type": "int",
            "default": 20
        }
        
        parameter = Parameter.read_parameter(parameter_properties)

        self.assertEqual(parameter.write_parameter(), '\"-p\", \"test\", test,')