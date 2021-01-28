FROM python:3.8.5
LABEL maintainer='Bazulenkov'
WORKDIR /code
COPY . .
RUN pip install -r requirements.txt && python3 manage.py collectstatic --noinput
CMD gunicorn foodgram.wsgi:application --bind 0.0.0.0:8000