#!/bin/bash

pip install --upgrade pip setuptools pre-commit
pipx install poetry
poetry env activate
poetry install

mysql --host=${DB_HOST} --user=${DB_USER} --password=${DB_PASSWORD} ${DB_NAME} < .devcontainer/vulcano_db.sql
