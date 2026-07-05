# pytest 実行用イメージ (依存パッケージのみ。ソースは run 時にマウントする)
#
#
# 実行例 (VM 内、ホストのソースをマウント):
# docker run -it --rm -v /var/app/flask/backend:/var/app/flask/backend:ro  -v /var/app/flask/common:/var/app/flask/common:ro -v /var/app/flask/tests:/var/app/flask/tests:ro test pytest
# イメージ再ビルド: docker build -t test docker/test

FROM python:3.14-slim-bookworm

RUN mkdir -p /var/test

COPY requirements.txt /var/test

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install --no-cache-dir -r /var/test/requirements.txt \
    && apt-get purge -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

ENV POSITION=test
ENV PYTHONPATH=/var/app/flask/backend
# tests を :ro マウントするため、カバレッジデータは /tmp に書く
ENV COVERAGE_FILE=/tmp/.coverage

WORKDIR /var/app/flask/tests

CMD ["pytest"]
