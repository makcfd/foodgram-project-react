from django_filters import rest_framework as filters
from recipe.models import Ingredient


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(field_name="name", lookup_expr="icontains")
    # name = filters.CharFilter(field_name="name")

    class Meta:
        model = Ingredient
        fields = ("name",)
