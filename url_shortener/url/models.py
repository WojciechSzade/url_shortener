from django.db import models
from django.utils.text import slugify

class Url(models.Model):
    original_url = models.CharField(max_length=200)
    shorten_url = models.SlugField(default ="", blank = True, null=False, db_index=True)
    pub_date = models.DateTimeField(auto_now=True)
    last_access = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        # if (self.original_url[0:4] != "http" and self.original_url[0:5] != "https"):
        #     self.original_url = "http://" + self.original_url
        if self.last_access == None:
            self.last_access = self.pub_date
        elif (self.last_access < self.pub_date):
            self.last_access = self.pub_date
        super().save(*args, **kwargs)