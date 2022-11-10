import datetime
import random
import string

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import *

valid_url_prefix = ["http://", "https://", "ftp://", "ftps://"]


def generate(shorten_url_length):
    shorten_url = ""
    for i in range(shorten_url_length):
        shorten_url += random.choice(string.ascii_letters + string.digits)
    return shorten_url


def generateValidShortenUrl(shorten_url_length):
    shorten_url = generate(shorten_url_length)
    for i in range(9):
        if Url.objects.filter(shorten_url=shorten_url).exists():
            shorten_url = generate(shorten_url_length)
        else:
            return shorten_url
    raise ValidationError("Can't generate valid shorten url")


def validate_url_prefix(value):
    for prefix in valid_url_prefix:
        if value.startswith(prefix):
            return True
    return False


def validate_url_text(value):
    if "." not in value:
        raise ValidationError("Url must contain at least one dot!")


def validate_url_link(value):
    if not validate_url_prefix(value):
        raise ValidationError(
            "Url must start with http://, https://, ftp:// or ftps://")
    validate_url_text(value)


def validate_date(value):
    if value > timezone.now():
        raise ValidationError("Date can't be in the future")


class Url(models.Model):
    shorten_url_length = 5
    original_url = models.CharField(max_length=250, blank=False, help_text="Enter the URL you want to shorten", validators=[
                                    validate_url_text, MinLengthValidator(2)], verbose_name="Original URL text")
    original_url_link = models.URLField(max_length=250, null=True, help_text="original_url with protocol if needed", validators=[
                                        validate_url_link, URLValidator, MinLengthValidator(2)], verbose_name="Original URL url")
    shorten_url = models.SlugField(max_length=shorten_url_length, primary_key=True, validators=[
                                   validate_slug], verbose_name="Shorten URL slug")
    pub_date = models.DateTimeField(default=timezone.now, validators=[
                                    validate_date], verbose_name="Publication date")
    last_access = models.DateTimeField(default=timezone.now, validators=[
                                       validate_date], verbose_name="Last access date")
    count = models.IntegerField(default=0, verbose_name="Number of accesses")

    def __str__(self):
        return (self.shorten_url + " -> " + self.original_url)

    def save(self, *args, **kwargs):
        if not self.shorten_url:
            self.shorten_url = generateValidShortenUrl(self.shorten_url_length)
        if not validate_url_prefix(self.original_url) and self.original_url_link is None:
            self.original_url_link = "http://" + self.original_url
        elif validate_url_prefix(self.original_url) and self.original_url_link is None:
            self.original_url_link = self.original_url
        super(Url, self).save(*args, **kwargs)
