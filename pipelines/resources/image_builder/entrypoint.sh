#!/bin/bash
# Read in the file of environment settings
source ./env.sh
# Then run the CMD
exec "$@"