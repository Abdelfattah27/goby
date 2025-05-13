### currently unused
from rest_framework.permissions import DjangoModelPermissions


class CustomDjangoModelPermissions(DjangoModelPermissions):
    """
    Custom DjangoModelPermissions that enforces 'view' permission on safe methods
    and 'add', 'change', 'delete' permissions on unsafe methods.
    """
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],  # Enforces 'view' permission on GET
        'OPTIONS': ['%(app_label)s.view_%(model_name)s'],
        'HEAD': ['%(app_label)s.view_%(model_name)s'],
        'POST': ['%(app_label)s.add_%(model_name)s'],  # Enforces 'add' permission on POST
        'PUT': ['%(app_label)s.change_%(model_name)s'],  # Enforces 'change' permission on PUT
        'PATCH': ['%(app_label)s.change_%(model_name)s'],  # Enforces 'change' permission on PATCH
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],  # Enforces 'delete' permission on DELETE
    }
