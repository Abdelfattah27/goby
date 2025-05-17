from datetime import datetime
from enum import unique
from django.db import models
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password

# from delivery.models import Credits
from restaurants.models import Restaurant


class Client(models.Model):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True)
    gender = models.CharField(
        max_length=6, choices=GENDER_CHOICES, blank=True, null=True
    )

    address_current = models.CharField(max_length=100, blank=True, null=True)
    address_latitude = models.FloatField(null=True, blank=True)
    address_longitude = models.FloatField(null=True, blank=True)

    is_deliveryman = models.BooleanField(default=False)
    is_approaved_by_admin = models.BooleanField(default=False)
    

    profile_image = models.ImageField(
        upload_to="client_profiles/", blank=True, null=True
    )

    favourites = models.ManyToManyField(
        Restaurant, related_name="favourites", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    password = models.CharField(max_length=255, blank=True, null=True, default="unset")

    # For personalization / analytics
    # preferred_language = models.CharField(max_length=10, blank=True, null=True)
    # app_notifications_enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    # def get_credits(self):
    #     return Credits.objects.get(owner=self).amount

    def set_password(self, password):
        self.password = make_password(password)

    def check_password(self, password):
        if self.password == "unset":
            return password == self.phone
        return check_password(password, self.password)

    class Meta:
        ordering = ["name"]

    def delete(self, *args, **kwargs):
        if self.profile_image:
            self.profile_image.delete(save=False)
        super().delete(*args, **kwargs)


def get_today():
    return datetime.now(settings.CAIRO_TZ).today()


# class New(models.Model):
#     title = models.CharField(max_length=100, blank=True, null=True)
#     content = models.TextField(blank=True, null=True)
#     created_at = models.DateField(default=get_today)
#     picture = models.ImageField(upload_to='news/', blank=True, null=True)
#
#     class Meta:
#         ordering = ["-created_at", "-id"]
#
#     def __str__(self):
#         return self.title
#
#     def delete(self, using=None, keep_parents=False):
#         if self.picture:
#             self.picture.delete(save=False)
