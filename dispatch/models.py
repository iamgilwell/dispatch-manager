from django.db import models

from accounts.models import AddedByMixin, SlugMixin, TimeMixin


ACTIVE = "ACTIVE"
DISPATCHED = "DISPATCHED"
DELIVERED = "DELIVERY"

ITEM_CHOICES = (
    ("", "Select Status"),
    (ACTIVE, "Active"),
    (DISPATCHED, "Dispatched"),
    (DELIVERED, "Delivered"),
)

def item_images(self, filename):
    return 'media/item_images/{}/{}'.format(self.slug, filename)
class Item(AddedByMixin, SlugMixin, TimeMixin, models.Model):
    name = models.CharField(max_length=200, blank=True, verbose_name="Item Name")
    status = models.CharField(max_length=20, choices=ITEM_CHOICES, blank=True, null=True)
    estimated_time = models.PositiveIntegerField(null=True, blank=True,verbose_name="Estimate Time in(Minutes)")
    departure = models.CharField(max_length=200, null=True, blank=True)    
    destination = models.CharField(max_length=200, null=True, blank=True)
    thumbnail = models.ImageField(upload_to=item_images,null=True, blank=True)

    def __str__(self):
        return self.name

class ItemTracker(AddedByMixin, SlugMixin, TimeMixin, models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, related_name="item_tracker")
    status = models.CharField(max_length=20, choices=ITEM_CHOICES, blank=True, null=True)
    location = models.CharField(max_length=5000, null=True, blank=True)
    notes = models.CharField(max_length=5000, null=True, blank=True)
    received_date = models.DateTimeField(blank=True, null=True, editable=True)

    def __str__(self:str) -> str:
        return str(self.item)