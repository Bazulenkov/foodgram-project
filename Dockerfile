FROM python:3.8.5
LABEL maintainer='Bazulenkov'
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt && python3 manage.py collectstatic --noinput
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000


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




# FROM python:3.8-alpine 
# LABEL maintainer='Bazulenkov'
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1 

# ENV MUSL_LOCALE_DEPS cmake make musl-dev gcc gettext-dev libintl
# ENV MUSL_LOCPATH /usr/share/i18n/locales/musl

# WORKDIR /code
# COPY . .

# RUN apk add --no-cache $MUSL_LOCALE_DEPS \
# && wget https://gitlab.com/rilian-la-te/musl-locales/-/archive/master/musl-locales-master.zip \
# && unzip musl-locales-master.zip \
# && cd musl-locales-master \
# && cmake -DLOCALE_PROFILE=OFF -D CMAKE_INSTALL_PREFIX:PATH=/usr . && make && make install \
# && cd .. && rm -r musl-locales-master

# ENV LANG ru_RU.UTF-8
# ENV LANGUAGE ru_RU:
# ENV LC_CTYPE ru_RU.UTF-8
# ENV LC_NUMERIC ru_RU.UTF-8
# ENV LC_TIME ru_RU.UTF-8
# ENV LC_COLLATE ru_RU.UTF-8
# ENV LC_MONETARY ru_RU.UTF-8
# ENV LC_MESSAGES ru_RU.UTF-8
# ENV LC_PAPER ru_RU.UTF-8
# ENV LC_NAME ru_RU.UTF-8
# ENV LC_ADDRESS ru_RU.UTF-8
# ENV LC_TELEPHONE ru_RU.UTF-8
# ENV LC_MEASUREMENT ru_RU.UTF-8
# ENV LC_IDENTIFICATION ru_RU.UTF-8
# ENV LC_ALL ru_RU.UTF-8

# RUN apk --update --upgrade --no-cache add \ 
# cairo-dev pango-dev gdk-pixbuf

# RUN set -ex \
# && apk add --no-cache --virtual .build-deps \ 
# musl-dev gcc postgresql-dev jpeg-dev zlib-dev libffi-dev \
# && pip install -r requirements.txt \
# # && apk del .build-deps \
# && python3 manage.py collectstatic --noinput
# CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000
