from recipe.models import (
    Tag,
    Recipe,
    Ingredient,
    Cart,
    Favorite,
    User,
    IngredientUnits,
)
from django.db.models import F
from django.conf import settings
from rest_framework import serializers
import base64
from django.core.files.base import ContentFile
from rest_framework.fields import IntegerField


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


class IngredientUnitsSerializers(serializers.ModelSerializer):
    "Сериализатор количеста ингредиетов для рецепта"
    id = IntegerField(write_only=True)

    class Meta:
        model = IngredientUnits
        fields = (
            "id",
            "amount",
        )


class RecipeSerializerRead(serializers.ModelSerializer):
    """Сериализатор рецептов для retrieve и list actions"""

    # # author = UserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    # is_favoured = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()
    # image = Base64ImageField()
    tags = TagSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            # "author",
            "ingredients",
            # "is_favoured",
            # "is_in_shopping_cart",
            "name",
            # "image",
            "text",
            "cooking_time",
        )

    def get_ingredients(self, obj):
        # ingredients = obj.ingredients.all()
        # ingredients1 = IngredientUnits.objects.filter(recipe=obj)
        # # val = ingredients1.amount
        # val1 = IngredientUnitsSerializers(ingredients1, many=True).data
        # return IngredientUnitsSerializers(ingredients1, many=True).data
        # # return ingredients
        recipe = obj
        ingredients = recipe.ingredients.values(
            "id",
            "name",
            "measurement_unit",
            amount=F("ingredientunits__amount"),
        )
        return ingredients


class RecipeSerializerWrite(serializers.ModelSerializer):
    """Сериализатор рецептов"""

    # tags = TagSerializer(
    #     # source="id",
    #     many=True,
    #     read_only=False,
    # )
    # tags = serializers.PrimaryKeyRelatedField(
    #     queryset=Tag.objects.all(), many=True
    # )
    # author = UserSerializer(read_only=True)
    ingredients = IngredientUnitsSerializers(many=True)
    # is_favoured = serializers.SerializerMethodField()
    # is_in_shopping_cart = serializers.SerializerMethodField()
    # image = Base64ImageField()
    # ingredients = IngridientsSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            # "author",
            "ingredients",
            #"is_favoured",
            # "is_in_shopping_cart",
            "name",
            # "image",
            "text",
            "cooking_time",
        )

    # def get_ingredients(self, obj):
    #     ingredients = obj.ingredients.all()
    #     return ingredients

    # def create(self, validated_data):
    #     va = validated_data
    #     recipe = Recipe.objects.create(**validated_data)
    #     tags_data = self.initial_data.pop("tags")
    #     recipe.tags.set(tags_data)

    #     return recipe

    def create(self, validated_data):
        tags_data = validated_data.pop("tags")
        ingredients_data = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        # print(len(ingredients_data))
        for ingredient in ingredients_data:
            IngredientUnits.objects.create(
                ingredient=Ingredient.objects.get(id=ingredient["id"]),
                recipe=recipe,
                amount=ingredient["amount"],
            )
        recipe.tags.set(tags_data)
        return recipe

    def to_representation(self, instance):
        request = self.context.get("request")
        context = {"request": request}
        inst = instance
        return RecipeSerializerRead(instance, context=context).data


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = ("id", "user", "recipe")
        read_only_fields = ('user', 'recipe')
