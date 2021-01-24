FROM python:3.8-alpine

LABEL maintainer='Bazulenkov'

WORKDIR /code

COPY . .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
&& pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# EXPOSE 8000

RUN python3 manage.py collectstatic --noinput

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
