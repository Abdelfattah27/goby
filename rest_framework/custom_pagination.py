from rest_framework.pagination import PageNumberPagination, BasePagination
from rest_framework.response import Response
from math import ceil


class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'

    def paginate_queryset(self, queryset, request, view=None):
        no_pagination = request.query_params.get('no_pagination')
        if no_pagination:
            return None
        return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        lang = self.request.lang
        count = self.page.paginator.count
        total_pages = ceil(count / self.get_page_size(self.request))
        message = {"en": "Data retrieved successfully", "ar": "تم الحصول على البيانات"}.get(lang,
                                                                                            "تم الحصول على البيانات") if count > 0 else {
            "en": "No results found", "ar": "لا توجد بيانات"}.get(lang, "لا توجد بيانات")

        return Response({
            "meta": {
                'total_pages': total_pages,
                'current_page': self.page.number,
                'count': self.page.paginator.count,
                'next': self.get_next_link(),
                'previous': self.get_previous_link(),
            },
            'data': data,
            "message": message,
        })


class NoPagination(BasePagination):
    def __init__(self):
        self.lang = None

    def paginate_queryset(self, queryset, request, view=None):
        self.lang = request.lang
        return list(queryset)

    def get_paginated_response(self, data):
        count = len(data)
        message = {"en": "Data retrieved successfully", "ar": "تم الحصول على البيانات"}.get(self.lang,
                                                                                            "تم الحصول على البيانات") if count > 0 else {
            "en": "No results found", "ar": "لا توجد بيانات"}.get(self.lang, "لا توجد بيانات")
        return Response({
            "data": data,
            "message": message,
        })
