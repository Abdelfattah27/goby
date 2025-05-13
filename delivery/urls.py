from django.urls import URLPattern, path, include
from rest_framework.routers import DefaultRouter

from .views import DeliveryViewSet

router = DefaultRouter()
router.register(r"deliveries", DeliveryViewSet, basename="deliveries")
urlpatterns = [
    path("", include(router.urls)),
]
