from django.core.management.base import BaseCommand, CommandError
from wagtail.admin.auth import get_user_model
from django.contrib.auth.models import Group, Permission

import yaml
DEFAULT_YAML_FILE = 'data/populate/users.yaml'

User = get_user_model()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def list_users(self):
        for user in User.objects.all():
            self.stdout.write(
                self.style.SUCCESS(
                    'username: {username:10s}email:{email:s}'.format(
                        username=user.username, email=user.email)))

    def delete_users(self):
        for user in User.objects.all():
            user.delete()

    def load_user(self, data, delete=False):
        role = data['role']
        userdata = data['user']
        username = userdata['username']
        print('creating {:s}'.format(username))
        q = User.objects.filter(username=username)
        if len(q) > 0:
            # remove any user with that name
            if delete:
                try:
                    q[0].delete()
                except IndexError:
                    return
            else:
                self.stdout.write(
                    self.style.WARNING('{:s} exists...'.format(username)))
                return

        if role == 'admin':
            user = User.objects.create_superuser(**userdata)
            user.save()
        else:
            group = None
            try:
                group = Group.objects.filter(name=role)[0]
            except IndexError:
                self.stdout.write(
                    self.style.WARNING(
                        'group {:s} not found creating...'.format(role)))
                group = Group.objects.create(name=role)

            user = User.objects.create_user(**userdata)
            if group:
                user.groups.add(group)
                user.save()

    def load_users(self, usersdata, delete=False):
        for data in usersdata:
            self.load_user(data, delete)

    def add_arguments(self, parser):
        parser.add_argument('--list',
                            action='store_true',
                            help='list users')
        parser.add_argument('--create',
                            action='store_true',
                            help='create users')
        parser.add_argument('--yamlfile',
                            type=str,
                            help='yaml file to load users from',
                            default=DEFAULT_YAML_FILE)
        parser.add_argument('--delete',
                            action='store_true',
                            help='delete users')

    def handle(self, *args, **options):
        if options['list']:
            self.list_users()
        elif options ['create']:
            if options['yamlfile']:
                yamlfile = options['yamlfile']
                self.stdout.write(
                    'creating users using yamlfile {:s}'.format(
                        yamlfile))
                with open(options['yamlfile'], 'r') as myyaml:
                    usersyaml= myyaml.read()
                    usersdict = yaml.safe_load(usersyaml)
                    print(usersdict)
                    self.load_users(usersdict)

        elif options ['delete']:
            print('deleting users...')
            self.delete_users()
