from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from .forms import SentimentForm


class SentimentViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.sentiment_url = reverse("sentiment:sentiment_analyzer")

    def test_get_request(self):
        response = self.client.get(self.sentiment_url)
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], SentimentForm)
        self.assertNotIn("result", response.context)

    def test_post_request_with_valid_data(self):
        response = self.client.post(self.sentiment_url, {"text": "I love Python!"})
        self.assertEqual(response.status_code, 200)
        self.assertIn("result", response.context)
        self.assertEqual(response.context["result"], "positive")

    def test_post_request_with_invalid_data(self):
        response = self.client.post(
            self.sentiment_url, {"text": ""}
        )  # Empty text should be invalid
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)
        self.assertIn("result", response.context)
        self.assertEqual(response.context["result"], "invalid text input!")
        self.assertTrue(response.context["form"].errors)

   