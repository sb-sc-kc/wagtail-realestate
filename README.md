# wagtail-realestate 

## Installation

    git clone --recurse git@github.com:sb-sc-kc/wagtail-realestate
  
    cd wagtail-realestate
    pipenv install -d
    pipenv shell
    python manage.py collectstatic
    python manage.py migrate
  
    python manage.py <re_cmd> --create 
  
<re_cmd> correspondant à une des commandes suivantes :
   
    python manage.py re_users
    python manage.py re_asset_types
    python manage.py re_pages
    python manage.py re_assets
    python manage.py re_offers
    TODO: re_images

 Attention! Les commandes doivent être exécutées dans l'ordre ci dessus
 
 ## Lancement du serveur
 
     python manage.py runserver [numero_port]
