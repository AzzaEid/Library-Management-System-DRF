from rest_framework import serializers
from LMS.library_app.models.borrowedBook import BorrowedBook
from LMS.library_app.serializers.book_serializer import BookSerializer
from LMS.library_app.serializers.member_serializer import MemberSerializer

class BorrowedBookSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    member = MemberSerializer(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    is_returned = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = BorrowedBook
        fields = ['id', 'book', 'member', 'borrowed_date', 'due_date', 'returned_date', 'is_returned', 'late_fee', 'is_overdue']

class BorrowedBookCreateSerializer(serializers.ModelSerializer):
    book_id = serializers.IntegerField()
    member_id = serializers.IntegerField()
    borrow_period_days = serializers.IntegerField(default=14)