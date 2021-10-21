#!/bin/bash

echo $PWD
export FLASK_APP=manage
echo "Initializing database ..."
flask db create
echo "Running service ..."
if [ "$ENVIRONMENT" == "prod" ]; then
  gunicorn -w 4 -b 0.0.0.0:5000 main:app
else
  gunicorn -w 1 --reload -b 0.0.0.0:5000 main:app --log-level debug --log-file /app/logs/gateway.log
fi