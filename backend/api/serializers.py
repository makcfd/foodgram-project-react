from recipe.models import Tag, Recipe, Ingredient, Cart, Favorite, User
from django.conf import settings
from rest_framework import serializers
import base64
from django.core.files.base import ContentFile


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            # Затем декодировать сами данные и поместить результат в файл,
            # которому дать название по шаблону.
            # TODO: передать имя рецепта для сохранения файла
            # проверить что в data есть имя
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)

        return super().to_internal_value(data)


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "id",
        )


class IngridientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиентов"""

    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "measurement_unit",
        )


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов"""

    tags = TagSerializer(
        many=True,
        read_only=True,
    )
    author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favoured = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "is_favoured",
            "is_in_shopping_cart",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def get_ingredients(self, obj):
        ingredients = obj.ingredients.all()
        return ingredients
