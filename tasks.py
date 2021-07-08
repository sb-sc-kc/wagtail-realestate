from invoke import task
import os
from pathlib import Path

DOCKER = 'docker'
DOCKER_COMPOSE = 'docker-compose'

BASE_DIR = Path(__file__).resolve().parent

os.chdir(BASE_DIR)

USE_PIPENV = False

if USE_PIPENV:
    MANAGE = 'pipenv run python manage.py'
    SPHINX_BUILD = 'pipenv run sphinx-build'
else:
    MANAGE = 'python manage.py'
    SPHINX_BUILD = 'sphinx-build'


@task
def runserver(c):
    """run server
    """
    c.run("{manage:s} runserver".format(manage=MANAGE))


@task
def migrate(c):
    """migrate django database
    """
    c.run("{manage:s} migrate --no-input".format(manage=MANAGE))


@task
def collectstatic(c):
    """collect static data
    """
    c.run("{manage:s} collectstatic --no-input".format(manage=MANAGE))


@task
def makemigrations(c):
    """build migration scripts
    """
    c.run("{manage:s} makemigrations".format(manage=MANAGE))


@task
def reset_db(c):
    """load database
    """
    print('reset_db...')
    c.run("{manage:s} reset_db".format(manage=MANAGE))
    print('reset_db done.')


def loaddata(c):
    """load database
    """
    print('loaddata...')
    # c.run("{manage:s} loaddata realestate".format(manage=MANAGE))
    c.run("{manage:s} loaddata --format yaml data/backups/test-db.yaml".format(manage=MANAGE))


@task
def dumpdata(c):
    """dump database
    """
    c.run("{manage:s} dumpdata --format yaml --indent 4 -e contenttypes \
    -o data/backups/test-db.yaml".format(manage=MANAGE))


@task
def notebook(c):
    """dump database
    """
    os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'True'
    c.run("{manage:s} shell_plus --notebook".format(manage=MANAGE))


@task
def createsuperuser(c):
    """Create django admin superuser
    """
    print('createsuperuser...')
    mystr = "from django.contrib.auth import get_user_model;\
    CustomUser = get_user_model();\
    CustomUser.objects.create_superuser(\
    'admin', 'admin@admin.io', 'admin')"
    c.run('echo "{:s}" | {manage:s} shell'.format(mystr, manage=MANAGE))


@task
def makemessages(c):
    """Create .po localization files
    """
    c.run("{django_admin:s} makemessages -l 'fr' -a".format(django_admin=DJANGO_ADMIN))


@task
def compilemessages(c):
    """Generate localization messages files
    """
    c.run("{django_admin:s} compilemessages".format(django_admin=DJANGO_ADMIN))


@task
def doc_rst(c):
    c.run('{sphinx_build:s} source build'.format(sphinx_build=SPHINX_BUILD))


@task
def doc_html(c):
    c.run('pipenv run sphinx-build -M html source build')


@task(doc_rst, doc_html)
def doc(c):
    print('building doc in build/html')


@task
def docker_img(c):
    c.run('{docker:s} build -t realestate:0.1 .'.format(docker=DOCKER))


@task
def docker_run(c):
    c.run('winpty docker run -it -p 8000:8000 realestate:0.1')


@task
def docker_compose_up(c):
    c.run('{docker_compose:s} up --build'.format(docker_compose=DOCKER_COMPOSE))


@task
def clean(c):
    import shutil
    import os
    print('clean...')
    if os.path.exists('mysite/db.sqlite3'):
        os.remove('mysite/db.sqlite3')
    if os.path.isdir('mysite/staticfiles'):
        shutil.rmtree('mysite/staticfiles')


@task(collectstatic, makemigrations, migrate, createsuperuser, loaddata)
def build(c):
    print("Building...")


@task(clean, build, runserver)
def all(c):
	print('All...')    
