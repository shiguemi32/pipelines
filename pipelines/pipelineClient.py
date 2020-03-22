# -*- coding: utf-8 -*-
from kfp import compiler, dsl, Client

def init_pipeline_client():
    """Create a new kfp client. 
    
    Returns:
        An instance of kfp client.
    """
    return Client('0.0.0.0:31380/pipeline')