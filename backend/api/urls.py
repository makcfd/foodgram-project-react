from rest_framework import routers
from django.urls import include, path
from api.views import (
    UsersViewSet,
    TagViewSet,
    IngredientViewSet,
    RecipeViewSet,
)

router = routers.DefaultRouter()

router.register("tags", TagViewSet)
router.register("ingredients", IngredientViewSet)
router.register("recipes", RecipeViewSet)
router.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path("", include(router.urls)),
]
