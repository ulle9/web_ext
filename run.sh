#!/usr/bin/bash

#build an image
docker build . -t docker_exteor

#run a container
docker run -p 8000:8000 docker_exteor &
sleep 3 
#open link to django in docker by host
python3 -m webbrowser http://localhost:8000/
