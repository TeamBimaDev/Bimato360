<<<<<<< HEAD
#!/bin/sh

set -e
python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :8500 --workers 4 --master --enable-threads --module app.wsgi
=======
#!/bin/sh

set -e
python manage.py wait_for_db
python manage.py collectstatic --noinput
python manage.py migrate

uwsgi --socket :8500 --workers 4 --master --enable-threads --module app.wsgi
>>>>>>> origin/ma-branch
