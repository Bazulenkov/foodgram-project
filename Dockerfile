FROM python:3.8-alpine

LABEL maintainer='Bazulenkov'

WORKDIR /code

COPY . .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
build-essential python3-dev python3-pip python3-setuptools python3-wheel \
python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 \
libffi-dev shared-mime-info \
&& pip install -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# EXPOSE 8000

RUN python3 manage.py collectstatic --noinput

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
