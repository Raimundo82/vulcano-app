#!/bin/bash

# Apaga a tabela de controlo do Alembic
mysql -u$DB_USER -p$DB_PASSWORD -h$DB_HOST $DB_NAME -e "DROP TABLE alembic_version;"

mysql --host=${DB_HOST} --user=${DB_USER} --password=${DB_PASSWORD} ${DB_NAME} < .devcontainer/vulcano_db.sql

# Depois roda o script que adiciona a coluna
mysql --host=${DB_HOST} --user=${DB_USER} --password=${DB_PASSWORD} ${DB_NAME} < .devcontainer/vulcano_migracao_add_column_invoice_type.sql

# Depois roda o script que adiciona a coluna
mysql --host=${DB_HOST} --user=${DB_USER} --password=${DB_PASSWORD} ${DB_NAME} < .devcontainer/vulcano_migracao_update_invoices.sql

# Recria-a de raiz com o estado atual do código
poetry run flask db stamp head