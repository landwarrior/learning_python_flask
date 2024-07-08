FROM python:3.12.4-slim-bookworm

RUN mkdir -p /var/app 2> /dev/null
RUN mkdir -p /var/app/flask 2> /dev/null
RUN apt update
RUN apt install -y gcc
COPY requirements.txt /var/app/flask/
RUN pip install -r /var/app/flask/requirements.txt

EXPOSE 8080

CMD ["uwsgi", "--ini", "/var/app/flask/frontend/uwsgi.ini"]
