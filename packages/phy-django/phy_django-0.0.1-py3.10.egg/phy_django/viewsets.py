from django.db.transaction import atomic
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination, CursorPagination, LimitOffsetPagination
from rest_framework.viewsets import *

__keep = (
    action, atomic,
    PageNumberPagination, CursorPagination, LimitOffsetPagination,
)


class ModelViewSet(ModelViewSet):
    pagination_class = LimitOffsetPagination
