from time import timezone
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

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated], url_path='borrowed-books')
    def get_borrowed_books(self, request, pk=None):
        user = request.user
        if user.is_staff:
            member = MemberRepository.get_member_by_id(pk)
            if member is None:
                return Response({'detail': 'Member not found.'}, status=status.HTTP_404_NOT_FOUND)
        elif user.member.id == pk:
            member = user.member
        else:
            return Response({'detail': 'Not authorized to view this member\'s borrowed books.'}, status=status.HTTP_403_FORBIDDEN)
        
        borrowed_books = BorrowedBookRepository.get_borrowed_by_member(member)
        serializer = BorrowedBookSerializer(borrowed_books, many=True)

        total_late_fees = sum([borrowed_book.late_fee for borrowed_book in borrowed_books if borrowed_book.late_fee])
        return Response({'borrowed_books': serializer.data, 'total_late_fees': total_late_fees}, status=status.HTTP_200_OK)


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
    
class ReturnBookView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        borrowed_book = BorrowedBookRepository.get_borrowed_book(pk)

        if borrowed_book.is_returned:
            raise ValidationError("This book has already been returned.")

        borrowed_book = BorrowedBookRepository.return_book(borrowed_book)

        BookRepository.decrease_borrowed_copies(borrowed_book.book)

        serializer = BorrowedBookSerializer(borrowed_book)
        return Response(serializer.data, status=status.HTTP_200_OK)
