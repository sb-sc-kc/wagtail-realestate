import os
from os import path
from realestate.models import PageGalleryImage
from wagtail.images.models import Image
from django.db.models.fields.files import ImageFieldFile
from django.core.management.base import BaseCommand, CommandError
from wagtail.admin.auth import get_user_model
import shutil

User = get_user_model()

# PRJDIR = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
# module = __import__(os.environ.get('DJANGO_SETTINGS_MODULE'))
BASEDIR = path.dirname(os.path.abspath('__file__'))
MEDIADIR = path.join(BASEDIR, 'data/media')
IMAGESDIR = path.join(MEDIADIR, 'original_images')
TESTIMAGESDIR = path.join(BASEDIR, 'data', 'test_images')


class Command(BaseCommand):
    help = 'Images'

    def add_arguments(self, parser):
        parser.add_argument('--list',
                            action='store_true',
                            help='list images')
        parser.add_argument('--create',
                            action='store_true',
                            help='create images')
        parser.add_argument('--delete',
                            action='store_true',
                            help='delete images')
        parser.add_argument('--copy',
                            action='store_true',
                            help='copy images')

    def handle(self, *args, **options):
        self.stdout.write("BASEDIR: {:s}".format(BASEDIR))
        if options['list']:
            self.list_images()
        elif options ['create']:
            self.stdout.write('creating images...')
            self.create_images()
        elif options ['delete']:
            self.stdout.write('deleting images...')
            self.delete_images()
        elif options ['copy']:
            self.stdout.write('copying images...')
            self.copy_images()

    def create_images(self):
        self.copy_images()
        os.chdir(IMAGESDIR)
        self.stdout.write('IMAGESDIR: {:s}'.format(IMAGESDIR))
        imgs = [myf for myf in os.listdir() if os.path.isfile(myf)]
        for img in imgs:
            img = os.path.join('original_images', img)
            image = Image(file=img)
            image.save()
            self.stdout.write('added {:s} '.format(img) + self.style.SUCCESS('OK'))

    def list_images(self):
        for item in Image.objects.all():
            self.stdout.write(item.filename)

    def copy_images(self):
        myfiles = os.listdir(TESTIMAGESDIR)
        for myfile in myfiles:
            src = path.join(TESTIMAGESDIR, myfile)
            dst = path.join(IMAGESDIR, myfile)
            shutil.copy(src, dst)
            self.stdout.write('{src} -> {dst} '.format(src=src, dst=dst) + self.style.SUCCESS('OK'))
    def delete_images(self):
        for item in Image.objects.all():
            self.stdout.write('deleting {filename}'.format(filename=item.filename))
            item.delete()
