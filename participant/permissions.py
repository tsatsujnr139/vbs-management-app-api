from rest_framework import permissions


class isAdminUser(permissions.BasePermission):
    """ Only allow admins to access list of objects"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            if view.action == 'create':
                return True
            elif view.action == 'count':
                return True
            else:
                return False
        else:
            return True
