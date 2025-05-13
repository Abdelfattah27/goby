from rest_framework.permissions import BasePermission


class IsApprovedDeliveryMan(BasePermission):
    """
    Allows access only to approved delivery men.
    """

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated and user.is_deliveryman and user.is_approved_by_admin
        )
