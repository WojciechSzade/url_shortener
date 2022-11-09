import datetime

from django.db import models
from django.utils import timezone

class Url(models.Model):
    original_url = models.CharField(max_length=200)
    shorten_url = models.SlugField(default ="", blank = True, null=False, db_index=True)
    pub_date = models.DateTimeField()
    last_access = models.DateTimeField() 
    count = models.IntegerField(default=0)
    def __str__(self):
        return self.original_url
    def save(self, *args, **kwargs):
        if self.pub_date == None:
            self.pub_date = timezone.now()
        if self.last_access == None:
            self.last_access = self.pub_date
        elif (self.last_access < self.pub_date):
            self.last_access = self.pub_date
        if self.count == None:
            self.count = 0
        super().save(*args, **kwargs)