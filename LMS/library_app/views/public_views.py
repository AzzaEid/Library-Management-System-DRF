from ..components import BookManagement, AuthorManagement 
from ..serializers import BookSerializer, AuthorSerializer, MemberSerializer
from ..components import MemberManagement
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from ..schemas import  AuthorSchema, BookSchema
from ..validator import SchemaValidator
from marshmallow import ValidationError


class PublicAuthorController(viewsets.ReadOnlyModelViewSet):
    permission_classes = [AllowAny]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.author_component = AuthorManagement()
        self.book_component = BookManagement()
        self.validator = SchemaValidator()
    
    def list(self, request):
        authors = self.author_component.get_all_authors()
        return Response(self.validator.dump(AuthorSchema, authors, many=True))
    
    def retrieve(self, request, pk=None):
        author = self.author_component.get_author_by_id(pk)
        if not author:
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.validator.dump(AuthorSchema, author))
    

class PublicBookController(viewsets.ReadOnlyModelViewSet):
    #permission_classes = [AllowAny]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.author_component = AuthorManagement()
        self.book_component = BookManagement()
        self.validator = SchemaValidator()
    
    def list(self, request):
        books = self.book_component.get_all_books()
        return Response(self.validator.dump(BookSchema, books, many=True))
    
    def retrieve(self, request, pk=None):
        book = self.book_component.get_book_by_id(pk)
        if not book:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.validator.dump(BookSchema, book))
