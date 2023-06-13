from rest_framework.permissions import BasePermission


class IsAdministrator(BasePermission):
    # TODO Заглушка. Надо сделать реальный пермишн
    def has_permission(self, request, view):

        return True
