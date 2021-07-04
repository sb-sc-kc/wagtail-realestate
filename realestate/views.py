from django.shortcuts import render
from django.contrib.auth.models import User


class PersonChooserViewSet(ModelChooserViewSet):
    icon = 'user'
    model = User
    page_title = _("Choose a person")
    per_page = 10
    order_by = 'firstname'
    fields = ['firstname', 'lastname', 'email']
