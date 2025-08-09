from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow safe methods for everyone. For unsafe methods, only the owner may modify.
    """
    def has_object_permission(self, request, view, obj):
        # Read-only allowed for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Otherwise only owner may modify
        return getattr(obj, 'created_by', None) == request.user
