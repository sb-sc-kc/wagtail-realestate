from django.core.management.base import BaseCommand, CommandError
from wagtail.admin.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from realestate.models import PropertyAssetType
import yaml

User = get_user_model()

def asset_types_create():
    for idx, label in enumerate(('Studio', 'T1', 'T2', 'T3', 'Villa', 'Domaine', 'Chalet')):
        print(idx, label)
        pat = PropertyAssetType.objects.create(id=idx, label=label)
        pat.save()


def asset_types_delete():
    for at in PropertyAssetType.objects.all():
        at.delete()

def asset_type_list():
    for pat in PropertyAssetType.objects.all():
        print(pat.pk, pat)

class Command(BaseCommand):
    help = 'Create AsssetTypes'

    def add_arguments(self, parser):
        parser.add_argument('--create', action='store_true')
        parser.add_argument('--list', action='store_true')
        parser.add_argument('--delete', action='store_true')

    def handle(self, *args, **options):
        if options['delete']:
            asset_types_delete()
        elif options['create']:
            asset_types_create()
        elif options['list']:
            asset_type_list()
        # asset_types_create()
