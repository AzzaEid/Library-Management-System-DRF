from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from ..components import BorrowManagement, MemberManagement
from ..serializers import BorrowedBookSerializer, MemberSerializer
from ..models import Member

class MemberBorrowedBookViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BorrowedBookSerializer
    
    def get_queryset(self):
        try:
            member = self.request.user.member
        except Member.DoesNotExist:
            raise PermissionDenied("You must be a registered member")

        return BorrowManagement.get_member_borrowed_books(member)

    def get_serializer(self, *args, **kwargs):
        kwargs['fields'] = [
                    'id', 'book', 'borrowed_date',
                    'due_date', 'returned_date', 'is_overdue', 'late_fee'
                ]
        return super().get_serializer(*args, **kwargs)
    
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        try:
            member = request.user.member
        except Member.DoesNotExist:
            raise PermissionDenied("You must be a registered member")
        
        borrowed_books = BorrowManagement.get_member_borrowed_books(
            member, 
            include_returned=False
        )

        serializer = self.get_serializer(borrowed_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class MemberProfileViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           viewsets.GenericViewSet):
    
    serializer_class = MemberSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return self.request.user.member
        except Member.DoesNotExist:
            raise PermissionDenied("You must be a registered member")

    def update(self, request, *args, **kwargs):
        member = self.get_object()
        serializer = self.get_serializer(member, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updated_member = MemberManagement.update_member(member.id, serializer.validated_data)
        if not updated_member:
            return Response({"detail": "Failed to update profile"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(MemberSerializer(updated_member).data, status=status.HTTP_200_OK)