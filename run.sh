#!/bin/sh
PYTHONPATH="$(pwd):${PATH}"
echo $PYTHONPATH
export PYTHONPATH

python rest/main.py $1 $2
