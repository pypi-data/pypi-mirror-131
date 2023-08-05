from django.db.transaction import atomic
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination, CursorPagination, LimitOffsetPagination
from rest_framework.viewsets import *

__keep = (
    action, atomic,
    PageNumberPagination, CursorPagination, LimitOffsetPagination,
)


class ModelViewSet(ModelViewSet):
    """符合我的开发习惯的配置"""
    pagination_class = LimitOffsetPagination
