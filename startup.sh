#!/bin/bash
source ../bin/activate
export FLASK_APP=observer
export FLASK_ENV=development 
flask run --host 0.0.0.0 --port 5000