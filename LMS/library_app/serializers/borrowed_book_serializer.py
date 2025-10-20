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

    class Meta:
        model = BorrowedBook
        fields = ['id', 'book', 'member', 'borrowed_date', 'due_date', 'returned_date', 'is_returned', 'late_fee', 'is_overdue']

class BorrowedBookCreateSerializer(serializers.ModelSerializer):
    
    borrow_period_days = serializers.IntegerField(write_only=True, default=14)

    class Meta:
        model = BorrowedBook
        fields = ['book', 'member', 'borrow_period_days']

    # def create(self, validated_data):
    #     book = validated_data['book']
    #     member = validated_data['member']
    #     borrow_period_days = validated_data.get('borrow_period_days', 14)
        
    #     return BorrowedBookRepository.create_borrow(book, member, borrow_period_days)
