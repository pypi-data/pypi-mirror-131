from django_filters import rest_framework as filters
from rest_framework import serializers, viewsets
from ..views import MunityViewSet

from .models import Record

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            "id",
            "dif_value",
            "next_value",
            "created",
            "user",
            "product_object_id",
            "product_content_type",
            "action",
        ]
        model = Record

class RecordsFilter(filters.FilterSet):
    class Meta:
        fields = {
            "created": ["gt", "gte", "lt", "lte"],
            "user": ["exact"],
        }
        model = Record


class RecordsViewSet(MunityViewSet):
    serializer_class = RecordSerializer
    filterset_class = RecordsFilter

