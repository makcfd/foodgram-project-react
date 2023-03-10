from rest_framework import routers
from django.urls import include, path

from api.views import TagViewSet


router = routers.DefaultRouter()

router.register("tags", TagViewSet)


urlpatterns = [
    path("v1/", include(router.urls)),
]
