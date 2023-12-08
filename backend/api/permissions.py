from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """Права доступа к ресурсу."""

    def has_object_permission(self, request, view, obj):
        """Функция проверки доступа к ресурсу."""
        return request.method in SAFE_METHODS or obj.author == request.user
