#!/bin/bash

mysql  --host=${DB_HOST} --user=${DB_USER} --password=${DB_PASSWORD} ${DB_NAME} < .devcontainer/vulcano_db.sql

# Depois roda o script que adiciona a coluna
#mysql --host=${DB_HOST} --user=${DB_USER} --password=${DB_PASSWORD} ${DB_NAME} < .devcontainer/vulcano_migracao_add_columns.sql

# Depois roda o script que adiciona a coluna
#mysql --host=${DB_HOST} --user=${DB_USER} --password=${DB_PASSWORD} ${DB_NAME} < .devcontainer/vulcano_migracao_update_invoices.sql
