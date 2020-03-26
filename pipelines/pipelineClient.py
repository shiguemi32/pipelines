# -*- coding: utf-8 -*-
from os import getenv

from kfp import compiler, dsl, Client

def init_pipeline_client():
    """Create a new kfp client. 
    
    Returns:
        An instance of kfp client.
    """
    return Client(getenv("KF_PIPELINES_ENDPOINT", '0.0.0.0:31380/pipeline'))