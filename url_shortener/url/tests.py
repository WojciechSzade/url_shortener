from django.test import TestCase
from django.utils import timezone
from django.test.utils import setup_test_environment, teardown_test_environment
from django.test import Client
from django.urls import reverse

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


class ShortenUrlGeneratorTests(TestCase):

    def test_generate_function_with_0_raises_error(self):
        self.assertRaises(ValidationError, generate, 0)

    def test_generate_function_with_negative_raises_error(self):
        self.assertRaises(ValidationError, generate, -1)

    def test_generate_function_with_10_raises_error(self):
        self.assertRaises(ValidationError, generate, 10)

    def test_generate_function_with_string_raises_error(self):
        self.assertRaises(ValidationError, generate, "abc")

    def test_generate_function_with_float_raises_error(self):
        self.assertRaises(ValidationError, generate, 1.5)

    def test_generate_function_with_1(self):
        shorten_url = generate(1)
        self.assertIs(type(shorten_url), str)
        self.assertEqual(len(shorten_url), 1)
        for i in shorten_url:
            self.assertIn(i, string.ascii_letters + string.digits)

    def test_generate_function_with_5(self):
        shorten_url = generate(5)
        self.assertIs(type(shorten_url), str)
        self.assertEqual(len(shorten_url), 5)
        for i in shorten_url:
            self.assertIn(i, string.ascii_letters + string.digits)

    def test_generate_function_with_8(self):
        shorten_url = generate(8)
        self.assertIs(type(shorten_url), str)
        self.assertEqual(len(shorten_url), 8)
        for i in shorten_url:
            self.assertIn(i, string.ascii_letters + string.digits)

    def test_generateValidShortenUrl_with_0_raises_error(self):
        self.assertRaises(ValidationError, generateValidShortenUrl, 0)

    def test_generateValidShortenUrl_with_negative_raises_error(self):
        self.assertRaises(ValidationError, generateValidShortenUrl, -1)

    def test_generateValidShortenUrl_with_10_raises_error(self):
        self.assertRaises(ValidationError, generateValidShortenUrl, 10)

    def test_generateValidShortenUrl_with_string_raises_error(self):
        self.assertRaises(ValidationError, generateValidShortenUrl, "abc")

    def test_generateValidShortenUrl_with_float_raises_error(self):
        self.assertRaises(ValidationError, generateValidShortenUrl, 1.5)

    def test_generateValidShortenUrl_with_1(self):
        shorten_url = generateValidShortenUrl(1)
        self.assertIs(type(shorten_url), str)
        self.assertEqual(len(shorten_url), 1)
        for i in shorten_url:
            self.assertIn(i, string.ascii_letters + string.digits)
        self.assertNotIn(shorten_url, Url.objects.all(
        ).values_list('shorten_url', flat=True))

    def test_generateValidShortenUrl_with_5(self):
        shorten_url = generateValidShortenUrl(5)
        self.assertIs(type(shorten_url), str)
        self.assertEqual(len(shorten_url), 5)
        for i in shorten_url:
            self.assertIn(i, string.ascii_letters + string.digits)
        self.assertNotIn(shorten_url, Url.objects.all(
        ).values_list('shorten_url', flat=True))

    def test_generateValidShortenUrl_with_8(self):
        shorten_url = generateValidShortenUrl(8)
        self.assertIs(type(shorten_url), str)
        self.assertEqual(len(shorten_url), 8)
        for i in shorten_url:
            self.assertIn(i, string.ascii_letters + string.digits)
        self.assertNotIn(shorten_url, Url.objects.all(
        ).values_list('shorten_url', flat=True))

    def test_generateValidShortenUrl_with_1_and_existing_shorten_url_should_generate_2(self):
        for i in (string.ascii_letters + string.digits):
            Url.objects.create(shorten_url=i)
        shorten_url = generateValidShortenUrl(1)
        self.assertIs(type(shorten_url), str)
        self.assertEqual(len(shorten_url), 2)
        for i in shorten_url:
            self.assertIn(i, string.ascii_letters + string.digits)
        self.assertNotIn(shorten_url, Url.objects.all(
        ).values_list('shorten_url', flat=True))


class UrlValidatorsTests(TestCase):
    def test_validate_url_prefix_if_incorrect_prefix(self):
        self.assertIs(validate_url_prefix("google.com"), False)

    def test_validate_url_prefix_if_int_raises_error(self):
        self.assertRaises(ValidationError, validate_url_prefix, 1)

    def test_validate_url_prefix_if_correct_prefix(self):
        self.assertIs(validate_url_prefix("https://google.com"), True)
        self.assertIs(validate_url_prefix("http://google.com"), True)
        self.assertIs(validate_url_prefix("ftp://google.com"), True)
        self.assertIs(validate_url_prefix("ftps://google.com"), True)

    def test_validate_url_prefix_if_incorrect_but_ends_with_protocol(self):
        self.assertIs(validate_url_prefix("google.com/http://"), False)
        self.assertIs(validate_url_prefix("google.com/https://"), False)
        self.assertIs(validate_url_prefix("google.com/ftp://"), False)
        self.assertIs(validate_url_prefix("google.com/ftps://"), False)

    def test_validate_url_prefix_if_correct_but_ends_with_protocol(self):
        self.assertIs(validate_url_prefix("https://google.com/http://"), True)
        self.assertIs(validate_url_prefix("http://google.com/https://"), True)
        self.assertIs(validate_url_prefix("ftp://google.com/ftp://"), True)
        self.assertIs(validate_url_prefix("ftps://google.com/ftps://"), True)

    def test_validate_url_prefix_if_incorrect_but_has_protocole_in_middle(self):
        self.assertIs(validate_url_prefix(
            "google.com/http://google.com"), False)
        self.assertIs(validate_url_prefix(
            "goohttp://gle.com/https://google.com"), False)
        self.assertIs(validate_url_prefix(
            "google.com/ftp://google.com"), False)

    def test_validate_url_text_if_empty_raises_error(self):
        self.assertRaises(ValidationError, validate_url_text, "")

    def test_validate_url_text_if_int_raises_error(self):
        self.assertRaises(ValidationError, validate_url_text, 1)

    def test_validate_url_text_if_just_dot_raises_error(self):
        self.assertRaises(ValidationError, validate_url_text, ".")

    def test_validate_url_text_if_contains_space_raises_error(self):
        self.assertRaises(ValidationError, validate_url_text, "google.com ")

    def test_validate_url_text_if_contains_special_character_raises_error(self):
        self.assertRaises(ValidationError, validate_url_text, "好")

    def test_validate_url_text_if_correct(self):
        self.assertIsNone(validate_url_text("google.com"))
        self.assertIsNone(validate_url_text("google.com/"))
        self.assertIsNone(validate_url_text("google.com/abc"))
        self.assertIsNone(validate_url_text("google.com/abc/"))
        self.assertIsNone(validate_url_text("google.com/abc/def"))
        self.assertIsNone(validate_url_text("google.com/abc/def/"))
        self.assertIsNone(validate_url_text("https://google.com"))
        self.assertIsNone(validate_url_text("https://google.com/"))
        self.assertIsNone(validate_url_text("https://google.com/abc"))

    def test_validate_url_link_if_empty_raises_error(self):
        self.assertRaises(ValidationError, validate_url_link, "")

    def test_validate_url_link_if_int_raises_error(self):
        self.assertRaises(ValidationError, validate_url_link, 1)

    def test_validate_url_link_if_just_dot_raises_error(self):
        self.assertRaises(ValidationError, validate_url_link, ".")

    def test_validate_url_link_if_contains_space_raises_error(self):
        self.assertRaises(ValidationError, validate_url_link, "google.com ")

    def test_validate_url_link_if_contains_special_character_raises_error(self):
        self.assertRaises(ValidationError, validate_url_link, "好")

    def test_validate_url_if_prefix_is_incorrect(self):
        self.assertRaises(ValidationError, validate_url_link, "google.com")

    def test_validate_url_link_if_correct(self):
        self.assertIsNone(validate_url_link("https://google.com"))
        self.assertIsNone(validate_url_link("https://google.com/"))
        self.assertIsNone(validate_url_link("https://google.com/abc"))
        self.assertIsNone(validate_url_link("http://google.com/abc/"))
        self.assertIsNone(validate_url_link("http://google.com/abc/def"))
        self.assertIsNone(validate_url_link("ftp://google.com"))
        self.assertIsNone(validate_url_link("ftp://google.com/"))


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
        response = client.get(
            reverse('url:shorten', args=(test_url.shorten_url,)))
        self.assertEqual(response.status_code, 200)

    def test_client_get_request_redirect_outside(self):
        test_url = Url(original_url="google.com")
        test_url.save()
        client = Client()
        response = client.get(
            reverse('url:redirect_outside', args=(test_url.shorten_url,)))
        self.assertEqual(response.status_code, 302)

    def test_shorten_view_displays_original_url_and_shorten_url(self):
        test_url = Url(original_url="google.com")
        test_url.save()
        response = self.client.get(
            reverse('url:shorten', args=(test_url.shorten_url,)))
        self.assertContains(response, test_url.original_url)
        self.assertContains(response, test_url.shorten_url)

    def test_redirect_outside_view_redirects_to_original_url(self):
        test_url = Url(original_url="google.com")
        test_url.save()
        response = self.client.get(
            reverse('url:redirect_outside', args=(test_url.shorten_url,)))
        self.assertRedirects(response, test_url.original_url_link,
                             fetch_redirect_response=False, status_code=302)

    def test_redirect_outside_view_redirects_to_original_url_with_prefix(self):
        test_url = Url(original_url="https://google.com")
        test_url.save()
        response = self.client.get(
            reverse('url:redirect_outside', args=(test_url.shorten_url,)))
        self.assertRedirects(response, test_url.original_url_link,
                             fetch_redirect_response=False, status_code=302)

    def test_redirect_outside_view_redirects_to_original_url_with_prefix_and_slash(self):
        test_url = Url(original_url="https://www.google.com/search?q=test&sxsrf=ALiCzsYKabuujI5SyiHaoaALtC5NqdnrLQ:1668210996991&source=lnms&tbm=isch&sa=X&ved=2ahUKEwj29oqfqqf7AhVXCBAIHTDxDx8Q_AUoAXoECAIQAw&biw=1920&bih=860&dpr=1")
        test_url.save()
        response = self.client.get(
            reverse('url:redirect_outside', args=(test_url.shorten_url,)))
        self.assertRedirects(response, test_url.original_url_link, fetch_redirect_response=False, status_code=302)
