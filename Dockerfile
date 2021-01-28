# FROM python:3.8-alpine

# LABEL maintainer='Bazulenkov'

# WORKDIR /code

# COPY . .

# RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
# && apk --update --upgrade add jpeg-dev zlib-dev libffi-dev \
# cairo-dev pango-dev gdk-pixbuf-dev \
# && pip install --upgrade pip && pip install -r requirements.txt

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# RUN python3 manage.py collectstatic --noinput

# CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000

FROM python:3.8-alpine 
LABEL maintainer='Bazulenkov'
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 
RUN apk --update --upgrade --no-cache add \ 
cairo-dev pango-dev gdk-pixbuf

WORKDIR /code
COPY . .

RUN set -ex \
&& apk add --no-cache --virtual .build-deps \ 
musl-dev gcc postgresql-dev jpeg-dev zlib-dev libffi-dev \
&& pip install -r requirements.txt \
# /&& apk del .build-deps \
&& python3 manage.py collectstatic --noinput
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
