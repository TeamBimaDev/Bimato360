from rest_framework import permissions


class ActionBasedPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if not hasattr(view, 'action_permissions'):
            return True

        action = view.action
        app_label = view.queryset.model._meta.app_label

        required_permission = view.action_permissions.get(action)

        if required_permission:
            # Ensure required_permission is a string, not a list
            if isinstance(required_permission, list):
                required_permission = required_permission[0]

            # Build the permission string
            permission_codename = f"{app_label}.{required_permission}"

            # Check if the user has the required permission
            if not request.user.user_permissions.filter(codename=permission_codename).exists():
                return False

        return True
