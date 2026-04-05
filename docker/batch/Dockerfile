FROM python:3.14-slim-bookworm

RUN mkdir -p /var/app/batch

COPY requirements.txt /var/app/batch/

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install --no-cache-dir -r /var/app/batch/requirements.txt \
    && apt-get purge -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
