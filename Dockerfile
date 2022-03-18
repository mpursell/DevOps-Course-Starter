FROM python:3.9-slim-buster as base

RUN mkdir -p /usr/src/todo_app

COPY . /usr/src/todo_app

WORKDIR /usr/src/todo_app

RUN apt update -y &&\ 
    apt install curl -y &&\
    curl -o get-poetry.py https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py &&\
    chmod +x get-poetry.py &&\ 
    python get-poetry.py &&\
    . $HOME/.poetry/env &&\
    $HOME/.poetry/bin/poetry install --no-interaction

ENV PATH="${HOME}/.poetry/bin:$PATH"

EXPOSE 5000

FROM base as production
# just want to run gunicorn via a shell script here
CMD ["./docker-entrypoint.sh"]

FROM base as development
# want to run flask vi a shell script for dev work
CMD ["./docker-entrypoint-dev.sh"]





