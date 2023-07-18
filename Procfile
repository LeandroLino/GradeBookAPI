web: gunicorn GradeBookAPI.wsgi:application --log-file - --log-level debug
release: python manage.py collectstatic --noinput
release: manage.py migrate --run-syncdb
