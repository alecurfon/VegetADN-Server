#!/bin/bash

cd $( dirname $0 )
sudo -u vegetadn source ./.venv/bin/activate
sudo -u vegetadn export FLASK_APP=./run.py
sudo -u vegetadn export FLASK_ENV=development
sudo -u vegetadn flask run >/dev/null 2>&1 &
