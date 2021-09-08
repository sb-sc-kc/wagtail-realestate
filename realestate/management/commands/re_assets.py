from django.core.management.base import BaseCommand, CommandError
from wagtail.admin.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from wagtail.core.models import Page
from realestate.models import (PropertyAssetIndexPage,
                               PropertyAssetPage,
                               PropertyAssetType,
                               PageGalleryImage,
                               RentalOfferPage,
                               SaleOfferPage)
from django.core.exceptions import ValidationError
                               
import yaml
DEFAULT_YAML_FILE = 'data/populate/assets.yaml'

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
        parser.add_argument('--yamlfile',
                            type=str,
                            help='yaml file to load assets from',
                            default=DEFAULT_YAML_FILE)

    def handle(self, *args, **options):
        if options['list']:
            self.list_assets()
        elif options ['create']:
            self.stdout.write('creating assets...')
            if options['yamlfile']:
                yamlfile = options['yamlfile']
                self.stdout.write(
                    'creating assets using yamlfile {:s}'.format(
                        yamlfile))
                with open(options['yamlfile'], 'r', encoding='utf-8') as myyaml:
                    myyaml = myyaml.read()
                    mydict = yaml.safe_load(myyaml)
                    # print(mydict)
                    self.load_assets(mydict)
            # self.create_assets()

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

    def load_asset(self, pagedata):
        parent = PropertyAssetIndexPage.objects.all()[0]
        assert parent is not None
        # self.stdout.write(str(pagedata))
        pagedata['asset_owner'] = User.objects.filter(
            username=pagedata['asset_owner'])[0]
        pagedata['asset_type'] = PropertyAssetType.objects.filter(
            label=pagedata['asset_type'])[0]
        assetpage = PropertyAssetPage(**pagedata)
        parent.add_child(instance=assetpage)
        return assetpage

    def load_assets(self, assets_list):
        for item in assets_list:
            try:
                assetpage = self.load_asset(item['asset'])
                if 'rental_offers' in item.keys():
                    idx = 1
                    for offer in item['rental_offers']:
                        offer['slug'] = 'rental-{}-{:02d}'.format(str(assetpage.slug), idx)
                        offer['path'] = offer['slug']
                        offerpage = RentalOfferPage(**offer)
                        assetpage.add_child(instance=offerpage)
                        # print('RENTAL OFFER:' + str(offer))
                        idx += 1
            except ValidationError as exc:
                self.stdout.write(self.style.ERROR('error:' + item['asset']['asset_data']['slug']))
                pass


    def delete_assets(self):
        for asset in PropertyAssetPage.objects.all():
            asset.delete()
