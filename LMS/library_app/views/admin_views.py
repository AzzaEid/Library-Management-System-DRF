from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db import transaction
from ..components import BorrowManagement, MemberManagement,  BookManagement, AuthorManagement
from ..serializers import (
    BorrowedBookSerializer,
    MemberSerializer,
    BookSerializer,
    AuthorSerializer
)

from ..filters import BorrowedBookFilter

class AdminBorrowedBookViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = BorrowedBookSerializer
    queryset = BorrowManagement.get_all_borrowed_books()
    filterset_class = BorrowedBookFilter
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['borrowed_date', 'due_date']

    def get_serializer(self, *args, **kwargs):
        if self.action == 'create':
            kwargs['fields'] = ['book_id', 'member_id', 'borrow_period_days']
        elif self.action in ['update', 'partial_update']:
            kwargs['fields'] = ['due_date', 'late_fee']
        else :
            kwargs['fields'] = [
                'id', 'book', 'member', 'borrowed_date',
                'due_date', 'returned_date', 'is_returned', 'late_fee'
            ]
        return super().get_serializer(*args, **kwargs)
    
    def get_queryset(self): # <= for nested route 
        member_id = self.kwargs.get('member_pk')
        qs =  BorrowManagement.get_all_borrowed_books()
        if member_id:
            qs = qs.filter(member_id=member_id)
        return qs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        book_id = serializer.validated_data['book_id']
        member_id = serializer.validated_data['member_id']
        borrow_period_days = serializer.validated_data.get('borrow_period_days')
        
        borrowed_book, error = BorrowManagement.borrow_book(
            book_id=book_id,
            member_id=member_id,
            borrow_period_days=borrow_period_days
        )
        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)
        output_serializer = self.get_serializer(borrowed_book)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, pk=None):
        borrowed_book, error= BorrowManagement.return_book(pk)
        if error:
            return Response(error, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(borrowed_book)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def overdue(self, request):
        overdue_books = BorrowManagement.get_overdue_books()
        serializer = self.get_serializer(overdue_books, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def not_returned(self, request):
        not_returned = BorrowManagement.get_not_returned_books()
        serializer = self.get_serializer(not_returned, many=True)
        return Response(serializer.data)
    
class AdminMemberViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MemberManagement.get_all_members()
    serializer_class = MemberSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        member = MemberManagement.create_member(serializer.validated_data)

        if not member:
            return Response(
                {"detail": "Failed to create member"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            MemberSerializer(member).data,
            status=status.HTTP_201_CREATED
        )
    
class AdminBookViewSet(viewsets.ModelViewSet):
    queryset = BookManagement.get_all_books()
    serializer_class = BookSerializer
    permission_classes = [IsAdminUser]

class AdminAuthorViewSet(viewsets.ModelViewSet):
    queryset = AuthorManagement.get_all_authors()
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminUser]

    

    