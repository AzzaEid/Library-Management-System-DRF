from rest_framework.permissions import BasePermission

class IsAuthorized(BasePermission):
    def has_permission(self, request, view):
        return request.member is not None
    
class IsStaff(BasePermission):
    def has_permission(self, request, view):
        return request.member and request.member.is_staff
