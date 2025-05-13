from django.db import models
from django.views.generic.dates import timezone_today

from django.utils import timezone

from users.models import User
from restaurants.models import Order


# Create your models here.


class Delivery(models.Model):
    tracking_id = models.CharField(max_length=100, unique=True)
    delivery_man = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="delivery_man"
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="delivery_order"
    )
    client = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="delivery_order"
    )
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Delivery {self.tracking_id}, Delivery_man {self.delivery_man}"

    def status(self):
        return f"{self.order.status}"


## History just to be able to know where the delivery guy went
## will only do it if I get some time
## also will probably be liek a json array or something
class LocationHistory(models.Model):
    delivery = models.ForeignKey(
        Delivery, on_delete=models.CASCADE, related_name="locations"
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.delivery.tracking_id} @ {self.timestamp}"


class Credits(models.Model):
    owner = models.OneToOneField(
        User, on_delete=models.RESTRICT, related_name="credits"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner.username}'s Credits: {self.amount}"
