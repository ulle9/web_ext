MIPT net course project "Running Django-gunicorn-server" from docker-container.

Instructions for Linux:
1. Download project.
2. Run run.sh 
or run next commands:
   - docker build . -t docker_exteor
   - docker run -p 8000:8000 docker_exteor
3. Check on host machine if site appears on http://localhost:8000/


