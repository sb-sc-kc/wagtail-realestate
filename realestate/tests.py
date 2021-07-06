from django.test import TestCase

# Create your tests here.
from wagtail.tests.utils import WagtailPageTests
from realestate.models import PropertyAssetType
from home.models import HomePage

class PropertyAssetTypeTest(WagtailPageTests):
    def test_can_create_a_page(self):
        self.assertCanCreateAt(HomePage, PropertyAssetType)
