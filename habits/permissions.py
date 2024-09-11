from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsPublic(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.is_public
