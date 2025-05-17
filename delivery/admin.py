from django.contrib import admin
from django.utils.html import format_html
from .models import Delivery, LocationHistory, Credits

@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'delivery_man', 'client', 'order', 'status', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('tracking_id', 'delivery_man__name', 'client__name', 'order__id')
    readonly_fields = ('created_at', 'updated_at', 'status')
    fieldsets = (
        ('Basic Information', {
            'fields': ('tracking_id', 'delivery_man', 'client', 'order')
        }),
        ('Location Tracking', {
            'fields': ('current_latitude', 'current_longitude')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    list_per_page = 20
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def status(self, obj):
        return obj.order.status
    status.short_description = 'Order Status'

@admin.register(LocationHistory)
class LocationHistoryAdmin(admin.ModelAdmin):
    list_display = ('delivery', 'timestamp', 'coordinates', 'map_link')
    list_filter = ('delivery__tracking_id', 'timestamp')
    search_fields = ('delivery__tracking_id',)
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    ordering = ('-timestamp',)

    def coordinates(self, obj):
        return f"{obj.latitude}, {obj.longitude}"
    coordinates.short_description = 'Coordinates'

    def map_link(self, obj):
        return format_html(
            '<a href="https://www.google.com/maps?q={},{}" target="_blank">View on Map</a>',
            obj.latitude,
            obj.longitude
        )
    map_link.short_description = 'Map'

@admin.register(Credits)
class CreditsAdmin(admin.ModelAdmin):
    list_display = ('owner', 'amount', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('owner__name', 'owner__phone', 'owner__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Credit Information', {
            'fields': ('owner', 'amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    list_per_page = 20
    date_hierarchy = 'created_at'
    ordering = ('-updated_at',)