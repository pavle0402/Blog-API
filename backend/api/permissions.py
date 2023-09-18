from rest_framework import permissions
from django.utils import timezone


class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or (request.user and request.user.is_staff)
    


class IsRegularMemberOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user.is_authenticated:
            if user.is_staff:
                return True
        delta = timezone.now() - user.date_joined
        if delta.days >= 30:
            return True
        return False