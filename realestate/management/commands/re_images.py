from realestate.models import PageGalleryImage
from wagtail.images.models import Image
from django.db.models.fields.files import ImageFieldFile
from django.core.management.base import BaseCommand, CommandError

User = get_user_model()

PRJDIR = os.path.dirname(os.path.dirname(os.path.abspath('__file__')))
MEDIADIR = os.path.join(PRJDIR, 'data/media')
IMAGESDIR = os.path.join(MEDIADIR, 'original_images')

class Command(BaseCommand):
    help = 'Images Gallery'

    def add_arguments(self, parser):
        parser.add_argument('--list',
                            action='store_true',
                            help='list gallery')
        parser.add_argument('--create',
                            action='store_true',
                            help='create gallery')
        parser.add_argument('--delete',
                            action='store_true',
                            help='delete gallery')

    def handle(self, *args, **options):
        if options['list']:
            self.list_gallery()
        elif options ['create']:
            self.stdout.write('creating assets...')
            self.create_gallery()

        elif options ['delete']:
            self.stdout.write('deleting assets...')
            self.delete_gallery()

    def load_images(name_filter=''):
        os.chdir(IMAGESDIR)
        imgs = [myf for myf in os.listdir() if os.path.isfile(myf) and name_filter in myf]
        for img in imgs:
            print(img)
            img = os.path.join('original_images', img)
            image = Image(file=img)
            image.save()

    def delete_gallery_images():
        for item in PageGalleryImage.objects.all():
            item.delete()

    def create_gallery_images(page, imgs):
        for img in imgs:
            mygalimg = PageGalleryImage(page=page, image=img)
            mygalimg.save()

    def get_file_images(filename_contains):
        return [img for img in Image.objects.all() if filename_contains in str(img.file)]
        # imgs = [img for img in Image.objects.all()]

        def list_assets(self):
            for item in PropertyAssetPage.objects.all():
                self.stdout.write(
                    'pk: {pk:d}  asset: {asset:32s} slug: {slug:s}'.format(
                        pk=item.pk,
                        asset=str(item)[:30],
                        slug=item.slug,
                    ))

    def create_gallery(self):
        for item in assets_list:
            self.create_asset(item)

    def delete_gallery(self):
        for item in Image.objects.all():
            item.delete()
