from ..components import BookManagement, AuthorManagement 
from ..serializers import BookSerializer, AuthorSerializer

from rest_framework import viewsets
from rest_framework.permissions import AllowAny

class PublicBookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BookManagement.get_all_books()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class PublicAuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuthorManagement.get_all_authors()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]