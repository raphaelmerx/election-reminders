from django.test import TestCase
from django.test import Client


class Staff(TestCase):
    def test_root_redirects_to_admin(self):
        c = Client()
        response = c.get('')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/admin/')
