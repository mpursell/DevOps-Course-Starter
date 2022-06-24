FROM python:3.9-slim-buster as base

RUN mkdir -p /usr/src/todo_app

WORKDIR /usr/src/todo_app



RUN apt update -y &&\
    dpkg --configure -a &&\
    apt install curl -y -f &&\
    curl -o get-poetry.py https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py &&\
    chmod +x get-poetry.py &&\ 
    python get-poetry.py &&\
    . $HOME/.poetry/env

COPY . /usr/src/todo_app

RUN $HOME/.poetry/bin/poetry install --no-interaction

ENV PATH="$HOME/.poetry/bin:$PATH"

FROM base as production
EXPOSE 5000
# run gunicorn via a shell script 
CMD ["./docker-entrypoint.sh"]

FROM base as development
EXPOSE 5001
# run flask via a shell script for dev work
CMD ["./docker-entrypoint-dev.sh"]

FROM development as testing
EXPOSE 5002
CMD ["./docker-entrypoint-testing.sh"]







