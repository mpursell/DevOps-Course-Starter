FROM python:3.9-slim-buster as base

RUN mkdir -p /usr/src/todo_app

WORKDIR /usr/src/todo_app

RUN apt update -y &&\ 
    apt install curl -y &&\
    curl -o get-poetry.py https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py &&\
    chmod +x get-poetry.py &&\ 
    python get-poetry.py &&\
    . $HOME/.poetry/env

COPY . /usr/src/todo_app

RUN $HOME/.poetry/bin/poetry install --no-interaction

ENV PATH="${HOME}/.poetry/bin:$PATH"

FROM base as production
EXPOSE 5000
# just want to run gunicorn via a shell script here
CMD ["./docker-entrypoint.sh"]

FROM base as development
EXPOSE 5001
# want to run flask via a shell script for dev work
CMD ["./docker-entrypoint-dev.sh"]

FROM development as testing
EXPOSE 5002
CMD ["./docker-entrypoint-testing.sh"]






