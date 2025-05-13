from django.core.mail import send_mail
from django.http import HttpResponse
# from django.conf import settings


def send(request):
    send_mail(
        "Test Subject",
        "Here is the message.",
        "PRO GYM",
        ["ahmedhatemezzathelal@gmail.com", "ahmed.hatem@sh-eng.menofia.edu.eg"],
        fail_silently=False,
    )
    return HttpResponse("Email sent!")
