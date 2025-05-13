from rest_framework_simplejwt.authentication import JWTAuthentication

from clients.models import Client
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication

# from rest_framework.exceptions import AuthenticationFailed


class ClientJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = JWTAuthentication()
        lang = getattr(request, "lang", "en")

        def _(en_msg, ar_msg):
            return ar_msg if lang == "ar" else en_msg

        try:
            header = request.headers.get("Authorization")
            if not header:
                raise exceptions.AuthenticationFailed(
                    _("Authorization header missing.", "رأس المصادقة مفقود.")
                )

            raw_token = auth.get_raw_token(header.encode())
            validated_token = auth.get_validated_token(raw_token)
            client_id = validated_token.get("client_id")

            if not client_id:
                raise exceptions.AuthenticationFailed(
                    _("Invalid token payload.", "محتوى الرمز غير صالح.")
                )

            try:
                client = Client.objects.get(id=client_id)
                return client, validated_token
            except Client.DoesNotExist:
                raise exceptions.AuthenticationFailed(
                    _("Client not found.", "العميل غير موجود.")
                )

        except exceptions.AuthenticationFailed as e:
            raise exceptions.AuthenticationFailed(
                _(f"Authentication error: {str(e)}", f"خطأ في المصادقة: {str(e)}")
            )
