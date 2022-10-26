#!/bin/bash
docker build --tag cyberforce-site .
docker run -e FLASK_APP=project -p 80:5000 cyberforce-site