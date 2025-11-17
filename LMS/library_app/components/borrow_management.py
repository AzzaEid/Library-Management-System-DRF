from ..repository import BookRepository, MemberRepository, BorrowedBookRepository
# from ..models.django_orm import BorrowedBook
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .book_management import BookManagement
from .member_management import MemberManagement


class BorrowManagement:
    def __init__(self, **kwargs):
        self.book_repo = BookRepository()
        self.member_repo = MemberRepository()
        self.borrowed_book_repo = BorrowedBookRepository()
        self.member_management=MemberManagement()
        super().__init__(**kwargs)

    def get_all_borrowed_books(self, filters=None, order_by='borrowed_date'):
        return self.borrowed_book_repo.get_all(filters, order_by)
    
    def get_borrow_by_id(self, borrow_id):
        try:
            return self.borrowed_book_repo.get_by_id(borrow_id)
        except Exception:
            return None
    
    def borrow_book(self, book_id, member_id, borrow_period_days=14):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            return None, "Book not found"
        
        member = self.member_repo.get_by_id(member_id)
        if not member:
            return None, "Member not found"
        
        if not self.book_repo.is_available(book_id):
            return None, "No available copies for this book"
        
        member_book = self.borrowed_book_repo.create_borrow(book_id, member_id, borrow_period_days)
        return member_book, None

    
    def return_book(self, borrowed_id):
        borrowed_book = self.borrowed_book_repo.get_by_id(borrowed_id)
        
        if not borrowed_book:
            return None, "Borrowed book record not found"
        
        if borrowed_book.returned_date is not None:
            return None, "This book has already been returned"

        returned = self.borrowed_book_repo.return_book(borrowed_book.id)
        return returned, None

    def get_overdue_books(self):
        return self.borrowed_book_repo.get_overdue()
    
    def get_not_returned_books(self):
        return self.borrowed_book_repo.get_not_returned()
    
    def get_member_borrowed_books(self, member_id, include_returned=True):
        member = self.member_management.get_member_by_id(member_id)
        if not member:
            return None, "Member not found"
        return self.borrowed_book_repo.get_by_member(member_id, include_returned), None