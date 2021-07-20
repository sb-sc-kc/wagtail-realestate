import os
os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'True'
from wagtail.admin.auth import get_user_model
User = get_user_model()

from wagtail.core.models import Page
from realestate.models import PageGalleryImage, PropertyAssetIndexPage, PropertyAssetType
from wagtail.images.models import Image
from django.db.models.fields.files import ImageFieldFile

PRJDIR = os.environ.get('MYPRJDIR', '/mnt/d/speyr/Projets/wagtail-realestate')
DATADIR = os.environ.get('MYDATADIR', os.path.join(PRJDIR, 'data'))
MEDIADIR = os.environ.get('MYMEDIADIR', os.path.join(DATADIR, 'media'))
IMAGESDIR = os.environ.get('MYIMAGESDIR', os.path.join(MEDIADIR, 'images'))

ASSET_SLUGS = ['maison-provence-01', 'studio-montagne']

from realestate.models import PropertyAssetType

def asset_types_create():
    for label in ('T1', 'T2', 'T3', 'Villa', 'Domaine'):
        pat = PropertyAssetType.objects.create(label=label)
        pat.save()

def create_assets_page():
    home = Page.objects.filter(title='Home')[0]
    pagedata = {
        'path': 'assets',
        'depth': 4, 
        'title': 'Assets', 
        'slug': 'assets'
    }
    page = PropertyAssetIndexPage(**pagedata)
    home.add_child(instance=page)

def create_index_pages():
    home = Page.objects.filter(title='Home')[0]

    page = RentalOfferIndexPage(
        title='Rental Offers',
        slug='rental-offers',
        path='rental-offers',    
    )
    home.add_child(instance=page)

    page = SaleOfferIndexPage(
        title='Sale Offers',
        slug='sale-offers',
        path='sale-offers',    
    )
    home.add_child(instance=page)    

def load_images():
    os.chdir(os.path.join(DATADIR, 'test_images'))
    imgs = [myf for myf in os.listdir() if os.path.isfile(myf)]
    for img in imgs:
        img = os.path.join('original_images', img)
        print(img)
        image = Image(file=img)
        image.save()

def create_gallery_images(page, imgs):
    for img in imgs:
        mygalimg = PageGalleryImage(page=page, image=img)
        mygalimg.save()

def delete_gallery_images():
    for item in PageGalleryImage.objects.all():
        item.delete()

def get_file_images(filename_contains):
    return [img for img in Image.objects.all() if filename_contains in str(img.file)]
