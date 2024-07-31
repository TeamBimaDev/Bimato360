<<<<<<< HEAD
from rest_framework import permissions


class ActionBasedPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if not hasattr(view, 'action_permissions'):
            return True

        action = view.action
        app_label = view.queryset.model._meta.app_label

        required_permission = view.action_permissions.get(action)

        if required_permission:
            if isinstance(required_permission, list):
                required_permission = required_permission[0]

            permission_codename = f"{app_label}.{required_permission}"

            if not request.user.user_permissions.filter(codename=permission_codename).exists():
                return False

        return True
=======
from rest_framework import permissions


class ActionBasedPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if not hasattr(view, 'action_permissions'):
            return True

        action = view.action
        app_label = view.queryset.model._meta.app_label

        required_permission = view.action_permissions.get(action)

        if required_permission:
            if isinstance(required_permission, list):
                required_permission = required_permission[0]

            permission_codename = f"{app_label}.{required_permission}"

            if not request.user.user_permissions.filter(codename=permission_codename).exists():
                return False

        return True
>>>>>>> origin/ma-branch
