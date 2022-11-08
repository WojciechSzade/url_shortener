from django.db import models
from django.utils.text import slugify

class Url(models.Model):
    original_url = models.CharField(max_length=200)
    shorten_url = models.CharField(max_length=30)
    pub_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField(default ="", blank = True, null=False, db_index=True)
    count = models.IntegerField(default=0)
    def __str__(self):
        return f"{self.original_url} -> {self.shorten_url}"
    
    def save(self, *args, **kwargs):
        if (self.original_url[0:4] != "http" and self.original_url[0:5] != "https"):
            self.original_url = "http://" + self.original_url
        self.slug = slugify(self.shorten_url)
        super().save(*args, **kwargs)