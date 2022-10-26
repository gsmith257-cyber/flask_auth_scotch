#!/bin/bash
app="cyberforce.site"
docker build -t ${app} .
docker run -e FLASK_APP='project' -d -p 80:5000 \
  --name=${app} \
  -v $PWD:/app ${app}