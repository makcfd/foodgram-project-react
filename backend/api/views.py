from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.generics import get_object_or_404
from api.serializers import (
    TagSerializer,
    IngridientsSerializer,
    RecipeSerializerRead,
    RecipeSerializerWrite,
    FavoriteSerializer,
)
from api.viewsets import CreateDeleteViewSet
from api.filters import IngredientFilter
from recipe.models import Tag, Ingredient, Recipe, Favorite, User
from django_filters.rest_framework import DjangoFilterBackend


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    # filter_backends = (SearchFilter,)
    # search_fields = ("name",)
    # permission_classes = (IsAdminOrReadOnly,)


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngridientsSerializer
    # permission_classes = (IsAdminOrReadOnly,)
    filterset_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return RecipeSerializerRead
        return RecipeSerializerWrite

    # filter_backends = (SearchFilter,)
    # search_fields = ("name",)
    # permission_classes = (IsAdminOrReadOnly,)


class FavoriteViewSet(CreateDeleteViewSet):
    serializer_class = FavoriteSerializer
    queryset = Favorite.objects.all()
    # def get_queryset(self):
    #     post_id = self.kwargs.get("id")
    #     post = get_object_or_404(Favorite, pk=post_id)
    #     return post.comments.all()

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get("id")
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        real_user = get_object_or_404(User, pk=self.request.user.id),
        user = self.request.user
        serializer.save(user=real_user, recipe=recipe)
