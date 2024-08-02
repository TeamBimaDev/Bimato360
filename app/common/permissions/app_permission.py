
from rest_framework import permissions


class IsAdminOrSelfUser(permissions.BasePermission):
    """
    Permission check for user updates.
    Users are only allowed to update their own profile, admins can update all.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.is_admin()


class IsAdminUser(permissions.BasePermission):
    """
    Permission check for user deletion.
    Only admins are allowed to delete a user.
    """

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin()


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class CanEditOtherPassword(permissions.BasePermission):
    """
    Custom permission to only allow admins with 'user.user.can_edit_other_password' to edit other's password.
    """

    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True

        return request.user.user_permissions. \
            filter(codename='user.user.can_edit_other_password').exists()


class UserHasAddPermission(permissions.BasePermission):
    """
    Custom permission to only allow users with 'user.user.can_add_permission' to manage permissions.
    """

    def has_permission(self, request, view):
        return request.user.user_permissions.filter(codename='user.user.can_add_permission').exists()


class IsAdminAndCanActivateAccount(permissions.BasePermission):
    """
    Custom permission to only allow admins who have 'user.user.can_activate_account' permission to view the object.
    """

    def has_permission(self, request, view):
        return request.user.has_perm('user.user.can_activate_account')


class IsSelfUserOrUserCanUpdate(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.has_perm('user.user.can_update')


class UserCanCreateOtherUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj or request.user.has_perm('user.user.can_create')
