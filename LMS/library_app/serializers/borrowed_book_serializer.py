from django.conf import settings
from rest_framework import serializers
from .dynamic_fields_model_serializer import DynamicFieldsModelSerializer
from ..models import BorrowedBook
from .book_serializer import BookSerializer
from .member_serializer import MemberSerializer

class BorrowedBookSerializer(DynamicFieldsModelSerializer):
    book = BookSerializer(read_only=True)
    member = MemberSerializer(read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    is_returned = serializers.BooleanField(read_only=True)
    days_overdue = serializers.IntegerField(read_only=True)
    book_id = serializers.IntegerField()
    borrow_period_days = serializers.IntegerField(
        write_only=True, 
        default=14,
        min_value=1,  
        max_value=settings.LIBRARY_SETTINGS['MAX_BORROW_PERIOD'] 
    )
    class Meta:
        model = BorrowedBook
        fields = '__all__'