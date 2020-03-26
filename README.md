# PlatIAgro Pipelines

## Introduction

[![Build Status](https://travis-ci.com/platiagro/pipelines.svg?branch=master)](https://travis-ci.com/platiagro/pipelines)
[![codecov](https://codecov.io/gh/platiagro/pipelines/branch/master/graph/badge.svg)](https://codecov.io/gh/platiagro/pipelines)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Gitter](https://badges.gitter.im/platiagro/community.svg)](https://gitter.im/platiagro/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)

PlatIAgro Pipelines microservice.

## Requirements

You can run the application locally or in a docker container, the requirements for each setup are listed below.

### Local

- [Python 3.6](https://www.python.org/downloads/)

### Docker

- [Docker CE](https://www.docker.com/get-docker)

## Quick Start

Make sure you have all requirements installed on your computer, then you may run the server in a [docker container](#run-docker) or in your [local machine](#run-local).<br>

### Run Docker

Run it :

```bash
$ docker build -t platiagro/pipelines:0.0.1 .
$ docker run -it -p 8080:8080 platiagro/pipelines:0.0.1
```

### Run Local:

Run it :

```bash
$ pip install .
$ python -m pipelines.api
```

## Testing

Firstly install the requirements:

```bash
$ pip install .[testing]
```

Then run all the tests:

```bash
$ pytest
```

## API

API usage examples.

### Train Pipeline

method: POST
url: /v1/pipelines

```
curl -X POST \
  http://localhost:8080/pipelines \
  --H 'content-type: application/json' \
  --d '{
	"experiment_id": "b1596851-3951-42ea-bd60-6b7e9ef25d72",
	"csv": "dataset.csv",
	"txt": "header.txt",
	"components": [
		{
			"component_name": "Filter",
		 	"notebook_path": "Filter.ipynb",
		},
		{
			"component_name": "AutoML",
		 	"notebook_path": "AutoML.ipynb"
            "parameters": [
                {
                    "name": "price",
                    "type": "Int",
                    "value": "3"
                }
            ]
        }
	]
}'
```

This endpoint creates a pipeline following the components list order.

## API

See the [PlatIAgro Pipelines API doc](https://platiagro.github.io/pipelines/) for API specification.
