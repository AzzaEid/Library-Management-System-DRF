from ..components import BookManagement, AuthorManagement 
from ..serializers import BookSerializer, AuthorSerializer, MemberSerializer
from ..components import MemberManagement
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from schemas import  AuthorSchema, BookSchema
from rest_framework.decorators import action
from validator import SchemaValidator
from marshmallow import ValidationError

class PublicBookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BookManagement.get_all_books()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    page_size = 10 
    page_size_query_param = 'page_size'  
    max_page_size = 100



class PublicAuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuthorManagement.get_all_authors()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]
    page_size = 10 
    page_size_query_param = 'page_size'  
    max_page_size = 100

class PublicMemberRegisterView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = MemberSerializer
    permission_classes = [AllowAny] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        member = MemberManagement.create_member(
            username=serializer.validated_data['username'],
        password=serializer.validated_data['password'],
        phone_number=serializer.validated_data['phone_number']
        )

        if not member:
            return Response(
                {"detail": "Failed to create member"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            MemberSerializer(member).data,
            status=status.HTTP_201_CREATED
        )


class PublicController(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.author_component = AuthorManagement()
        self.book_component = BookManagement()
        self.validator = SchemaValidator()
    
    @action(detail=False, methods=['GET'], url_path='authors')
    def list_authors(self, request):
        authors = self.author_component.get_all_authors()
        return Response(self.validator.dump(AuthorSchema, authors, many=True))
    
    @action(detail=True, methods=['GET'], url_path='authors')
    def retrieve_author(self, request, pk=None):
        author = self.author_component.get_author_by_id(pk)
        if not author:
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.validator.dump(AuthorSchema, author))
    
    @action(detail=False, methods=['GET'], url_path='books')
    def list_books(self, request):
        books = self.book_component.get_all_books()
        return Response(self.validator.dump(BookSchema, books, many=True))
    
    @action(detail=True, methods=['GET'], url_path='books')
    def retrieve_book(self, request, pk=None):
        book = self.book_component.get_book_by_id(pk)
        if not book:
            return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.validator.dump(BookSchema, book))
