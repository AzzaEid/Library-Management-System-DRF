from rest_framework.permissions import BasePermission

class IsAuthorized(BasePermission):
    def has_permission(self, request, view):
        return request.user is not None
    
class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff
