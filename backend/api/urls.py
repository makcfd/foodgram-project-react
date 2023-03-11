from rest_framework import routers
from django.urls import include, path

from api.views import TagViewSet, IngredientViewSet


router = routers.DefaultRouter()

router.register("tags", TagViewSet)
router.register("ingredients", IngredientViewSet)

urlpatterns = [
    path("v1/", include(router.urls)),
]
