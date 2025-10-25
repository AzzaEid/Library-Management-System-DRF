from ..repository import BorrowedBookRepository, BookRepository
from ..models import BorrowedBook
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .book_management import BookManagement
from .member_management import MemberManagement
class BorrowManagement:
    
    @staticmethod
    def get_all_borrowed_books():
        return BorrowedBookRepository.get_all_borrowed()
    
    @staticmethod 
    def get_borrow_by_id(borrow_id):
        try:
            return BorrowedBookRepository.get_by_id(borrow_id)
        except BorrowedBook.DoesNotExist:
            return None
    
    @staticmethod
    def borrow_book(book_id, member_id, borrow_period_days=14):
        book = BookManagement.get_book_by_id(book_id=book_id)
        if not book:
            return False, "Book not found"
        
        member = MemberManagement.get_member_by_id(member_id=member_id)
        if not member:
            return False, "Member not found"
        with transaction.atomic():
            # Lock the book row for update
            book = BookRepository.get_book_for_update(book_id)
            
            # Check availability
            if not BookRepository.is_available(book):
                return False, "No available copies for this book"
            
            # Increase borrowed copies
            BookRepository.increase_borrowed_copies(book)
            
            # Create borrow record
            borrowed_book = BorrowedBookRepository.create_borrow(
                book, member, borrow_period_days
            )
            
        return borrowed_book
    
    @staticmethod
    def return_book(borrowed_id):
        borrowed_book = BorrowManagement.get_borrow_by_id(borrowed_id)
        
        if not borrowed_book:
            return None, "Borrowed book record not found"
        
        if borrowed_book.is_returned:
            return None, "This book has already been returned"
        
        with transaction.atomic():
            # Process return and calculate late fee
            borrowed_book = BorrowedBookRepository.return_book(borrowed_book)
            
            # Decrease borrowed copies
            BookRepository.decrease_borrowed_copies(borrowed_book.book)
            
        return borrowed_book, None
    
    @staticmethod
    def get_overdue_books():
        return BorrowedBookRepository.get_overdue()
    
    @staticmethod
    def get_not_returned_books():
        return BorrowedBookRepository.get_not_returned()
    
    @staticmethod
    def get_member_borrowed_books(member, include_returned=True):

        member = MemberManagement.get_member_by_id(member_id=member.id)
        if not member:
            raise ValidationError({'member': 'member not found'})
        
        borrowed_books = BorrowedBookRepository.get_borrowed_by_member(member)
        if not include_returned:
            borrowed_books = borrowed_books.filter(returned_date__isnull=True)

        return borrowed_books