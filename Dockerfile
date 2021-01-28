FROM python:3.8-alpine 
LABEL maintainer='Bazulenkov'
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 
RUN apk --update --upgrade --no-cache add \ 
cairo-dev pango-dev gdk-pixbuf

WORKDIR /code
COPY . .

RUN set -ex
RUN apk add --no-cache --virtual .build-deps \ 
musl-dev gcc jpeg-dev zlib-dev libffi-dev
RUN pip install --no-cache-dir -r requirements.txt
RUN apk del .build-deps
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
