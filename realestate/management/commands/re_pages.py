from django.core.management.base import BaseCommand, CommandError
from wagtail.admin.auth import get_user_model
from wagtail.core.models import Page
from realestate.models import (PropertyAssetIndexPage,
                               OfferIndexPage,
                               RentalOfferIndexPage,
                               SaleOfferIndexPage)

User = get_user_model()

class Command(BaseCommand):
    help = 'List site pages'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def add_arguments(self, parser):
        parser.add_argument('--list',
                            action='store_true',
                            help='list pages')
        parser.add_argument('--create',
                            action='store_true',
                            help='create pages')
        parser.add_argument('--delete',
                            action='store_true',
                            help='delete page')
        parser.add_argument('--pk', type=int,
                            default=None,
                            help='page pk')

    def handle(self, *args, **options):
        if options['list']:
            self.list_pages()
        elif options ['create']:
            self.stdout.write('creating pages...')
            self.create_pages()

        elif options ['delete']:
            self.stdout.write('deleting pages...')
            self.delete_page(options['pk'])

    def list_pages(self):
        for page in Page.objects.all():
            # mystr = "{:s}".format(str(page))
            mystr = ""
            parent = page.get_parent()
            while parent:
                mystr = "{:s} > {:s}".format(str(parent), mystr)
                mypage = parent
                parent = mypage.get_parent()
            self.stdout.write(self.style.SUCCESS(
                'id: {id:2d} {page:50s} slug: {slug:s}'.format(
                    id=page.id,
                    page=mystr + str(page)[:48],
                    slug=page.slug)))

    def delete_page(self, pk):
        page = Page.objects.get(pk=pk)
        page.delete()

    def create_pages(self):
        home = Page.objects.filter(title='Home')[0]

        page = PropertyAssetIndexPage(
            title='Property Assets',
            slug='assets',
        )
        home.add_child(instance=page)
        page = RentalOfferIndexPage(
            title='Rental Offers',
            slug='rental-offers',
            path='rental-offers',
        )
        home.add_child(instance=page)

        page = SaleOfferIndexPage(
            title='Sale Offers',
            slug='sale-offers',
            path='sale-offers',
        )
        home.add_child(instance=page)
