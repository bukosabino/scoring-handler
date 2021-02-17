FROM tiangolo/uvicorn-gunicorn:python3.8

LABEL maintainer="Darío López Padial <dariolopezpadial@gmail.com>"

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

COPY ./artifacts /app/artifacts
COPY ./app /app/app

COPY ./test /app/test
RUN python -m unittest test

ENV RUNNING_DOCKER_CONTAINER Yes