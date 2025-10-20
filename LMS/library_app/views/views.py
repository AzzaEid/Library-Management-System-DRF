from datetime import timezone
from django.forms import ValidationError
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.db import transaction
from rest_framework.exceptions import NotFound

from library_app.models.borrowedBook import BorrowedBook
from library_app.repository import BorrowedBookRepository, MemberRepository, BookRepository, AuthorRepository
from library_app.serializers import AuthorSerializer, BookSerializer, MemberSerializer, BorrowedBookSerializer, BorrowedBookCreateSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = AuthorRepository.get_all_authors()
    serializer_class = AuthorSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class BookViewSet(viewsets.ModelViewSet):
    queryset = BookRepository.get_all_books()
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

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated], url_path='me/borrowed-books')
    def get_member_borrowed_books(self, request):
        member = request.user.member
        
        borrowed_books = BorrowedBookRepository.get_borrowed_by_member(member)
        serializer = BorrowedBookSerializer(borrowed_books, many=True)

        total_late_fees = sum([borrowed_book.late_fee for borrowed_book in borrowed_books if borrowed_book.late_fee])
        return Response({'borrowed_books': serializer.data, 'total_late_fees': total_late_fees}, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'], permission_classes=[IsAdminUser], url_path='borrowed-books')
    def get_borrowed_books(self, request):
        username_filter = request.query_params.get('username', None)
        order_by = request.query_params.get('order_by', 'borrowed_date')

        borrowed_books = BorrowedBookRepository.get_with_filters(username=username_filter, order_by=order_by)
        serializer = BorrowedBookSerializer(borrowed_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


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

        book = BookRepository.get_book_by_id(serializer.validated_data.get('book').id)
        member = MemberRepository.get_member_by_id(serializer.validated_data.get('member').id)
        borrow_period_days = serializer.validated_data.get('borrow_period_days', 14)
        
        if BookRepository.is_available(book.id) is False:
            raise ValidationError({'book': 'No available copies for this book.'})


        with transaction.atomic():
            BookRepository.increase_borrowed_copies(book)
            borrowed_book = BorrowedBookRepository.create_borrow(book, member, borrow_period_days)
        
        read_serializer = BorrowedBookSerializer(borrowed_book)
        return Response(read_serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        raise ValidationError("Updating a borrowed book is not allowed.")

    def partial_update(self, request, *args, **kwargs):
        raise ValidationError("Updating a borrowed book is not allowed.")
    
    @action(detail=False, methods=['GET'], permission_classes=[IsAdminUser], url_path='overdue')
    def get_overdue_books(self, request):
        overdue_books = BorrowedBookRepository.get_overdue()
        serializer = BorrowedBookSerializer(overdue_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['GET'], permission_classes=[IsAdminUser], url_path='not-returned')
    def get_not_returned_books(self, request):
        not_returned_books = BorrowedBookRepository.get_not_returned()
        serializer = BorrowedBookSerializer(not_returned_books, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ReturnBookView(APIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [TokenAuthentication]

    def post(self, request, pk):       

        try:
            borrowed_book = BorrowedBookRepository.get_borrowed_book(pk)
        except BorrowedBook.DoesNotExist:
            raise NotFound("Borrowed book record not found.")
        
        if borrowed_book.is_returned:
            return Response({"massege": "This book has already been returned."}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            borrowed_book = BorrowedBookRepository.return_book(borrowed_book)
            BookRepository.decrease_borrowed_copies(borrowed_book.book)

        serializer = BorrowedBookSerializer(borrowed_book)
        return Response(serializer.data, status=status.HTTP_200_OK)
