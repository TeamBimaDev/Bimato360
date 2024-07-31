<<<<<<< HEAD
from rest_framework import permissions


class CanReadProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('erp.can_read_product')


class CanUpdateProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('erp.can_update_product')


class CanReadBankPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('erp.can_read_bank')


class CanCreateBankPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('erp.can_create_bank')
=======
from rest_framework import permissions


class CanReadProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('erp.can_read_product')


class CanUpdateProductPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('erp.can_update_product')


class CanReadBankPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('erp.can_read_bank')


class CanCreateBankPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('erp.can_create_bank')
>>>>>>> origin/ma-branch
