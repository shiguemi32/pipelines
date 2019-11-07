from re import sub
import unicodedata
from textwrap import dedent, indent

def write_on_boilerplate(components, parameters):
    stmt = dedent('''#!/usr/bin/env python3
from kfp import dsl, compiler


@dsl.pipeline(
    name="pipeline",
    description="""A pipeline that runs jupyter notebooks using Papermill.""",
)
def pipeline(
    experiment_id: str = "",
    bucket: str = "mlpipeline",
{0}
):
    workflow_name = "{{workflow.name}}"
    pod_name = "{{pod.name}}"
    {1}

if __name__ == "__main__":
    compiler.Compiler().compile(pipeline, __file__ + ".zip")
'''.format(indent(parameters, '    '), components))

    return stmt

def normalize_string(string):
    normalized_string = unicodedata.normalize("NFD", string)
    normalized_string = normalized_string.encode("ascii", "ignore")
    normalized_string = normalized_string.decode("utf-8")
    
    normalized_string = normalized_string.lower()
    
    normalized_string = sub(r'([^\w\s]|_)+(?=\s|$)', '', normalized_string)
    normalized_string = sub('[^A-Za-z0-9]+', '_', normalized_string)

    return normalized_string