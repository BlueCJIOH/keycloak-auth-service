from django.test import TestCase
from django.urls import reverse


class HelloViewTests(TestCase):
    def test_unauthorized_without_token(self):
        url = reverse('hello')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
