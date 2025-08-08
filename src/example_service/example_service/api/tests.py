from django.test import TestCase
from django.urls import reverse


class HealthzTests(TestCase):
    def test_healthz_returns_pong(self):
        url = reverse("healthz")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"ping": "pong"})
