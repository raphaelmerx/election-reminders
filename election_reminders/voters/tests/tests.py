import urllib
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.test import Client

from reminders.tests.factories import MessageFactory


class Unsubscribe(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.message = MessageFactory()
        cls.voter = cls.message.voter
        cls.url = reverse('unsubscribe')
        cls.client = Client()

    def test_invalid_request(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

        response = self.client.get(self.url, {'uuid': 'ab327ec3-9cdf-4467-9e04-ad12e6cc28a2'})
        self.assertEqual(response.status_code, 404)

        response = self.client.get(self.url, {'uuid': 'ab'})
        self.assertEqual(response.status_code, 400)

    def test_get_form(self):
        response = self.client.get(self.url, {'uuid': self.voter.uuid})
        self.assertEqual(response.status_code, 200)

    def test_post_unsubscribe(self):
        url = self.url + '?' + urllib.parse.urlencode({'uuid': self.voter.uuid})
        voter = self.voter
        self.assertFalse(voter.unsubscribed)
        response = self.client.post(url, {'unsubscribed': 1})
        self.assertEqual(response.status_code, 200)
        voter.refresh_from_db()
        self.assertTrue(voter.unsubscribed)

    def test_revert_unsubscribe(self):
        voter = self.voter
        voter.unsubscribed = True
        voter.save()
        url = self.url + '?' + urllib.parse.urlencode({'uuid': voter.uuid})
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 200)
        voter.refresh_from_db()
        self.assertFalse(voter.unsubscribed)
