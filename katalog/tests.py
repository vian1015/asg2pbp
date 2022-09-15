from django.test import TestCase, Client
from django.urls import resolve


class ContohAppTest(TestCase):
    def test_contoh_app_url_exists(self):   
        response = Client().get('/katalog/')
        self.assertEqual(response.status_code, 200)

    def test_contoh_app_using_to_do_list_template(self):
        response = Client().get('/katalog/')
        self.assertTemplateUsed(response, 'katalog.html')
