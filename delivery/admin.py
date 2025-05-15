from django.contrib import admin

from delivery.models import Credits, Delivery, LocationHistory


admin.site.register(Credits)
admin.site.register(LocationHistory)
admin.site.register(Delivery)
