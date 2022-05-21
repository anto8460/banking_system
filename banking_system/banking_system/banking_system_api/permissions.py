
from rest_framework import permissions
from banking_system_app.models import KnownBank


class IsBankOrNoAccess(permissions.BasePermission):

    def has_permission(self, request, view):
        is_bank = KnownBank.objects.filter(user_id=request.user.id)
        return is_bank
