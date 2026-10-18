from rest_framework.permissions import BasePermission


class IsArtisan(BasePermission):

    def has_permission(self, request, view):
        return hasattr(request.user, "artisan_profile")
