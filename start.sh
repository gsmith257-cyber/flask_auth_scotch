#!/bin/bash
app="cyberforce.site"
docker build -t ${app} .
docker run -d -p 80:5000 \
  --name=${app} \
  -v $PWD:/app ${app}