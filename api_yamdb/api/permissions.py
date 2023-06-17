from rest_framework.permissions import SAFE_METHODS, BasePermission


def is_role(request, role):
    if request.user and request.user.is_authenticated:
        return request.user.role == role
    return False


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        return (is_role(request, 'admin')
                or request.user.is_superuser)


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return is_role(request, 'moderator')


class IsAdministratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or is_role(request, 'admin'))
