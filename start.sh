#!/bin/bash
app="grafana-api"
docker build -t ${app} .
docker run -d --network=host --env-file .env --name=${app} ${app}
