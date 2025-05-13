from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import ClientViewSet, ClientLogin, GetClientData, ChangeClientPassword

router = DefaultRouter()
router.register("client", ClientViewSet, basename="client")

urlpatterns = [
    path("", include(router.urls)),
    path("client-login/", ClientLogin.as_view(), name="client-login"),
    path("client-data/", GetClientData.as_view(), name="client-data"),
    path(
        "change-client-password/",
        ChangeClientPassword.as_view(),
        name="change-client-password",
    ),
]
