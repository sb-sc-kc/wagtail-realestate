from django.core.management.base import BaseCommand, CommandError
from wagtail.admin.auth import get_user_model
User = get_user_model()

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        for user in User.objects.all():
            self.stdout.write(self.style.SUCCESS('username: {username:s} email:{email:s}'.format(username=user.username, email=user.email)))
