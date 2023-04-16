import base64

from django.contrib.auth import get_user_model
from django.db.models import F

from djoser.serializers import UserCreateSerializer, UserSerializer
from django.core.files.base import ContentFile

from rest_framework.fields import IntegerField
from rest_framework import serializers

from recipe.models import (
    Tag,
    Recipe,
    Ingredient,
    IngredientUnits,
) 
from users.models import Subscribe


User = get_user_model()


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name="temp." + ext)
        return super().to_internal_value(data)


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            User.USERNAME_FIELD,
        )
    # REQUIRED_FIELDS = (
    #     "first_name",
    #     "last_name",
    #     "email",
    #     "password",
    # )

class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "id",
            "username",
            "first_name",
            "last_name",
            "is_subscribed",
        )

    def get_is_subscribed(self, obj):
        user = self.context.get("request").user
        return user.is_anonymous and Subscribe.objects.filter(user=user, author=obj).exists()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор данных для Тегов рецепта."""

    class Meta:
        model = Tag
        fields = (
            "id",
            "name",
            "slug",
            "color",
        )


class IngridientsSerializer(serializers.ModelSerializer):
    """Сериализатор ингридиентов."""

    class Meta:
        model = Ingredient
        fields = (
            "id",
            "name",
            "measurement_unit",
        )


class IngredientUnitsSerializers(serializers.ModelSerializer):
    """Сериализатор количеста ингредиетов для рецепта"""

    id = IntegerField(write_only=True)

    class Meta:
        model = IngredientUnits
        fields = (
            "id",
            "amount",
        )


class RecipeSerializerRead(serializers.ModelSerializer):
    """Сериализатор рецептов для retrieve и list actions."""

    author = CustomUserSerializer(read_only=True)
    ingredients = serializers.SerializerMethodField()
    is_favoured = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Base64ImageField()
    tags = TagSerializer(
        many=True,
        read_only=True,
    )

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

    def get_is_favoured(self, obj):
        request = self.context.get("request")
        return obj.favorited.filter(user=request.user).exists() and not request.user.is_anonymous

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get("request")
        return obj.in_shopping_cart.filter(user=request.user).exists() and not request.user.is_anonymous

    def get_ingredients(self, obj):
        ingredients = obj.ingredients.values(
            "id",
            "name",
            "measurement_unit",
            amount=F("ingredientunits__amount"),
        )
        return ingredients


class RecipeSerializerWrite(serializers.ModelSerializer):
    """Сериализатор рецептов для записи данных."""

    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientUnitsSerializers(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            "id",
            "tags",
            "author",
            "ingredients",
            "name",
            "image",
            "text",
            "cooking_time",
        )

    def create(self, validated_data):
        tags_data = validated_data.pop("tags")
        ingredients_data = validated_data.pop("ingredients")
        recipe = Recipe.objects.create(**validated_data)
        ingredients_list = list()

        for ingredient in ingredients_data:
            ingredients_list.append(
                IngredientUnits(
                ingredient=Ingredient.objects.get(id=ingredient["id"]),
                recipe=recipe,
                amount=ingredient["amount"])
            )
        IngredientUnits.objects.bulk_create(ingredients_list)
        recipe.tags.set(tags_data)
        return recipe

    def update(self, recipe, validated_data):
        tags_data = validated_data.pop("tags")
        ingredients_data = validated_data.pop("ingredients")
        IngredientUnits.objects.filter(recipe=recipe).delete()
        for ingredient in ingredients_data:
            IngredientUnits.objects.create(
                ingredient=Ingredient.objects.get(id=ingredient["id"]),
                recipe=recipe,
                amount=ingredient["amount"],
            )
        recipe.tags.set(tags_data)
        return super().update(recipe, validated_data)

    def to_representation(self, instance):
        request = self.context.get("request")
        context = {"request": request}
        return RecipeSerializerRead(instance, context=context).data


class RecipeFavoriteAndShopping(serializers.ModelSerializer):
    """Сериализатор рецептов для избранного и списка покупок."""

    id = serializers.IntegerField(source="recipe.id")
    name = serializers.CharField(source="recipe.name")
    image = serializers.ImageField(source="recipe.image")
    cooking_time = serializers.IntegerField(source="recipe.cooking_time")

    class Meta:
        model = Recipe
        fields = (
            "id",
            "name",
            "image",
            "cooking_time",
        )
