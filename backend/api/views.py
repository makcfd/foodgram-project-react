from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.serializers import (
    TagSerializer,
    IngridientsSerializer,
    RecipeSerializerRead,
    RecipeSerializerWrite,
)
from recipe.models import Tag, Ingredient, Recipe


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


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeSerializerRead
        return RecipeSerializerWrite

    # filter_backends = (SearchFilter,)
    # search_fields = ("name",)
    # permission_classes = (IsAdminOrReadOnly,)
