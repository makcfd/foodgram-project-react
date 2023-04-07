from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated

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
        methods=["POST", "DELETE"],
        permission_classes=(IsAuthenticated,),
    )
    def shopping_cart(self, request, pk):
        if request.method == "POST":
            try:
                recipe = Recipe.objects.get(pk=pk)
            except Recipe.DoesNotExist:
                return Response(
                    {"errors": "Рецепт не найден"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            shopping_cart, created = ShoppingCart.objects.get_or_create(
                user=request.user, recipe=recipe
            )
            if not created:
                return Response(
                    {"errors": "Уже в списке покупок"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer = RecipeFavoriteAndShopping(shopping_cart)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )

        if request.method == "DELETE":
            try:
                recipe = Recipe.objects.get(pk=pk)
            except Recipe.DoesNotExist:
                return Response(
                    {"errors": "Рецепт не найден"},
                    status=status.HTTP_404_NOT_FOUND,
                )
            try:
                shopping_recipe = ShoppingCart.objects.get(
                    user=request.user, recipe=recipe
                )
                shopping_recipe.delete()
                return Response(
                    {"detail": "Рецепт успешно удален из списка покупок"},
                    status=status.HTTP_204_NO_CONTENT,
                )
            except ShoppingCart.DoesNotExist:
                return Response(
                    {"errors": "В списке покупок рецепт не найден"},
                    status=status.HTTP_404_NOT_FOUND,
                )

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


class FavoriteCreateDeleteViewSet(CreateDeleteViewSet):
    queryset = Favorite.objects.all()
    serializer_class = RecipeFavoriteAndShopping
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        recipe_id = kwargs.get("id")
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Recipe.DoesNotExist:
            return Response(
                {"errors": "Рецепт не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )
        favorite, created = Favorite.objects.get_or_create(
            user=request.user, recipe=recipe
        )
        if not created:
            return Response(
                {"errors": "Уже в избранном"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(instance=favorite)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

    def delete(self, request, *args, **kwargs):
        recipe_id = kwargs.get("id")
        try:
            recipe = Recipe.objects.get(pk=recipe_id)
        except Recipe.DoesNotExist:
            return Response(
                {"errors": "Рецепт не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            favorite = Favorite.objects.get(user=request.user, recipe=recipe)
            favorite.delete()
            return Response(
                {"detail": "Рецепт успешно удален из избранного"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Favorite.DoesNotExist:
            return Response(
                {"errors": "В избранном рецепт не найден"},
                status=status.HTTP_404_NOT_FOUND,
            )
