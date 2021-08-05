from django.core.management.base import BaseCommand, CommandError
from wagtail.admin.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from wagtail.core.models import Page
from realestate.models import (PropertyAssetIndexPage,
                               PropertyAssetPage,
                               PropertyAssetType,
                               PageGalleryImage)
import yaml
DEFAULT_YAML_FILE = 'data/populate/assets.yml'

assets_list = [
    {
        'title': 'Villa en provence',
        'slug': 'maison-provence-01',
        'path': 'maison-provence-01',
        'depth': '00010',
        'asset_owner': 'jconrad',
        'address_street': 'Cavalaire',
        'address_zip': '83987',
        'address_city': 'Cavalaire',
        'asset_surface': 253,
        'asset_type': 'Villa',
        # 'tags': ['Provence']
    },
    {
        # 'id': 1,
        'title': 'Studio à la montagne',
        'slug': 'studio-montagne',
        'path': 'studio-montagne',
        'asset_owner': 'gorwell',
        'address_street': '654 chemin qui monte',
        'address_zip': '06987',
        'address_city': 'Isola',
        'asset_surface': 25,
        'asset_type': 'Studio',
        'tags': ['Montagne']
    },
    {
        # 'id': 2,
            'title': 'Villa en provence verte',
        'slug': 'maison-provence-02',
        'path': 'maison-provence-02',
        'depth': '00010',
        'asset_owner': 'fkafka',
        'address_street': '78 rue du puis',
        'address_zip': '83951',
        'address_city': 'Le Mole',
        'asset_surface': 125,
        'asset_type': 'Villa',
        'tags': ['Provence'],
    },
]

User = get_user_model()


class Command(BaseCommand):
    help = 'Property Assets'

    def add_arguments(self, parser):
        parser.add_argument('--list',
                            action='store_true',
                            help='list assets')
        parser.add_argument('--create',
                            action='store_true',
                            help='create assets')
        parser.add_argument('--delete',
                            action='store_true',
                            help='delete assets')

    def handle(self, *args, **options):
        if options['list']:
            self.list_assets()
        elif options ['create']:
            self.stdout.write('creating assets...')
            self.create_assets()

        elif options ['delete']:
            self.stdout.write('deleting assets...')
            self.delete_assets()

    def list_assets(self):
        for item in PropertyAssetPage.objects.all():
            self.stdout.write(
                'pk: {pk:d}  asset: {asset:32s} slug: {slug:s}'.format(
                    pk=item.pk,
                    asset=str(item)[:30],
                    slug=item.slug,
                ))

    def create_asset(self, pagedata):
        parent = PropertyAssetIndexPage.objects.all()[0]
        pagedata['asset_owner'] = User.objects.filter(
            username=pagedata['asset_owner'])[0]
        pagedata['asset_type'] = PropertyAssetType.objects.filter(
            label=pagedata['asset_type'])[0]
        page = PropertyAssetPage(**pagedata)
        parent.add_child(instance=page)

    def create_assets(self):
        for item in assets_list:
            self.create_asset(item)

    def delete_assets(self):
        for asset in PropertyAssetPage.objects.all():
            asset.delete()
