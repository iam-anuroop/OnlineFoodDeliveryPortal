from rest_framework.pagination import PageNumberPagination


class CustomUserListPagination(PageNumberPagination):
    page_size = 7
    page_query_param = "page"
