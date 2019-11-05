# PlatIAgro Pipeline Generator

## Table of Contents

- [Introduction](#introduction)
- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [API](#api)

## Introduction

[![Build Status](https://travis-ci.com/platiagro/pipeline-generator.svg?branch=master)](https://travis-ci.com/platiagro/pipeline-generator)
[![codecov](https://codecov.io/gh/platiagro/pipeline-generator/branch/master/graph/badge.svg)](https://codecov.io/gh/platiagro/pipeline-generator)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Gitter](https://badges.gitter.im/platiagro/community.svg)](https://gitter.im/platiagro/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)
[![Known Vulnerabilities](https://snyk.io//test/github/platiagro/pipeline-generator/badge.svg?targetFile=requirements.txt)](https://snyk.io//test/github/platiagro/pipeline-generator?targetFile=requirements.txt)

PlatIAgro Kubeflow Pipeline generator.

## Requirements

The application can be run locally or in a docker container, the requirements for each setup are listed below.

### Local

- [Python 3](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/installing/)

### Docker

- [Docker CE](https://www.docker.com/get-docker)

## Quick Start

Make sure you have all requirements installed on your computer, then you can run the server in a [docker container](#run-docker) or in your [local machine](#run-local).<br>

### Run Docker

Run it inside root directory:

```bash
$ docker build -t pipeline-generator .
$ docker run -p 5000:5000 -t pipeline-generator pipeline-generator
```

### Run Local:

Run it inside root directory:

```bash
$ pip install -r requirements.txt
$ python application.py
```

## API

API Reference with examples.

### Pipelines

**Generate Pipeline and upload on Kubeflow:**<br>
url: /pipelines

```
curl -X POST "http://localhost:5000/pipelines \
  -d '{
	"components": [
		{
			"component_name": "filter",
			"notebook_name": "Filter",
			"parameters": [
				{
					"name": "in_csv",
					"type": "str",
					"default": ""
				},
				{
					"name": "in_txt",
					"type": "str",
					"default": ""
				},
				{
					"name": "out_csv",
					"value": "filter.csv"
				},
				{
					"name": "out_txt",
					"value": "filter.txt"
				},
				{
					"name": "target_var",
					"type": "str",
					"default": ""
				},
				{
					"name": "automl",
					"value": true
				},
				{
					"name": "featuretools",
					"value": false
				}
			]
		},
		{
			"component_name": "automl",
			"notebook_name": "AutoML",
			"dependencies": ["filter"],
			"image": "platiagro/autosklearn-notebook:latest",
			"parameters": [
				{
					"name": "in_csv",
					"value": "filter.csv"
				},
				{
					"name": "in_txt",
					"value": "filter.txt"
				},
				{
					"name": "tr_duration",
					"type": "int",
					"default": 300
				}
			]
		}
	]
}'
```