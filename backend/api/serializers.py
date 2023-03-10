from recipe.models import Tag, Recipe, Ingredient, Cart, Favorite
from django.conf import settings
from rest_framework import serializers


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор данных для Тегов рецепта"""

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "slug",
            "color",
        )
