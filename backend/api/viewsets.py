from rest_framework import mixins
from rest_framework import viewsets


class CreateDeleteViewSet(
    mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet
):
    """
    A viewset that provides `create`, and `delete` actions.
    To use it, override the class and set the `.queryset` and
    `.serializer_class` attributes.
    """
