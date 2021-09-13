# wagtail-realestate 

# realestate: Projet de validation web designer

Status: Développement en cours

# Technologies utilisées

## Django

[Dango Project](https://www.djangoproject.com/)

[Getting started with Django](https://www.djangoproject.com/start/)

[OpenClassRoom: Découvrez le framework Django](https://openclassrooms.com/fr/courses/4425076-decouvrez-le-framework-django)

## Wagtail

<https://wagtail.io/>

<https://learnwagtail.com/>

## [Bootstrap](https://getbootstrap.com/)

Version : 5.0

Framework css/js

### Media Queries

[Breakpoints](https://getbootstrap.com/docs/5.0/layout/breakpoints/)

# Choix des settings
	$Env:DJANGO_SETTINGS_MODULE='mysite.settings.development'

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
     







## 
CREATION DE LA PAGE UTILISATEUR
  espace utilisateur
  formulaire de réservation , avec sécurité de mot de passe.
  formulaire ou le client peut mettre son nom, prénom, mail, numéro de tel ,
  son adresse, date d'arrivée et de départ . 
  je dois pouvoir leur faire la démo que cela fonctionne sur la base de donnée.
