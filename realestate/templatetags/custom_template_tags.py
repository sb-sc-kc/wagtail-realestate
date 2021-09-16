from django import template
from wagtail.core.models import PageViewRestriction
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


@register.simple_tag(takes_context=True)
def can_view(context, page):
    print('can_view:', page.slug)
    request = context['request']
    user = request.user
    if user.is_superuser:
        return True
    pvrs = page.get_view_restrictions()
    current_user_groups = user.groups.all()
    if pvrs and len(pvrs) > 0:
        for pvr in pvrs:
            if pvr.restriction_type == PageViewRestriction.GROUPS:
                current_user_groups = request.user.groups.all()
                for pagegroup in pvr.groups.all():
                    if pagegroup in current_user_groups:
                        return True
            else:
                return True
        return False
    return True

	# for restriction in page.get_view_restrictions():
	# 	print("has restricction")
	# 	if restriction.restriction_type == PageViewRestriction.GROUPS:
	# 		if not request.user.is_superuser:
	# 			current_user_groups = request.user.groups.all()
	# 		else: 
	# 			return True
	# 		if not any(group in current_user_groups for group in user.groups.all()):
	# 			return False
	# return True
