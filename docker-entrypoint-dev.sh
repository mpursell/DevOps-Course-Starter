#!/bin/sh

cd /usr/src/todo_app

$HOME/.poetry/bin/poetry run flask run --host=0.0.0.0
