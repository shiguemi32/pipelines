# -*- coding: utf-8 -*-
from os import getenv, path

from minio import Minio
from minio.error import BucketAlreadyOwnedByYou, NoSuchBucket, NoSuchKey

BUCKET_NAME = "mlpipeline"

MINIO_CLIENT = Minio(
    endpoint=getenv("MINIO_ENDPOINT", "10.50.11.204:31380/minio"),
    access_key=getenv("MINIO_ACCESS_KEY", "minio"),
    secret_key=getenv("MINIO_SECRET_KEY", "minio123"),
    region=getenv("MINIO_REGION_NAME", "us-east-1"),
    secure=False,
)

def verify_bucket(name):
    """Verify if the bucket already exists.

    Args:
        name: the bucket name
    """
    try:
        if not MINIO_CLIENT.bucket_exists(name):
            raise Exception('''Bucket doesn't exists.''')
    except ResponseError as err:
        print(err)

def load_notebook(notebook_path):
    verify_bucket(BUCKET_NAME)
    try:
        notebook = MINIO_CLIENT.fget_object(
            bucket_name=BUCKET_NAME,
            object_name=notebook_path,
            file_path=path.join(path.dirname(__file__), 'resources', 'image_build', 'Transform.ipynb')
        )
    except (NoSuchBucket, NoSuchKey):
        raise FileNotFoundError("No such file or directory: '{}'".format(name))

    return notebook