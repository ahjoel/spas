from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import list_type

class TestUrls(SimpleTestCase):
    ## Test sur les urls du stock

    def test_list_type_url_resolves(self):
        url = reverse('list_type')
        self.assertEquals(resolve(url).func, list_type)
