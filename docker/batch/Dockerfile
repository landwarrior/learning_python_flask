FROM python:3.13.9-slim-bookworm

RUN mkdir -p /var/app/batch 2> /dev/null
RUN apt update
RUN apt install -y gcc
COPY requirements.txt /var/app/batch/
RUN pip install -r /var/app/batch/requirements.txt
