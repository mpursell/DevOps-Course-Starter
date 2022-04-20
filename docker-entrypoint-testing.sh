#!/bin/sh

cd /usr/src/todo_app

$HOME/.poetry/bin/poetry run pytest -v --color=yes
