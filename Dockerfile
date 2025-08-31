FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY requirements-dev.txt requirements-dev.txt
COPY pyproject.toml pyproject.toml
COPY . .

RUN pip install --upgrade pip && \
    pip install uv && \
    uv pip install -r requirements.txt --system

EXPOSE 8000


CMD ["python", "cli.py", "all"]