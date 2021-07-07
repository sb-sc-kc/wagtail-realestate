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
            parent = Page.objects.filter(pk=page.pk).first_common_ancestor()
            self.stdout.write(self.style.SUCCESS('{page:s} <- {parent:s}'.format(page=str(page), parent=str(parent))))
