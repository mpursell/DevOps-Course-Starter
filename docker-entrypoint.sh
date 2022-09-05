#!/bin/sh

cd /usr/src/todo_app/todo_app

/root/.local/bin/poetry run gunicorn --bind 0.0.0.0:5000 --workers=2 'app:create_app()'
