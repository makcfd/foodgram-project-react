from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """Права доступа для админаф."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_superuser
        )


class IsAuthorOrReadOnly(BasePermission):
    """Правама доступа для автораф."""

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or request.user == obj.author


class IsAdminOrAuthor(BasePermission):
    """Права доступа для админов и авторов."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user == obj.author
            or request.user.is_superuser
        )
