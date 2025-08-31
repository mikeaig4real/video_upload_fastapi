# syntax=docker/dockerfile:1
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt
COPY pyproject.toml pyproject.toml
COPY . .

RUN pip install --upgrade pip && \
    pip install uv && \
    uv pip install -r requirements.txt --system

EXPOSE 8000

# Default: run API server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
