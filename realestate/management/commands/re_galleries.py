import os
from os import path
from realestate.models import PageGalleryImage, PropertyAssetPage
from wagtail.images.models import Image
from django.db.models.fields.files import ImageFieldFile
from django.core.management.base import BaseCommand, CommandError
from wagtail.admin.auth import get_user_model

BASEDIR = path.dirname(os.path.abspath('__file__'))
MEDIADIR = path.join(BASEDIR, 'data/media')
IMAGESDIR = path.join(MEDIADIR, 'original_images')
TESTIMAGESDIR = path.join(BASEDIR, 'data', 'test_images')

class Command(BaseCommand):
    help = 'Galleries'

    def add_arguments(self, parser):
        parser.add_argument('--list',
                            action='store_true',
                            help='list galleries')
        parser.add_argument('--create',
                            action='store_true',
                            help='create galleries')
        parser.add_argument('--delete',
                            action='store_true',
                            help='delete galleries')

    def handle(self, *args, **options):
        self.stdout.write("BASEDIR: {:s}".format(BASEDIR))
        if options['list']:
            self.list_galleries()
        elif options ['create']:
            self.stdout.write('creating galleries...')
            self.create_galleries()
        elif options ['delete']:
            self.stdout.write('deleting galleries...')
            self.delete_galleries()

    def create_gallery(self, page, imgs):
        for img in imgs:
            mygalimg = PageGalleryImage(page=page, image=img)
            mygalimg.save()

    def get_images(self, filename_contains):
        return [img for img in Image.objects.all()
                if filename_contains in str(img.file)]
        # imgs = [img for img in Image.objects.all()]

    def create_galleries(self):
        for item in PropertyAssetPage.objects.all():
            self.stdout.write('creating images gallery for {}'.format(item.slug))
            imgs = self.get_images(item.slug)
            for img in imgs:
                page = PageGalleryImage(page=item, image=img)
                page.save()

    def delete_galleries(self):
        for item in PageGalleryImage.objects.all():
            item.delete()

    def list_galleries(self):
        for item in PageGalleryImage.objects.all():
            self.stdout.write('{}: {}'.format(item.page, item.image.file))
