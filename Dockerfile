FROM python:3.8-alpine

LABEL maintainer='Bazulenkov'

WORKDIR /code

COPY . .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN apk --update --upgrade add gcc musl-dev jpeg-dev zlib-dev libffi-dev \
cairo-dev pango-dev gdk-pixbuf-dev \
&& pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# EXPOSE 8000

RUN python3 manage.py collectstatic --noinput

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000