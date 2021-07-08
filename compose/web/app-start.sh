export PYTHON_PATH=.
dockerize -wait tcp://db:5432 -timeout 30s -wait-retry-interval 5s
# python app/manage.py runserver 0.0.0.0:8000

APP_MODULE="mysite.wsgi:application"

cd app
python manage.py migrate
python manage.py loaddata --format yaml -e contenttypes ../test-db.yaml

echo "DJANGO_SETTINGS_MODULE: ${DJANGO_SETTINGS_MODULE}"

gunicorn -c ../gunicorn.conf.py ${APP_MODULE}
