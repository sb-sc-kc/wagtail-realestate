# wagtail-realestate 

## Installation

Ouvrir un powershell

    git clone --recurse git@github.com:sb-sc-kc/wagtail-realestate
  
    cd wagtail-realestate
    pipenv install -d
    pipenv shell
    python manage.py collectstatic
    python manage.py migrate

	.\load-test-data.ps1

## Lancement du serveur
 
     python manage.py runserver
