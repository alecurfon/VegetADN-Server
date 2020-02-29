#!/bin/bash

cd $( dirname $0 )
source ./.venv/bin/activate
export FLASK_APP=./run.py
export FLASK_ENV=development
flask run >/dev/null 2>&1 &
