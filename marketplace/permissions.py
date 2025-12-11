from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # (GET, HEAD, OPTIONS) available for anyone
        if request.method in permissions.SAFE_METHODS:
            return True

        # (PUT, DELETE) only for creator
        return obj.addedBy == request.user