from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 10  # الحجم الافتراضي
    page_size_query_param = 'page_size'  # يفعّل ?page_size=3
    max_page_size = 100  # أقصى حجم ممكن
