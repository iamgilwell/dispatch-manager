from django.db import models

from accounts.models import AddedByMixin, SlugMixin, TimeMixin


class Item(AddedByMixin,SlugMixin,TimeMixin,models.Model):
    name = models.CharField(max_length=200,blank=True, verbose_name="Item Name")
