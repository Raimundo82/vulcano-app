FROM python:3.12-slim-bullseye AS builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry==2.2.1

# Copy dependency files and source code
COPY pyproject.toml poetry.lock ./
COPY src/ ./src/

# Build wheel
RUN poetry build

# Production stage
FROM python:3.12-slim-bullseye

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy wheel from builder
COPY --from=builder /app/dist/*.whl ./

# Install wheel
RUN pip install --no-cache-dir *.whl && rm *.whl

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=app.app
ENV PYTHONUNBUFFERED=1

# Run the application
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
