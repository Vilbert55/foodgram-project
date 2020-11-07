from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAdminUser


class IsOwnerOrAdmin(permissions.IsAuthenticatedOrReadOnly):
    
    def has_permission(self, request, view, obj):
        return request.user.is_superuser or (obj.author == request.user)

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or (obj.author == request.user)