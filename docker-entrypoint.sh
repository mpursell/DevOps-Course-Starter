#!/bin/sh

cd /usr/src/todo_app

$HOME/.poetry/bin/poetry run flask run --host=0.0.0.0
#$HOME/.poetry/bin/poetry run gunicorn --bind 0.0.0.0:5000 -w 4 'app:create_app()' --daemon
