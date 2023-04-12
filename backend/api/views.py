from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import get_object_or_404

from api.serializers import (
    TagSerializer,
    IngridientsSerializer,
    RecipeSerializerRead,
    RecipeSerializerWrite,
    RecipeFavoriteAndShopping,
)
from api.viewsets import CreateDeleteViewSet
from api.filters import IngredientFilter, RecipeFilter
from recipe.models import (
    Tag,
    Ingredient,
    Recipe,
    Favorite,
    IngredientUnits,
    ShoppingCart,
)
from api.permissions import IsAdminOrAuthor, IsAdminOrReadOnly


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngridientsSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = IngredientFilter
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAdminOrAuthor,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action in (
            "list",
            "retrieve",
        ):
            return RecipeSerializerRead
        return RecipeSerializerWrite

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.save(Favorite, request.user, pk)
        else:
            return self.remove(Favorite, request.user, pk)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.save(ShoppingCart, request.user, pk)
        else:
            return self.remove(ShoppingCart, request.user, pk)

    def save(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            return Response({"errors": "Рецепт уже добавлен!"},
                            status=status.HTTP_400_BAD_REQUEST)
        recipe = get_object_or_404(Recipe, id=pk)
        obj = model.objects.create(user=user, recipe=recipe)
        serializer = RecipeFavoriteAndShopping(obj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def remove(self, model, user, pk):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response({"message": 
                             "Рецепт успешно удален."},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({"errors": "Рецепт уже удален!"},
                        status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        user = request.user
        ingredients = (
            IngredientUnits.objects.filter(recipe__in_shopping_cart__user=user)
            .values("ingredient__name", "ingredient__measurement_unit")
            .annotate(total_amount=Sum("amount"))
        )
        data = ingredients.values_list(
            "ingredient__name", "ingredient__measurement_unit", "total_amount"
        )
        shopping_cart = "Список покупок:\n"
        for name, measure, amount in data:
            shopping_cart += f"{name.capitalize()} {amount} {measure},\n"

        return HttpResponse(shopping_cart, content_type="text/plain")
