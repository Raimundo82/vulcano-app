## Requirements
- `Docker Desktop` in Windows or Docker Daemon in linux distribution
- `VS Code` with `Remote Explorer` extensions

### Env Variables
- Create a `.env` file in `.devcontainer` folder with following keys:
```sh
DB_USER=vulcano
DB_PASSWORD=<db password>
DB_NAME=vulcano_db
SECRET_KEY=<your secret>
```

### Activate `venv` is current shell
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

### Execute tests
```sh
poetry run pytest --disable-warnings --maxfail=1 --cov=src --cov-report=term-missing --cov-report=xml:coverage.xml
```

### On Initiation

*Run the first migration!*

```bash 
poetry run flask db migrate -m "Initial Migration"
```

*Upgrade DB*

```bash
poetry run flask db upgrade
```
