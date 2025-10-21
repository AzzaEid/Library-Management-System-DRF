from django.conf import settings
from rest_framework import serializers
from library_app.repository.borrowed_book_repository import BorrowedBookRepository
from library_app.models import Book, Member
from library_app.models import BorrowedBook
from library_app.serializers import BookSerializer, MemberSerializer

class BorrowedBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    member = MemberSerializer(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    is_returned = serializers.BooleanField(read_only=True)
    days_overdue = serializers.IntegerField(read_only=True)

    class Meta:
        model = BorrowedBook
        fields = ['id', 'book', 'member', 'borrowed_date', 'due_date', 'returned_date', 'is_returned', 'late_fee', 'is_overdue', 'days_overdue']

class BorrowedBookCreateSerializer(serializers.ModelSerializer):
    
    borrow_period_days = serializers.IntegerField(
        write_only=True, 
        default=14,
        min_value=1,  
        max_value=settings.LIBRARY_SETTINGS['MAX_BORROW_PERIOD'] 
    )
    class Meta:
        model = BorrowedBook
        fields = ['book', 'member', 'borrow_period_days']

    