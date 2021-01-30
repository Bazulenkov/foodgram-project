FROM python:3.8-alpine 
LABEL maintainer='Bazulenkov'
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

WORKDIR /code
COPY . .

RUN set -ex \
&& apk add --update --upgrade --no-cache --virtual .build-deps \ 
cairo-dev pango-dev gdk-pixbuf cairo ttf-freefont ttf-font-awesome \
musl-dev gcc postgresql-dev jpeg-dev zlib-dev libffi-dev \
&& pip install -r requirements.txt \
&& python3 manage.py collectstatic --noinput

CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
