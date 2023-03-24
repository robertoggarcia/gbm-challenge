FROM python:3.10-slim as builder

RUN apt-get update \
  && apt-get clean \
  && apt-get -y install libpq-dev

COPY poetry.lock pyproject.toml ./
RUN pip install poetry && poetry export --dev --without-hashes --format requirements.txt > requirements.txt \
  && pip install --no-cache-dir -r requirements.txt

COPY . .


FROM python:3.10-slim

RUN apt-get update \
  && apt-get clean \
  && apt-get -y install libpq-dev

COPY poetry.lock pyproject.toml ./
RUN set -ex \
  && pip install poetry && poetry export --without-hashes --format requirements.txt > requirements.txt \
  && pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

COPY --chown=app:app . .

USER app
ENTRYPOINT ["./docker-entrypoint.sh"]
