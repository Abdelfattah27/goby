from django.contrib import admin
from django.utils.html import format_html
from .models import (User, Nationality, MaritalStatus, EmployeeType, 
                    City, CityDistrict, Employee, Moderator)
from .forms import UserAdminForm

# class UserAdmin(admin.ModelAdmin):
#     list_display = ('username', 'name', 'phone', 'is_deliveryman', 
#                    'is_approaved_by_admin', 'is_moderator', 'is_superuser')
#     list_filter = ('is_deliveryman', 'is_approaved_by_admin', 
#                   'is_moderator', 'is_superuser', 'is_root')
#     search_fields = ('username', 'name', 'phone', 'national_id')
#     fieldsets = (
#         ('Authentication', {
#             'fields': ('username', 'password')
#         }),
#         ('Personal Info', {
#             'fields': ('name', 'phone', 'national_id', 'national_id_img', 'vehicle')
#         }),
#         ('Permissions', {
#             'fields': ('is_active', 'is_deliveryman', 'is_approaved_by_admin',
#                       'is_moderator', 'is_superuser', 'is_root',
#                       'groups', 'user_permissions')
#         }),
#         ('Important Dates', {
#             'fields': ('last_login', 'date_joined')
#         }),
#     )
#     readonly_fields = ('last_login', 'date_joined')
#     filter_horizontal = ('groups', 'user_permissions')
#     list_per_page = 20

#     def national_id_img_preview(self, obj):
#         if obj.national_id_img:
#             return format_html('<img src="{}" width="100" />', obj.national_id_img.url)
#         return "No image"
#     national_id_img_preview.short_description = 'National ID Preview'

class EmployeeSettingsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 20

class CityDistrictInline(admin.TabularInline):
    model = CityDistrict
    extra = 1

@admin.register(City)
class CityAdmin(EmployeeSettingsAdmin):
    inlines = [CityDistrictInline]

@admin.register(CityDistrict)
class CityDistrictAdmin(EmployeeSettingsAdmin):
    list_display = ('name', 'city')
    list_filter = ('city',)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'gander', 'nationality', 'phone', 'city', 
                   'district', 'emp_type', 'photo_preview')
    list_filter = ('gander', 'nationality', 'city', 'emp_type')
    search_fields = ('name', 'phone', 'phone2', 'national_id')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'gander', 'birth_date', 'age', 'photo', 'photo_preview')
        }),
        ('Identity Information', {
            'fields': ('nationality', 'religion', 'marital_status', 'national_id')
        }),
        ('Contact Information', {
            'fields': ('phone', 'phone2', 'city', 'district', 'address')
        }),
        ('Employment Information', {
            'fields': ('emp_type', 'added_by')
        }),
    )
    readonly_fields = ('photo_preview', 'age')
    list_per_page = 20

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%; object-fit: cover;" />', obj.photo.url)
        return "No photo"
    photo_preview.short_description = 'Photo'

    def save_model(self, request, obj, sender, form, change):
        if not obj.added_by:
            obj.added_by = request.user
        super().save_model(request, obj, sender, form, change)

@admin.register(Moderator)
class ModeratorAdmin(admin.ModelAdmin):
    list_display = ('employee', 'user', 'moderator_status')
    search_fields = ('employee__name', 'user__username')
    list_per_page = 20

    def moderator_status(self, obj):
        if obj.user and obj.user.is_moderator:
            return format_html('<span style="color: green;">✓ Active</span>')
        return format_html('<span style="color: red;">✗ Inactive</span>')
    moderator_status.short_description = 'Status'
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import (User, Nationality, MaritalStatus, EmployeeType, 
                    City, CityDistrict, Employee, Moderator)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'name', 'phone', 'is_restaurant', 'is_deliveryman', 
                   'is_moderator', 'is_approaved_by_admin', 'is_active')
    list_filter = ('is_restaurant', 'is_deliveryman', 'is_moderator', 
                  'is_approaved_by_admin', 'is_active')
    search_fields = ('username', 'name', 'phone', 'national_id')
    actions = ['approve_users', 'disapprove_users', 'make_restaurant_users']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {
            'fields': ('name', 'phone', 'national_id', 'national_id_img', 'vehicle')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_restaurant', 'is_deliveryman', 
                      'is_moderator', 'is_approaved_by_admin',
                      'is_superuser', 'is_root', 'groups', 'user_permissions')
        }),
    )
    
    def get_fieldsets(self, request, obj=None):
        if not request.user.is_superuser:
            return (
                (None, {'fields': ('username', 'password')}),
                ('Personal Info', {
                    'fields': ('name', 'phone', 'national_id', 'national_id_img')
                }),
                ('Status', {
                    'fields': ('is_active', 'is_approaved_by_admin')
                }),
            )
        return super().get_fieldsets(request, obj)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs
    
    def approve_users(self, request, queryset):
        queryset.update(is_approaved_by_admin=True)
    approve_users.short_description = "Approve selected users"
    
    def disapprove_users(self, request, queryset):
        queryset.update(is_approaved_by_admin=False)
    disapprove_users.short_description = "Disapprove selected users"
    
    def make_restaurant_users(self, request, queryset):
        queryset.update(is_restaurant=True)
    make_restaurant_users.short_description = "Mark as restaurant users"
    
    def national_id_img_preview(self, obj):
        if obj.national_id_img:
            return format_html('<img src="{}" width="100" />', obj.national_id_img.url)
        return "No image"
    national_id_img_preview.short_description = 'National ID'

admin.site.register(User, CustomUserAdmin)

# Register models
# admin.site.register(User, UserAdmin)
admin.site.register(Nationality, EmployeeSettingsAdmin)
admin.site.register(MaritalStatus, EmployeeSettingsAdmin)
admin.site.register(EmployeeType, EmployeeSettingsAdmin)
# admin.site.register(User, UserAdminForm)

# admin.site.register(Employee)
# admin.site.register(EmployeeType)
# admin.site.register(Nationality)
# admin.site.register(City)
# admin.site.register(MaritalStatus)
# admin.site.register(CityDistrict)
# admin.site.register(Moderator)
# admin.site.unregister(Group)
