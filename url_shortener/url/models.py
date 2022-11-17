import datetime
import random
import string

from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import *

valid_url_prefix = ["http://", "https://", "ftp://",
                    "ftps://"]  # used in validate_url_prefix
maxShortenUrlLength = 8  # max length of shorten url


def validate_value_to_validators(value):
    """function used to validate if the value is valid -> is it a string only containg proper characters for validators"""
    if type(value) != str:
        raise ValidationError("Value must be string")
    for i in value:
        if i not in string.ascii_letters + string.digits + string.punctuation:
            raise ValidationError(
                "Value can contain only letters and digits and punctuations! No spaces and special charactes allowed!")


def validate_value_to_generator(value):
    """function used to validate if the value is valid -> is it a number between 1 and maxShortenUrlLength"""
    if type(value) != int:
        raise ValidationError("Value must be integer")
    if value < 1:
        raise ValidationError("Value must be at least 1")
    if value > maxShortenUrlLength:
        raise ValidationError(
            "Value must be at most" + str(maxShortenUrlLength) + "or Were unable to generate unique url with length less than" + str(maxShortenUrlLength))


def generate(shorten_url_length):
    """function used in generateValidShortenUrl to generate a combination of letters and digits of given length"""
    validate_value_to_generator(shorten_url_length)
    shorten_url = ""
    for i in range(shorten_url_length):
        shorten_url += random.choice(string.ascii_letters + string.digits)
    return shorten_url


def generateValidShortenUrl(shorten_url_length):
    """function used to generate valid, unique shorten url"""
    validate_value_to_generator(shorten_url_length)
    shorten_url = generate(shorten_url_length)
    for i in range(9):
        if Url.objects.filter(shorten_url=shorten_url).exists():
            shorten_url = generate(shorten_url_length)
        else:
            return shorten_url
    # if we were unable to generate unique shorten_url with given length, we try to generate shorten_url with length + 1 (untill length = 8)
    else:
        return generateValidShortenUrl(shorten_url_length + 1)


def validate_url_prefix(value):
    """function used to validate if the url starts with valid prefix (protocol), doesn"t raise error (used to generate valid url)"""
    validate_value_to_validators(value)
    for prefix in valid_url_prefix:
        if value.startswith(prefix):
            return True
    return False


def validate_url_text(value):
    """used in validate_url_link"""
    validate_value_to_validators(value)
    if "." not in value:
        raise ValidationError("Url must contain at least one dot!")
    if len(value) < 2:
        raise ValidationError("Url must contain at least 2 characters")
    if value[0] == ".":
        raise ValidationError("Url can't start with dot")


def validate_url_link(value):
    """function used to validate if the url starts with valid prefix (protocol) and has at least one dot (raises error)"""
    if not validate_url_prefix(value):
        raise ValidationError(
            "Url must start with http://, https://, ftp:// or ftps://")
    validate_url_text(value)


def validate_date(value):
    if value > timezone.now():
        raise ValidationError("Date can't be in the future")


class Url(models.Model):
    # default value for shorten_url_length is 5, changed automaticly if generateValidShortenUrl can"t generate unique value of this lenght, max length is in maxShortenUrlLength
    shorten_url_length = models.IntegerField(default=5, validators=(
        MaxValueValidator(maxShortenUrlLength), MinValueValidator(1)))
    original_url = models.CharField(max_length=250, blank=False, help_text="Enter the URL you want to shorten", validators=[
                                    validate_url_text, MinLengthValidator(2)], verbose_name="Original URL text")
    original_url_link = models.URLField(max_length=250, null=True, help_text="original_url with protocol if needed", validators=[
                                        validate_url_link, URLValidator, MinLengthValidator(2)], verbose_name="Original URL url")
    shorten_url = models.SlugField(max_length=maxShortenUrlLength, primary_key=True, validators=[
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
        if len(self.shorten_url) != self.shorten_url_length:
            if len(self.shorten_url) < maxShortenUrlLength:
                self.shorten_url_length = len(self.shorten_url)
            else:
                raise ValidationError("Shorten url length must be at most" + str(maxShortenUrlLength) +
                                      "or Were unable to generate unique url with length less than" + str(maxShortenUrlLength))
        if not validate_url_prefix(self.original_url) and self.original_url_link is None:
            self.original_url_link = "http://" + self.original_url
        elif validate_url_prefix(self.original_url) and self.original_url_link is None:
            self.original_url_link = self.original_url
        super(Url, self).save(*args, **kwargs)
