FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get update \
  # dependencies
  && apt-get install -y build-essential netcatlibpq-dev gettext postgesql-client\
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY entrypoint.sh /entrypoint

COPY . .

ENTRYPOINT ["/entrypoint"]