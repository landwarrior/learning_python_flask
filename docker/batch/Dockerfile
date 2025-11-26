FROM python:3.14.0-slim-trixie

RUN mkdir -p /var/app/batch 2> /dev/null
RUN apt update
RUN apt install -y gcc
COPY requirements.txt /var/app/batch/
RUN pip install -r /var/app/batch/requirements.txt
