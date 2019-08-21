from rest_framework import permissions
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import BasePermission

SAFE_METHODS = ('HEAD', 'OPTIONS')


class IsOwnerOrAdmin(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.method in ('POST',"GET"):
            if not bool(request.user and request.user.is_authenticated):
                raise AuthenticationFailed('Unauthorized')
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == 'POST':
            if bool(request.user and request.user.is_authenticated or request.user.is_admin):
                raise AuthenticationFailed('Unauthorized')
        return obj.owner == request.user or request.user.is_admin
