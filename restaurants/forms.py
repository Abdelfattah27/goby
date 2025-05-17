from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Restaurant

class UserRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password1', 'password2']

class RestaurantRegistrationForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name_ar', 'description_ar', 'merchant_type', 'image', 'cover']
        widgets = {
            'description_ar': forms.Textarea(attrs={'rows': 4}),
        }

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )