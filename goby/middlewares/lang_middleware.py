class LangMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        lang = request.headers.get("language", "ar")
        if lang not in "ar, en":
            lang = "ar"
        request.lang = lang
        response = self.get_response(request)
        return response
