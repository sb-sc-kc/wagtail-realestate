from django.conf import settings

def site_options(request):
    my_dict = {
        'site_options': {
            'site_theme': settings.SITE_THEME,
            'site_name': settings.SITE_NAME,
        }
    }

    return my_dict
