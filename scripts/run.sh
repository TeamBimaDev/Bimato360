#!/bin/sh

set -e
chmod -R 777 /app/media
chown -R 1000:1000 /app/media
python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :8500 --workers 4 --master --enable-threads --module app.wsgi
