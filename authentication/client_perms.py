from rest_framework import permissions


class IsClientAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(not request.user.is_anonymous)
