from rest_framework.permissions import BasePermission

def has_role(user, allowed_roles):
    if user.is_superuser:
        return True
    try:
        return user.user_role.role.name in allowed_roles
    except:
        return False

class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return has_role(request.user, ['Admin'])

class IsSupportOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return has_role(request.user, ['Admin', 'Support'])

class IsReadOnlyAllowed(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return has_role(request.user, ['Admin', 'Support', 'ReadOnly'])
        return has_role(request.user, ['Admin', 'Support'])