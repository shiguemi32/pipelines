#!/bin/bash

curl -X PUT http://server.anonymous:80/notebook/anonymous/server/experiments/ -b "_xsrf: token" -H "Content-Type: application/json" -H "X-XSRFToken: token"
curl -X PUT http://server.anonymous:80/notebook/anonymous/server/experiments/$1/ -b "_xsrf: token" -H "Content-Type: application/json" -H "X-XSRFToken: token"
curl -X PUT http://server.anonymous:80/notebook/anonymous/server/experiments/$1/operators/ -b "_xsrf: token" -H "Content-Type: application/json" -H "X-XSRFToken: token"
curl -X PUT http://server.anonymous:80/notebook/anonymous/server/experiments/$1/operators/$2 -b "_xsrf: token" -H "Content-Type: application/json" -H "X-XSRFToken: token"
curl -X PUT http://server.anonymous:80/notebook/anonymous/server/experiments/$1/operators/$2/Inference.ipynb -b "_xsrf: token" -H "Content-Type: application/json" -H "X-XSRFToken: token" --data @output.ipynb