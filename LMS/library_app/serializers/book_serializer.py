from rest_framework import serializers
from LMS.library_app.models.book import Book
from LMS.library_app.models.borrowedBook import BorrowedBook

class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'isbn', 'available_copies', 'total_copies']