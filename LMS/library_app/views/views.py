from django.forms import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from decimal import Decimal

from library_app.repository import BorrowedBookRepository, MemberRepository, BookRepository
from library_app.models import Author, Book, Member
from library_app.serializers import AuthorSerializer, BookSerializer, MemberSerializer, BorrowedBookSerializer, BorrowedBookCreateSerializer

# get post put delete authors, books, members
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class MemberViewSet(viewsets.ModelViewSet):
    queryset = MemberRepository.get_all_members()
    serializer_class = MemberSerializer

class BorrowedBookViewSet(viewsets.ModelViewSet):
    queryset = BorrowedBookRepository.get_all_borrowed()
    serializer_class = BorrowedBookSerializer
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == 'create':
            return BorrowedBookCreateSerializer
        return BorrowedBookSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        book = serializer.validated_data.get('book')
        member = serializer.validated_data.get('member')
        borrow_period_days = serializer.validated_data.get('borrow_period_days', 14)
        
        # transation needed here 
        if BookRepository.is_available(book.id) is False:
            raise ValidationError({'book': 'No available copies for this book.'})

        BookRepository.increase_borrowed_copies(book)

        borrowed_book = BorrowedBookRepository.create_borrow(book, member, borrow_period_days)
        
        read_serializer = BorrowedBookSerializer(borrowed_book)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        raise ValidationError("Updating a borrowed book is not allowed.")

    def partial_update(self, request, *args, **kwargs):
        raise ValidationError("Updating a borrowed book is not allowed.")
    


    
   
