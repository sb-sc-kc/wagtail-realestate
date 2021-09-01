from django.core.management.base import BaseCommand, CommandError
from wagtail.admin.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from wagtail.core.models import Page
from realestate.models import (RentalOfferIndexPage,
                               RentalOfferPage,
                               OfferPage,
                               SaleOfferPage,
                               PropertyAssetPage,
                               PropertyAssetType,
                               PageGalleryImage)
from datetime import datetime
import yaml

User = get_user_model()

from scripts import utils, offers

DEFAULT_YAML_FILE = 'data/populate/offers.yaml'

OFFERS_LIST = [
{
    'property_asset': 'studio-montagne',
    'title': 'Studio à Isola', 
    'slug': 'rental-studio-isola',
    'path': 'rental-studio-isola',
    'depth': '00010',
    'start_date': datetime(year=2021, month=8, day=20, hour=12),
    'end_date': datetime(year=2021, month=8, day=27, hour=12),
    'price': 1500,
    'deposit': 750,
    'description': offers.STR1,
},
{
    'property_asset': 'maison-provence-01',
    'title': "Villa les pieds dans l'eau", 
    'slug': 'rental-villa-plage',
    'path': 'rental-villa-plage',
    'depth': '00010',
    'start_date': datetime(year=2021, month=8, day=20, hour=12),
    'end_date': datetime(year=2021, month=8, day=27, hour=12),
    'price': 2500,
    'deposit': 3000,
    'description': offers.STR2,
},
{
    'property_asset': 'maison-provence-02',
    'title': "Vente Villa provence côte", 
    'slug': 'sale-maison-provence-01',
    'path': 'sale-maison-provence-01',
    'depth': '00010',
    'price': 2500000,
    'description': offers.STR2,
}
]

class Command(BaseCommand):
    help = 'Property Offers'

    def add_arguments(self, parser):
        parser.add_argument('--list',
                            action='store_true',
                            help='list offers')
        parser.add_argument('--create',
                            action='store_true',
                            help='create offers')
        parser.add_argument('--delete',
                            action='store_true',
                            help='delete offers')

    def handle(self, *args, **options):
        if options['list']:
            self.list_offers()
        elif options ['create']:
            self.stdout.write('creating offers...')
            self.create_offers(OFFERS_LIST)

        elif options ['delete']:
            self.stdout.write('deleting offers...')
            self.delete_offers()

    def list_offers(self):
        for item in OfferPage.objects.specific().all():
            self.stdout.write(
                'pk: {pk:d} type: {otype:20s} offer: {offer:32s} slug: {slug:s}'.format(
                    pk=item.pk,
                    otype=str(type(item)).split('.')[-1][:-2],
                    offer=str(item)[:30],
                    slug=item.slug,
                ))

    def create_offer(self, offer_dict):
        parent = PropertyAssetPage.objects.filter(slug=offer_dict['property_asset'])[0]
        del offer_dict['property_asset']
        page = None
        if offer_dict['slug'].startswith('rental'):
            page = RentalOfferPage(**offer_dict)
        else:
            page = SaleOfferPage(**offer_dict)
        parent.add_child(instance=page)

    def create_offers(self, offers_list):
        for item in offers_list:
            self.create_offer(item)

    def delete_offers(self):
        for offer in OfferPage.objects.all():
            offer.delete()
