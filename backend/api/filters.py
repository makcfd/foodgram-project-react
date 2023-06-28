from django_filters.rest_framework import FilterSet, filters

from recipe.models import Ingredient, Recipe, Tag


class IngredientFilter(FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")

    class Meta:
        model = Ingredient
        fields = ("name",)


class RecipeFilter(FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        field_name="tags__slug",
        to_field_name="slug",
        queryset=Tag.objects.all(),
    )

    is_favorited = filters.BooleanFilter(method="get_favorited")
    is_in_shopping_cart = filters.BooleanFilter(method="get_shopping_cart")

    class Meta:
        model = Recipe
        fields = (
            "tags",
            "author",
        )

    def get_favorited(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(favorited__user=user)
        return queryset

    def get_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value and not user.is_anonymous:
            return queryset.filter(in_shopping_cart__user=user)
        return queryset
