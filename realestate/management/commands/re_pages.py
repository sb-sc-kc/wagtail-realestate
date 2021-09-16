from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group
from wagtail.admin.auth import get_user_model
from wagtail.core.models import Page, Site, PageViewRestriction
from realestate.models import (PropertyAssetIndexPage,
                               RealEstateHomePage,
                               OfferIndexPage,
                               RentalOfferIndexPage,
                               SaleOfferIndexPage,
                               RentalOfferContactIndexPage)
from django.core.exceptions import ValidationError

User = get_user_model()

DEFSTR = """Nullam eu ante vel est convallis dignissim. Fusce suscipit, 
wisi nec facilisis facilisis, 
est dui fermentum leo, quis tempor ligula erat quis odio. Nunc porta vulputate tellus. Nunc rutrum turpis se
"""

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
        default_home = Page.objects.filter(title='Home')[0]
        # home_page.delete()
        default_home.slug = 'home-old'
        default_home.save_revision().publish()
        default_home.save()
        root = Page.objects.get(id=1)
        home_page =  RealEstateHomePage(
                title='Accueil',
                slug='accueil',
                # depth='0000',
                # path='/'
            )
        root.add_child(instance=home_page)
        # home_page.save()
        # revision = home_page.save_revision()
        # revision.publish()
        home_page.save()
        site = Site.objects.all()[0]
        site.root_page = home_page
        site.save()
        try:
            page = PropertyAssetIndexPage(
                title='Biens Immobiliers',
                slug='assets',
            )
            home_page.add_child(instance=page)
            # page.save_revision().publish()
            # page.save()
        except ValidationError:
            pass

        try:
            page = RentalOfferIndexPage(
                title='Offres à la location Mer',
                slug='rental-offers-mer',
                path='rental-offers-mer',
            )
            page.tag = 'mer'
            page.show_in_menus = True
            page.intro = DEFSTR
            home_page.add_child(instance=page)
        except ValidationError:
            pass

        try:
            page = RentalOfferIndexPage(
                title='Offres à la location Montagne',
                slug='rental-offers-montagne',
                path='rental-offers-montagne',
            )
            page.tag = 'montagne'
            page.show_in_menus = True
            page.intro = DEFSTR
            home_page.add_child(instance=page)
        except ValidationError:
            pass

        try:
            page = SaleOfferIndexPage(
                title='Offres à la vente',
                slug='sale-offers',
                path='sale-offers',
            )
            home_page.add_child(instance=page)
        except ValidationError:
            pass
        try:
            page = RentalOfferContactIndexPage(
                title='Contacts Locations',
                slug='contacts-locations',
                path='contacts-locations',
                show_in_menus=True
            )
            page = home_page.add_child(instance=page)
            pvr = PageViewRestriction(restriction_type=PageViewRestriction.GROUPS, page=page)
            pvr.save()
            group = Group.objects.filter(name='Editors').first()
            pvr.groups.add(group)
            group = Group.objects.filter(name='Moderators').first()
            pvr.groups.add(group)
        except ValidationError:
            pass
