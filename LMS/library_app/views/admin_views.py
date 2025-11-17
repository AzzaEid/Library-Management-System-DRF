from rest_framework import viewsets, status
from rest_framework.decorators import action
from ..permissions import IsStaff
from rest_framework.response import Response
from ..schemas import AuthorSchema, BookSchema, MemberBookCreateSchema, MemberBookSchema, MemberSchema
from ..components import BorrowManagement, MemberManagement,  BookManagement, AuthorManagement
from ..validator import SchemaValidator
from marshmallow import ValidationError


class AdminAuthorsController(viewsets.ViewSet):
    permission_classes = [IsStaff]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.author_component = AuthorManagement()
        self.validator = SchemaValidator()
    
    def list(self, request):
        authors = self.author_component.get_all_authors()
        return Response(self.validator.dump(AuthorSchema, authors, many=True))
    
    def retrieve(self, request, pk=None):
        author = self.author_component.get_author_by_id(pk)
        if not author:
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.validator.dump(AuthorSchema, author))
    
    def create(self, request):
        try:
            data = self.validator.validate(AuthorSchema, request.data)
            author = self.author_component.create_author(data)
            return Response(self.validator.dump(AuthorSchema, author), status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        try:
            partial = request.method == 'PATCH'
            data = self.validator.validate(AuthorSchema, request.data, partial=partial)
            author = self.author_component.update_author(pk, data)
            if not author:
                return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response(self.validator.dump(AuthorSchema, author))
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
    
    # def partial_update(self, request, pk=None):
    #     return self.update(request, pk=pk)

    def delete(self, request, pk=None):
        success = self.author_component.delete_author(pk)
        if not success:
            return Response({'error': 'Author not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class AdminBooksController(viewsets.ViewSet):
    permission_classes = [IsStaff]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
    
    def create(self, request):
        try:
            data = self.validator.validate(BookSchema, request.data)
            book = self.book_component.create_book(data)
            return Response(self.validator.dump(BookSchema, book), status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        try:
            partial = request.method == 'PATCH'
            data = self.validator.validate(BookSchema, request.data, partial=partial)
            book = self.book_component.update_book(pk, data)
            if not book:
                return Response({'error': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response(self.validator.dump(BookSchema, book))
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        success, error = self.book_component.delete_book(pk)
        if not success:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class AdminMembersController(viewsets.ViewSet):
    # permission_classes = [IsStaff]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.member_component = MemberManagement()
        self.validator = SchemaValidator()


    def list(self, request):
        filters = {
            'username': request.query_params.get('username'),
            'phone_number': request.query_params.get('phone_number')
        }
        members = self.member_component.get_all_members(filters)
        return Response(self.validator.dump(MemberSchema, members, many=True))
    
    def retrieve(self, request, pk=None):
        member = self.member_component.get_member_by_id(pk)
        if not member:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.validator.dump(MemberSchema, member))
    
    def create(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            phone_number = request.data.get('phone_number', '')
            is_staff = request.data.get('is_staff', False)
            
            member = self.member_component.create_member(username, password, phone_number, is_staff)
            return Response(self.validator.dump(MemberSchema, member), status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk=None):
        try:
            partial = request.method == 'PATCH'
            data = self.validator.validate(MemberSchema, request.data, partial=partial)
            member = self.member_component.update_member(pk, data)
            if not member:
                return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response(self.validator.dump(MemberSchema, member))
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        success = self.member_component.delete_member(pk)
        if not success:
            return Response({'error': 'Member not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, methods=['GET'], url_path='borrowed-books')
    def member_borrowed_books(self, request, pk=None):
        borrowed_books, total_late_fees = self.member_component.get_member_borrowed_books(pk)
        return Response({
            'borrowed_books': self.validator.dump(MemberBookSchema, borrowed_books, many=True),
            'total_late_fees': total_late_fees
        })

class AdminBorrowedBooksController(viewsets.ViewSet):
    # permission_classes = [IsStaff]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.borrow_component = BorrowManagement()
        self.validator = SchemaValidator()

    def list(self, request):
        filters = {
            'member_username': request.query_params.get('member_username')
        }
        order_by = request.query_params.get('order_by', 'borrowed_date')
        
        member_books = self.borrow_component.get_all_borrowed_books(filters, order_by)
        return Response(self.validator.dump(MemberBookSchema, member_books, many=True))
    
    def retrieve(self, request, pk=None):
        member_book = self.borrow_component.get_borrow_by_id(pk)
        if not member_book:
            return Response({'error': 'MemberBook not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.validator.dump(MemberBookSchema, member_book))
    
    def create(self, request):
        try:
            validated = self.validator.validate(MemberBookCreateSchema, request.data)
            book_id = validated['book_id']
            member_id = validated['member_id']
            period = validated.get('borrow_period_days', 14)
            
            member_book, error = self.borrow_component.borrow_book(book_id, member_id, period)
            if error:
                return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response(self.validator.dump(MemberBookSchema, member_book), status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': e.messages}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['POST'], url_path='return')
    def return_book(self, request, pk=None):
        member_book, error = self.borrow_component.return_book(pk)
        if error:
            return Response({'error': error}, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.validator.dump(MemberBookSchema, member_book))
    
    @action(detail=False, methods=['GET'], url_path='overdue')
    def overdue_books(self, request):
        overdue = self.borrow_component.get_overdue_books()
        return Response(self.validator.dump(MemberBookSchema, overdue, many=True))
    
    @action(detail=False, methods=['GET'], url_path='not-returned')
    def not_returned_books(self, request):
        not_returned = self.borrow_component.get_not_returned_books()
        return Response(self.validator.dump(MemberBookSchema, not_returned, many=True))