from django.contrib import admin
from django.utils.html import format_html
from .models import Client

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'gender', 'is_deliveryman', 'is_approaved_by_admin', 'profile_image_tag', 'created_at')
    list_filter = ('is_deliveryman', 'is_approaved_by_admin', 'gender', 'created_at')
    search_fields = ('name', 'phone', 'email')
    readonly_fields = ('profile_image_tag', 'created_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'phone', 'email', 'gender')
        }),
        ('Location', {
            'fields': ('address_current', 'address_latitude', 'address_longitude')
        }),
        ('Status', {
            'fields': ('is_deliveryman', 'is_approaved_by_admin')
        }),
        ('Media & Favorites', {
            'fields': ('profile_image', 'profile_image_tag', 'favourites')
        }),
        ('Dates', {
            'fields': ('created_at',)
        }),
    )
    filter_horizontal = ('favourites',)
    list_per_page = 20
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

    def profile_image_tag(self, obj):
        if obj.profile_image:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />'.format(obj.profile_image.url))
        return "-"
    profile_image_tag.short_description = 'Profile Image'

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     # Make password field read-only unless adding a new client
    #     if obj and 'password' in form.base_fields:
    #         form.base_fields['password'].disabled = True
    #         form.base_fields['password'].help_text = 'Raw passwords are not stored, so there is no way to see this user\'s password.'
    #     return form

    # def save_model(self, request, obj, form, change):
    #     # Only update password if it's changed (and not the default "unset")
    #     if 'password' in form.changed_data and obj.password != 'unset':
    #         obj.set_password(form.cleaned_data['password'])
    #     super().save_model(request, obj, form, change)