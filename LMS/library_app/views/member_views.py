from rest_framework import viewsets, mixins, status
from ..permissions import  IsAuthorized
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response

from ..schemas import MemberBookSchema

from ..components import BorrowManagement, MemberManagement
from ..serializers import BorrowedBookSerializer, MemberSerializer
from ..validator import SchemaValidator
from marshmallow import ValidationError


class MemberBooksController(viewsets.ViewSet):
    permission_classes = [IsAuthorized]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.member_component = MemberManagement()
        self.borrow_component = BorrowManagement()
        self.validator = SchemaValidator()
    
    @action(detail=False, methods=['GET'], url_path='active')
    def active(self, request):
        member = request.user
        borrowed_books, total_late_fees = self.member_component.get_member_borrowed_books(member.id)
        return Response({
            'borrowed_books': self.validator.dump(MemberBookSchema, borrowed_books, many=True),
            'total_late_fees': total_late_fees
        })
    
    def list(self, request):
        member = request.user
        member_books, error = self.borrow_component.get_member_borrowed_books(member.id)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(self.validator.dump(MemberBookSchema, member_books, many=True))
    
