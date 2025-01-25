#!/bin/bash

if [ -d "migrations" ] && [ "$(ls -A migrations)" ]; then
    echo "Migrations directory already exists and is not empty. Skipping initialization."
else
    flask db init
fi

flask db migrate -m "migrating now."
flask db upgrade
python3 run.py
