from rest_framework import permissions

class IsAdminOrReviewer(permissions.BasePermission):
    """
    Custom permission to allow only reviewers or admin users to modify a review.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True 
        return request.user and (
            request.user.is_staff or request.user == obj.reviewer
        )

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Read-only for all, write access only for admin.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True 
        return request.user.is_staff 
