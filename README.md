# wagtail-realestate 

## Installation

    git clone --recurse git@github:sb-sc-kc/wagtail-realestate
  
    cd wagtail-realestate
    pipenv install -d
    pipenv shell
    python manage.py collectstatic
    python manage.py migrate
  
    python manage.py <re_cmd> --create 
  
<re_cmd> correspondant à une des commandes suivantes :
   
    re_users
    re_asset_types
    re_pages
    re_assets
    re_offers
    TODO: re_images

 Attention! Les commandes doivent être exécutées dans l'ordre ci dessus
 
 ## Lancement du serveur
 
     python manage.py runserver [numero_port]
