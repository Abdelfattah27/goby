import json


class HelperMessageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.method == 'POST' and response.status_code in [200, 201]:
            lang = request.lang
            message = {
                'en': "Operation completed successfully",
                'ar': "تمت العملية بنجاح"
            }.get(lang, "تمت العملية بنجاح.")

            if isinstance(getattr(response, "data", None), dict):
                response.data = {"data": {**response.data}, "message": message}
                response._is_rendered = False
                response.render()
        return response
