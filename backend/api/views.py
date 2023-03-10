from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import TagSerializer
from recipe.models import Tag


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # filter_backends = (SearchFilter,)
    # search_fields = ("name",)
    # permission_classes = (IsAdminOrReadOnly,)
