from rest_framework import serializers
from ..models.django_orm.author import Author
from ..models.django_orm.book import Book

class BookSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField() # <== just the author's name

    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True
    )  
    borrowed_copies = serializers.IntegerField(read_only=True)
    available_copies = serializers.IntegerField(read_only=True)
        
    class Meta:
        model = Book
        fields = ['id', 'title', 'author_id', 'author', 'isbn', 'total_copies', 'borrowed_copies', 'available_copies']