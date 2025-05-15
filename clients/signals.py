from django.dispatch import receiver
from django.db.models.signals import post_save
from clients.models import Client
from delivery.models import Credits


@receiver(post_save, sender=Client)
## had a bug in here
def create_user_credits(sender, instance, created, **kwargs):
    if created and hasattr(instance, "is_deliveryman") and instance.is_deliveryman:
        Credits.objects.get_or_create(owner=instance, defaults={"amount": 1000.00})
    elif (
        not created and hasattr(instance, "is_deliveryman") and instance.is_deliveryman
    ):
        Credits.objects.get_or_create(owner=instance, defaults={"amount": 1000.00})
