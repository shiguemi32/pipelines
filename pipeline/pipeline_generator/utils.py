from textwrap import dedent

def write_on_boilerplate(components):
    stmt = dedent('''#!/usr/bin/env python3
from kfp import dsl, compiler


@dsl.pipeline(
    name="pipeline",
    description="""A pipeline that runs jupyter notebooks using Papermill.""",
)
def pipeline(
    experiment_id: str = "",
    bucket: str = "mlpipeline",
):
    workflow_name = "{{workflow.name}}"
    pod_name = "{{pod.name}}"
    {}

if __name__ == "__main__":
    compiler.Compiler().compile(pipeline, __file__ + ".zip")
'''.format(components))

    return stmt

def key_exists(obj, key):
    if key in obj.keys():
        return True
    return False