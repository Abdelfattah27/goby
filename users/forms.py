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


from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from restaurants.models import Restaurant

class RestaurantSignUpForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=True, help_text="Required for contact")
    restaurant_name = forms.CharField(max_length=100, required=True)
    merchant_type = forms.ChoiceField(choices=Restaurant.MERCHANT_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'phone', 'password1', 'password2']

class RestaurantLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)