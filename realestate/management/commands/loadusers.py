from django.core.management.base import BaseCommand, CommandError
from wagtail.admin.auth import get_user_model
from django.contrib.auth.models import Group, Permission

import yaml

User = get_user_model()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('yamlfile', type=str)


    def handle(self, *args, **options):
        usersyaml = open(options['yamlfile'], 'r').read()
        usersdict = yaml.load(usersyaml)
        self.load_users(usersdict)
        # self.stdout.write(self.style.SUCCESS(mydict))
        # for user in User.objects.all():
        #     self.stdout.write(self.style.SUCCESS('username: {username:s} email:{email:s}'.format(username=user.username, email=user.email)))

    def load_users(self, usersdata, delete=False):
        for data in usersdata:
            role = data['role']
            userdata = data['user']
            username = userdata['username']
            q = User.objects.filter(username=username)
            if len(q) > 0:
                # remove any user with that name
                if delete:
                    try:
                        q[0].delete()
                    except IndexError:
                        continue
                else:
                    self.stdout.write(self.style.WARNING('{:s} exists...'.format(username)))
                    continue

            if role == 'admin':
                user = User.objects.create_superuser(**userdata)
                user.save()
            else:
                group = None
                try:
                    group = Group.objects.filter(name=role)[0]
                except IndexError:
                    self.stdout.write(self.style.WARNING('group {:s} not found creating...'.format(role)))
                    group = Group.objects.create(name=role)

                user = User.objects.create_user(**userdata)
                if group:
                    user.groups.add(group)
                    user.save()
