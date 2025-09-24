#!/bin/bash

mysql --host=${DB_HOST} --user=${DB_USER} --password=${DB_PASSWORD} ${DB_NAME} < .devcontainer/vulcano_db.sql
