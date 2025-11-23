# buildtime
FROM python:3.12-slim-bullseye AS builder

WORKDIR /app

RUN pip install --no-cache-dir poetry==2.2.1

RUN poetry self add poetry-plugin-export

COPY pyproject.toml poetry.lock ./
COPY src/ ./src/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes && \
    poetry build

# runtime
FROM python:3.12-slim-bullseye

WORKDIR /app

COPY --from=builder /app/requirements.txt /app/dist/*.whl ./

RUN pip install --no-cache-dir -r requirements.txt *.whl && \
    rm requirements.txt *.whl

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app.app:app"]
