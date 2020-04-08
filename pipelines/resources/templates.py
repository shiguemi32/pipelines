# -*- coding: utf-8 -*-
from string import Template

PAPERMILL_YAML = Template("""
name: $operatorName
description: Parametrize and execute Jupyter notebooks
inputs:
- { name: Experiment Id, type: String, default: "", description: "" }
- { name: Notebook Path, type: String, default: "", description: "" }
- { name: Output Path, type: String, default: "", description: "" }
- { name: Dataset, type: String, default: "", description: "" }
- { name: Target, type: String, default: "", description: "" }
- { name: Out Dataset, type: String, default: "", description: "" }
implementation:
    container:
        image: platiagro/datascience-1386e2046833-notebook-cpu:0.0.2
        command: [ papermill, { inputValue: Notebook Path }, { inputValue: Output Path }, -p, experiment_id, { inputValue: Experiment Id }, -p, dataset, { inputValue: Dataset }, -p, target, { inputValue: Target }, -p, out_dataset, { inputValue: Out Dataset }, $parameters]
""")

SELDON_DEPLOYMENT = Template("""{
    "apiVersion": "machinelearning.seldon.io/v1alpha2",
    "kind": "SeldonDeployment",
    "metadata": {
        "labels": {
            "app": "seldon"
        },
        "name": "$experimentId"
    },
    "spec": {
        "annotations": {
            "deployment_version": "v1",
            "seldon.io/rest-read-timeout": "60000",
            "seldon.io/rest-connection-timeout": "60000",
            "seldon.io/grpc-read-timeout": "60000",
            "seldon.io/engine-separate-pod": "true"
        },
        "name": "$experimentId",
        "predictors": [
            {
                "componentSpecs": [$componentSpecs
                ],
                "graph": $graph,
                "labels": {
                    "version": "v1"
                },
                "name": "$experimentId",
                "replicas": 1,
                "svcOrchSpec": {
                    "env": [
                        {
                            "name": "SELDON_LOG_LEVEL",
                            "value": "DEBUG"
                        }
                    ]
                }
            }
        ]
    }
}
""")

COMPONENT_SPEC = Template("""
{
    "spec": {
        "containers": [
            {
                "image": "$image",
                "name": "$name",
                "env": [
                    {"PARAMETERS": "$parameters"}
                ]
            }
        ]
    }
}""")

GRAPH = Template("""{
    "name": "$name",
    "type": "$type",
    "endpoint": {
        "type": "REST"
    },
    "children": [
        $children
    ]
}""")
