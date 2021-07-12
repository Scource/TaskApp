from rest_framework import permissions
from .models import *


class HasExpireLinkCreateAccess(permissions.BasePermission):
    message = 'Upgrade your plan to gain access to this site'

    def has_permission(self, request, view):
        return UserDetail.objects.get(user=request.user).plan.get_expiring_link


class HasExpireLinkAccess(permissions.BasePermission):
    message = 'User is not allowed to see this object'

    def has_permission(self, request, view):
        return ExpireLink.objects.get(
            pk=view.kwargs['pk']).files.user == request.user
