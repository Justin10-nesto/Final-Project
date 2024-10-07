#!/bin/sh
docker network create proxy

touch acme.json && chmod 600 acme.json

docker compose up --build -d

docker compose exec elearning python manage.py migrate --noinput