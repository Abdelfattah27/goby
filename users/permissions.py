from rest_framework import permissions


class CanAdd(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(
            f'{view.queryset.model._meta.app_label}.add_{view.queryset.model._meta.model_name}')


class CanEdit(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(
            f'{view.queryset.model._meta.app_label}.change_{view.queryset.model._meta.model_name}')


class CanDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(
            f'{view.queryset.model._meta.app_label}.delete_{view.queryset.model._meta.model_name}')


class CanView(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm(
            f'{view.queryset.model._meta.app_label}.view_{view.queryset.model._meta.model_name}')
