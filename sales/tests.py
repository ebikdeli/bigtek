from django.test import TestCase
from sales.models import Customers, Cart


class OptionsTest(TestCase):
    ali = ''
    alik = ''
    def setUp(self):
        ali = Customers.objects.create(email='ali@gmail.com', domain='sales.com')
        self.alik = ali

    def test_sales(self):
        print(self.alik.website_name)

