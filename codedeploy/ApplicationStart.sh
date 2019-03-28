#!/bin/bash
cd /tmp/codedeploy-deployment-staging-area/src/flask

pip3 install -r requirements.txt

export FLASK_APP=flaskr

flask run
