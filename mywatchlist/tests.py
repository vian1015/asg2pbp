from django.test import TestCase, Client
from django.urls import resolve


class ContohAppTest(TestCase):
    def html_url_exists(self):   
        response = Client().get('/mywatchlist/html/')
        self.assertEqual(response.status_code, 200)

    def html_using_to_do_list_template(self):
        response = Client().get('/mywatchlist/html/')
        self.assertTemplateUsed(response, 'mywatchlist.html')
        
    def xml_url_exists(self):   
        response = Client().get('/mywatchlist/xml/')
        self.assertEqual(response.status_code, 200)

    def xml_using_to_do_list_template(self):
        response = Client().get('/mywatchlist/xml/')
        self.assertTemplateUsed(response, 'mywatchlist.html')

    def json_url_exists(self):   
        response = Client().get('/mywatchlist/json/')
        self.assertEqual(response.status_code, 200)

    def json_using_to_do_list_template(self):
        response = Client().get('/mywatchlist/json/')
        self.assertTemplateUsed(response, 'mywatchlist.html')
