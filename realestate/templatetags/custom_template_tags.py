from django import template
import environ

register = template.Library()

@register.simple_tag
def setvar(val=None):
    """Positionner une variable dans les templates
    Utilisé dans les carousels pour détecter le premier élément
    """
    return val

@register.simple_tag
def theme(val=None):
    """Positionner une variable dans les templates
    Utilisé dans les carousels pour détecter le premier élément
    """
    env = environ.Env(
        # set casting, default value
        DEBUG=(bool, False),
        THEME= (str, 'default')
    )
    return environ('THEME')
