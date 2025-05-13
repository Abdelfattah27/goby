from django.utils import timezone
from pytz import timezone as pytz_timezone
from django.conf import settings


class GlobalTimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Activate the timezone for the entire project
        timezone.activate(pytz_timezone(settings.TIME_ZONE))
        response = self.get_response(request)
        # Deactivate the timezone after the request is completed
        timezone.deactivate()
        return response
