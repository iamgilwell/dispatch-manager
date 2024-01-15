from django.contrib import admin

from dispatch.models import Item, ItemTracker

class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ['name','status','estimated_time','departure','destination','thumbnail',]
admin.site.register(Item, ItemAdmin)

class ItemTrackerAdmin(admin.ModelAdmin):
    model = ItemTracker
    list_display = ['item','status','location','notes','date',]
admin.site.register(ItemTracker, ItemTrackerAdmin)