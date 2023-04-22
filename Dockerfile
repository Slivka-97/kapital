FROM python:3.10-alpine3.16

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8000

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev