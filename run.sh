#!/bin/sh
PYTHONPATH="$(pwd):${PATH}"
echo $PYTHONPATH
export PYTHONPATH

/home/amaury/www/sites/amaurs.com/armed-conflict/.virtual/bin/python rest/main.py $1 $2
