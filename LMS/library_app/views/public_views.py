from ..components import BookManagement, AuthorManagement 
from ..serializers import BookSerializer, AuthorSerializer, MemberSerializer
from ..components import MemberManagement
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class PublicBookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BookManagement.get_all_books()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]


class PublicAuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuthorManagement.get_all_authors()
    serializer_class = AuthorSerializer
    permission_classes = [AllowAny]

class PublicMemberRegisterView(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = MemberSerializer
    permission_classes = [AllowAny] 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        member = MemberManagement.create_member(serializer.validated_data)

        if not member:
            return Response(
                {"detail": "Failed to create member"},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            MemberSerializer(member).data,
            status=status.HTTP_201_CREATED
        )
