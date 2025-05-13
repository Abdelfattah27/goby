from django.contrib.auth.admin import UserAdmin
from .models import User


class UserAdminForm(UserAdmin):
    model = User

    list_display = ('username', 'name', 'phone', 'national_id', 'is_superuser')
    list_filter = ('username', 'name', 'phone', 'national_id')
    fieldsets = [
        ("Personal Information", {'fields': ['name', 'phone', 'national_id']}),
        ("Authentication", {'fields': ['username', 'password']}),
        ("Permissions", {'fields': ['is_active', 'is_moderator', 'is_superuser', 'is_root', 'user_permissions']}),
    ]
    add_fieldsets = [
        (None, {'fields': ['username', 'password1', 'password2', 'name', 'phone', 'national_id', 'is_active',
                           'is_moderator', 'is_superuser']}),
    ]
