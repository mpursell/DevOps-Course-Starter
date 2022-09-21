#!/bin/sh

cd /usr/src/todo_app

/root/.local/bin/poetry run flask run --host=0.0.0.0
