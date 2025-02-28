from rest_framework.permissions import BasePermission
from .models import Admin

class IsNotAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return False
        return True


