def get_translated_field(request, ar, en):
    if request.lang == "en" and en and en .strip:
        return en
    return ar
