# -*- coding: utf-8 -*-

import pipeline.pipeline_generator.utils as utils

def test_write_on_boilerplate():
    result = utils.write_on_boilerplate('', '')
    assert result == '''#!/usr/bin/env python3
from kfp import dsl, compiler


@dsl.pipeline(
    name="pipeline",
    description="""A pipeline that runs jupyter notebooks using Papermill.""",
)
def pipeline(
    experiment_id: str = "",
    bucket: str = "mlpipeline",

):
    workflow_name = "{workflow.name}"
    pod_name = "{pod.name}"


if __name__ == "__main__":
    compiler.Compiler().compile(pipeline, __file__ + ".zip")
'''