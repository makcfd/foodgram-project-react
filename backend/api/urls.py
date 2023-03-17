from rest_framework import routers
from django.urls import include, path
from api.views import (
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet,
    FavoriteViewSet,
)


router = routers.DefaultRouter()

router.register("tags", TagViewSet)
router.register("ingredients", IngredientViewSet)
router.register(r'^recipes/(?P<id>\d+)/favorite', FavoriteViewSet)
router.register("recipes", RecipeViewSet)


urlpatterns = [
    path("", include(router.urls)),
]
