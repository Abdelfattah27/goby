from django.urls import path
from .views import *


urlpatterns = [
    path("send/", send, name="send-email"),
]
