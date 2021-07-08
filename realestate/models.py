#
# RealEstate Application models
#

from django.db import models
from django.db.models.functions import Substr
from django import forms

from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase

from wagtail.core.fields import RichTextField
from wagtail.core.models import Page, Orderable, PageManager
from wagtail.admin.edit_handlers import (
    FieldPanel, InlinePanel, MultiFieldPanel)
from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from wagtail.snippets.models import register_snippet


class AddressPage(Page):
    """An address used by other classes
    """
    address_street = models.CharField(max_length=256, verbose_name=_('Street'),
                                      blank=True,
                                      null=True)
    address_city = models.CharField(max_length=128, verbose_name=_('City'),
                                      blank=True,
                                      null=True)
    address_zip = models.CharField(max_length=32, verbose_name=_('Zip Code'),
                                      blank=True,
                                      null=True)
    address_country = models.CharField(
        max_length=64, verbose_name=_('Country'),
        blank=True,
        null=True)
    address_website = models.URLField(max_length=200,
                                      verbose_name='Web Site',
                                      blank=True,
                                      null=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('address_street'),
            FieldPanel('address_city'),
            FieldPanel('address_zip'),
            FieldPanel('address_country'),
        ], heading=_("Asset Address")),
    ]

    def address_county(self):
        return str(self.address_zip)[:2]


class AgencyPage(AddressPage):
    """A realestate agency
    """
    agency_name = models.CharField(max_length=64)
    template = 'realestate/agency_page.html'

    content_panels = [
        FieldPanel('agency_name'),
    ] + AddressPage.content_panels

    class Meta:
        verbose_name = _('Agency')
        verbose_name_plural = _('Agencies')

    def __str__(self):
        return str(self.agency_name)


@register_snippet
class PropertyAssetCategory(models.Model):
    """ Property Type (T1, T2 ...)
    """
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='+'
    )

    panels = [
        FieldPanel('name'),
        ImageChooserPanel('icon'),
    ]

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name_plural = 'property asset categories'


@register_snippet
class PropertyAssetType(models.Model):
    """Type of asset: T1 T2 T3 House...
    """
    label = models.CharField(max_length=32)

    class Meta:
        verbose_name = _('Asset Type')
        verbose_name_plural = _('Asset Types')

    def __str__(self):
        return str(self.label)


@register_snippet
class PropertyAssetTag(TaggedItemBase):
    content_object = ParentalKey(
        'PropertyAssetPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class PropertyAssetTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        context = super().get_context(request)
        tag = request.GET.get('tag')
        if tag:
            assetpages = PropertyAssetPage.objects.filter(tags__name__in=tag)
            context['assetpages'] = assetpages

        # Update template context
        return context


class PropertyAssetIndexPage(Page):
    intro = RichTextField(blank=True)
    template='realestate/property_asset_index_page.html'
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        assetpages = self.get_children().live()
        context['assetpages'] = assetpages
        return context

    subpage_types = ['realestate.PropertyAssetPage']


class PropertyAssetManager(PageManager):
    """QuerySet manager for Invoice class to add non-database fields.

    A @property in the model cannot be used because QuerySets (eg. return
    value from .all()) are directly tied to the database Fields -
    this does not include @property attributes."""

    def get_queryset(self):
        """Overrides the PageManager method"""
        qs = super().get_queryset().annotate(
            address_county=Substr('address_zip', 1, 2))
        return qs


class PropertyAssetPage(Page):
    """.. _models-propertyasset
    # Property Asset
    A house or flat to be sent or rented
    """
    asset_owner = models.ForeignKey(User, on_delete=models.RESTRICT,
                              verbose_name=_('Owner'))
    time_created = models.DateTimeField(
        auto_now_add=True,
        editable=False, verbose_name=_('Creation Date'))

    tags = ClusterTaggableManager(through=PropertyAssetTag, blank=True)
    categories = ParentalManyToManyField(
        'realestate.PropertyAssetCategory', blank=True)

    # Address
    address_street = models.CharField(max_length=256, verbose_name=_('Street'))
    address_city = models.CharField(max_length=128, verbose_name=_('City'))
    address_zip = models.CharField(max_length=32, verbose_name=_('Zip Code'))
    address_city = models.CharField(max_length=128, verbose_name=_('City'))
    address_country = models.CharField(max_length=64, verbose_name=_('Country'), default='France')

    # Asset
    asset_surface = models.DecimalField(
        max_digits=4, decimal_places=0, verbose_name=_('Surface'))
    asset_type = models.ForeignKey(
        PropertyAssetType, null=True,
        on_delete=models.SET_NULL, verbose_name=_('Asset Type'))

    # Description
    description = RichTextField(blank=True, null=True)

    # Overridden objects manager
    objects = PropertyAssetManager()

    subpage_types = ['realestate.SaleOfferPage', 'realestate.RentalOfferPage']

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('tags'),
            FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        ], heading=_("Property Asset information")),
        MultiFieldPanel([
            FieldPanel('asset_owner'),
            FieldPanel('address_street'),
            FieldPanel('address_city'),
            FieldPanel('address_zip'),
            FieldPanel('address_country'),
        ], heading=_("Asset Address")),
        MultiFieldPanel([
            FieldPanel('asset_type'),
            FieldPanel('asset_surface'),
            ], heading=_("Asset Informations")
        ),
        FieldPanel('description', classname="full"),
        InlinePanel('gallery_images', label="Gallery images"),
    ]
    

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        context['asset'] = self
        return context

    class Meta:
        verbose_name = _('Property Asset')
        verbose_name_plural = _('Property Assets')

    def __str__(self):
        return '{address_city:s} {address_zip:s} {asset_type:s}'.format(
            address_city=self.address_city, address_zip=self.address_zip, asset_type=str(self.asset_type),
        )

    def main_image(self):
        gallery_item = self.gallery_images.first()
        if gallery_item:
            return gallery_item.image
        else:
            return None

    def address_county(self):
        return self.address_zip[:2]


class OfferManager(PageManager):
    """QuerySet manager for PropertyAsset class to add non-database fields.

    A @property in the model cannot be used because QuerySets (eg. return
    value from .all()) are directly tied to the database Fields -
    this does not include @property attributes."""

    def get_queryset(self):
        return super().get_queryset().filter(status='_(Published)')  


class OfferPage(Page):
    """ Abstract class for offers
    """
    STATUS = (
        (1, _('Draft')),
        (2, _('Published')),
        (3, _('Archived')),
    )

    price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name=_('Price'))

    # Description
    description = RichTextField(blank=True, null=True)
    status = models.PositiveSmallIntegerField(
      choices=STATUS,
      default=1,
    )

    content_panels = Page.content_panels + [
        FieldPanel('price'),
        FieldPanel('description', classname="full"),
    ]

    class Meta:
        verbose_name = _('Offer')
        verbose_name_plural = _('Offers')

    def __str__(self):
        return 'Offer: {title:s} prix: {price:9.2f}'.format(
            title=self.title, price=self.price)

    def asset_surface(self):
        return self.get_parent().specific.asset_surface


class OfferIndexPage(RoutablePageMixin, Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request, *args, **kwargs):
        """Adding custom stuff to our context."""
        context = super().get_context(request, *args, **kwargs)
        offerpages = self.get_children().specific().live()
        # assert(len(offerpages) > 0)
        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            offerpages = offerpages.filter(tags__slug__in=[tags])
        context['offerpages'] = offerpages
        context['offerpages_count'] = self.get_children_count()

        return context


class RentalOfferIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    subpage_types = ['realestate.RentalOfferPage']

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        offerpages = RentalOfferPage.objects.specific()
        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            offerpages = offerpages.filter(tags__slug__in=[tags])

        context['offerpages'] = offerpages
        context['offer_type'] = 'rental-offer'
        
        return context


class RentalOfferPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'RentalOfferPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class RentalOfferPage(RoutablePageMixin, OfferPage):
    """Rental Offers
    """
    deposit = models.DecimalField(
        max_digits=6, decimal_places=2, default=0, verbose_name=_('Deposit'))
    start_date = models.DateTimeField(verbose_name=_('Start Date'))
    end_date = models.DateTimeField(verbose_name=_('End Date'))
    tags = ClusterTaggableManager(through=RentalOfferPageTag, blank=True)

    content_panels = OfferPage.content_panels + [
        FieldPanel('tags'),
        FieldPanel('deposit'),
        FieldPanel('start_date'),
        FieldPanel('end_date'),
    ]

    class Meta:
        verbose_name = _('Rental Offer')
        verbose_name_plural = _('Rental Offers')

    # def __str__(self):
    #     return _('{asset:s} available from {start_date:s} to {end_date:s} price: {price:9.2f}').format(
    #         asset=str(self.get_parent().asset),
    #         start_date=format_date(self.start_date),
    #         end_date=format_date(self.end_date), price=self.price)
    
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        asset = self.get_parent().specific
        images = asset.gallery_images.all()
        # assert(len(offerpages) > 0)
        context['offer'] = self
        context['asset'] = asset
        context['images'] = images
        return context

    def __str__(self):
        return _('Rental Offer: {title:s} prix: {price:9.2f}').format(
            title=self.title, price=self.price)

    @route(r'^rental-offer/(?P<offerid>)/$')
    def view_offer(self, request, offerid, *args, **kwargs):
        offer = RentalOfferPage.objects.get(pk=offerid)
        return self.render(request)


class SaleOfferIndexPage(Page):
    intro = RichTextField(blank=True)
    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full")
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        offerpages = SaleOfferPage.objects.live().specific()
        if request.GET.get('tag', None):
            tags = request.GET.get('tag')
            offerpages = offerpages.filter(tags__slug__in=[tags])

        context['offerpages'] = offerpages
        context['offer_type'] = 'sale-offer'
        
        return context

    subpage_types = ['realestate.SaleOfferPage']


class SaleOfferPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'SaleOfferPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class SaleOfferPage(OfferPage):
    """Sale Offers
    """
    tags = ClusterTaggableManager(through=SaleOfferPageTag, blank=True)

    class Meta:
        verbose_name = _('Sale Offer')
        verbose_name_plural = _('Sale Offers')

    content_panels = OfferPage.content_panels + [
        FieldPanel('tags'),
    ]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        asset = self.get_parent().specific
        images = asset.gallery_images.all()
        # assert(len(offerpages) > 0)
        context['offer'] = self
        context['asset'] = asset
        context['images'] = images
        return context



class PageGalleryImage(Orderable):
    page = ParentalKey(PropertyAssetPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('caption'),
    ]
