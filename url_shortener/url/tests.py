from django.test import TestCase
from django.utils import timezone
from django.test.utils import setup_test_environment, teardown_test_environment
from django.test import Client

from .models import *

# Create your tests here.


class UrlModelTests(TestCase):

    def test_create_model_instance_and_get_values_basic(self):
        test_url = Url(original_url="google.com", pub_date=datetime.datetime(
            2020, 1, 1, 0, 0, 0, 0, timezone.utc))
        self.assertEqual(test_url.original_url, "google.com")
        self.assertEqual(test_url.pub_date, datetime.datetime(
            2020, 1, 1, 0, 0, 0, 0, timezone.utc))

    def test_create_model_instance_and_get_values_all(self):
        test_url = Url(original_url="google.com", original_url_link="https://google.com", shorten_url="abcde", pub_date=datetime.datetime(
            2020, 1, 1, 0, 0, 0, 0, timezone.utc), count=1, last_access=datetime.datetime(2022, 1, 1, 0, 0, 0, 0, timezone.utc))
        self.assertEqual(test_url.original_url, "google.com")
        self.assertEqual(test_url.original_url_link, "https://google.com")
        self.assertEqual(test_url.shorten_url, "abcde")
        self.assertEqual(test_url.pub_date, datetime.datetime(
            2020, 1, 1, 0, 0, 0, 0, timezone.utc))
        self.assertEqual(test_url.count, 1)
        self.assertEqual(test_url.last_access, datetime.datetime(
            2022, 1, 1, 0, 0, 0, 0, timezone.utc))

    def test_create_model_instance_and_get_values_all_with_save(self):
        test_url = Url(original_url="google.com", original_url_link="https://google.com", shorten_url="abcde", pub_date=datetime.datetime(
            2020, 1, 1, 0, 0, 0, 0, timezone.utc), count=1, last_access=datetime.datetime(2022, 1, 1, 0, 0, 0, 0, timezone.utc))
        test_url.save()
        self.assertEqual(test_url.original_url, "google.com")
        self.assertEqual(test_url.original_url_link, "https://google.com")
        self.assertEqual(test_url.shorten_url, "abcde")
        self.assertEqual(test_url.pub_date, datetime.datetime(
            2020, 1, 1, 0, 0, 0, 0, timezone.utc))
        self.assertEqual(test_url.count, 1)
        self.assertEqual(test_url.last_access, datetime.datetime(
            2022, 1, 1, 0, 0, 0, 0, timezone.utc))

    def test_correct_https_link_should_be_validated(self):
        test_url = Url(original_url="google.com",
                       original_url_link="https://google.com")
        self.assertIs(validate_url_prefix(test_url.original_url_link), True)

    def test_original_url_link_generation_if_no_protocole(self):
        test_url = Url(original_url="google.com")
        test_url.save()
        self.assertEqual(test_url.original_url_link, "http://google.com")

    def test_original_url_link_generation_if_protocole(self):
        test_url = Url(original_url="https://google.com")
        test_url.save()
        self.assertEqual(test_url.original_url_link, "https://google.com")

    def test_original_url_link_if_provided(self):
        test_url = Url(original_url_link="https://google.com")
        test_url.save()
        self.assertEqual(test_url.original_url_link, "https://google.com")

    def test_original_url_link_if_provided_and_original_url_provided(self):
        test_url = Url(original_url="google.com",
                       original_url_link="https://google.com")
        test_url.save()
        self.assertEqual(test_url.original_url_link, "https://google.com")

    class UrlViewTests(TestCase):
        def test_client_get_request(self):
            client = Client()
            response = client.get('/')
            self.assertEqual(response.status_code, 200)

        def test_client_get_incorrect_request(self):
            client = Client()
            response = client.get('/incorrect', follow=True)
            self.assertEqual(response.status_code, 404)

        def test_client_get_request_shorten_view(self):
            test_url = Url(original_url="google.com")
            test_url.save()
            client = Client()
            response = client.get('/shorten {{ test_url.shorten_url }}')
            self.assertEqual(response.status_code, 200)

        def test_client_get_request_redirect_outside(self):
            test_url = Url(original_url="google.com")
            test_url.save()
            client = Client()
            response = client.get('/{{ test_url.shorten_url }}')
            self.assertEqual(response.status_code, 302)

