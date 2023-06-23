from rest_framework import permissions


class ActionBasedPermission(permissions.BasePermission):

    def has_permission(self, request, view):

        if not hasattr(view, 'action_permissions'):
            return True

        action = view.action
        app_label = view.queryset.model._meta.app_label
        model_name = view.queryset.model._meta.model_name

        required_permission = view.action_permissions.get(action)

        if required_permission:
            # Permission string format: "app_label.permission_codename_model_name"
            permission_codename = f"{app_label}.{required_permission}_{model_name}"
            return request.user.has_perm(permission_codename)
        return True
