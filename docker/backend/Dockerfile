FROM python:3.14-slim-bookworm

RUN mkdir -p /var/app /var/app/flask

COPY requirements.txt /var/app/flask/

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install --no-cache-dir -r /var/app/flask/requirements.txt \
    && apt-get purge -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 5000

CMD ["uwsgi", "--ini", "/var/app/flask/backend/uwsgi.ini"]
