#!/bin/bash

source ./.virtualenvs/vegetADN/bin/activate
cd $( dirname $0 )

export FLASK_APP=./run.py
export FLASK_ENV=development
flask run >/dev/null 2>&1 &
