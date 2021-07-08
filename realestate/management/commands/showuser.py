from django.core.management.base import BaseCommand, CommandError
from wagtail.admin.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Show user <username>'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)

    def handle(self, *args, **options):
        username = options['username']
        try:
            user = User.objects.get(username=username)
            self.stdout.write(
                self.style.SUCCESS(
                    'username: {username:s} email:{email:s} {first_name:s} {last_name:s}'.format(
                        username=user.username,
                        email=user.email,
                        first_name=user.first_name,
                        last_name=user.last_name
                )))
            self.stdout.write(
                self.style.SUCCESS(str(user))
            )
        except User.DoesNotExist:
            raise CommandError('Username "{:s}" does not exist'.format(username))

