from rest_framework.permissions import SAFE_METHODS, BasePermission

STAFF_ROLES = ('moderator', 'admin')


def is_role(request, role):
    if request.user and request.user.is_authenticated:
        return (request.user.role == role
                or request.user.is_superuser)
    return False


class IsAdministrator(BasePermission):
    def has_permission(self, request, view):
        return is_role(request, 'admin')


class IsAdministratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or is_role(request, 'admin'))


class IsAuthorModeratorAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (True if request.method in SAFE_METHODS
                else (obj.author == request.user
                      or request.user.role in STAFF_ROLES
                      or request.user.is_superuser))
