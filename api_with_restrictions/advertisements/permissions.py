from rest_framework import permissions


class IsOwnerOrReadonly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return bool(
                    request.method in permissions.SAFE_METHODS or
                    request.user and request.user.is_authenticated and request.user == obj.creator
                    )
