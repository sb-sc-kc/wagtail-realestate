from django.core.management.base import BaseCommand, CommandError
from wagtail.admin.auth import get_user_model
from wagtail.core.models import Page

User = get_user_model()

class Command(BaseCommand):
    help = 'List site pages'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        for page in Page.objects.all():
            # mystr = "{:s}".format(str(page))
            mystr = ""
            parent = page.get_parent()
            while parent:
                mystr = "{:s} > {:s}".format(str(parent), mystr)
                mypage = parent
                parent = mypage.get_parent()
            self.stdout.write(self.style.SUCCESS('{:s} > {:s} {:s}'.format(mystr, str(page), page.slug)))
