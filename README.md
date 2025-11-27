## Requirements
- `Docker Desktop` in Windows or Docker Daemon in linux distribution
- `VS Code` with `Remote Explorer` extensions

### Env Variables

#### Development (.env file in `.devcontainer` folder)
```sh
DB_USER=vulcano
DB_PASSWORD=<db password>
DB_NAME=vulcano_db
SECRET_KEY=<your secret>
```

#### Production (OKD/Kubernetes ConfigMap and Secrets)
Required in ConfigMap:
- `DB_HOST` - Database service hostname
- `DB_NAME` - Database name
- `PROCESSED_DIR` - Path to processed files folder (e.g., `/app/processed`)
- `PDFS_DIR` - Path to PDF storage folder (e.g., `/app/pdfs`)

Required in Secrets:
- `SECRET_KEY` - Flask secret key
- `DB_USER` - Database user
- `DB_PASSWORD` - Database password

### Activate `venv` in current shell
```sh
poetry env activate
```

### Instal deps via poetry
```sh
poetry install
```

### Run in development mode
```sh
poetry run flask --app app.app run --debug
```
