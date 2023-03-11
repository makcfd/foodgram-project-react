from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import TagSerializer, IngridientsSerializer
from recipe.models import Tag, Ingredient


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # filter_backends = (SearchFilter,)
    # search_fields = ("name",)
    # permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngridientsSerializer
    # filter_backends = (SearchFilter,)
    # search_fields = ("name",)
    # permission_classes = (IsAdminOrReadOnly,)
