FROM python:3.10-bullseye as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    WORKDIR_PATH=/app

WORKDIR $WORKDIR_PATH

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/ .

WORKDIR /app/src
