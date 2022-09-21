#!/bin/sh

cd /usr/src/todo_app

/root/.local/bin/poetry run pytest -v --color=yes
