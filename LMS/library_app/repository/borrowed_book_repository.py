from django.db.models import Q, F
from django.utils import timezone
from datetime import timedelta
from ..models import BorrowedBook


class BorrowedBookRepository:
    
    @staticmethod
    def get_all_borrowed_books():
        return BorrowedBook.objects.select_related(
            'book__author', 'member__user'
        ).all()
    
    @staticmethod
    def get_borrowed_book_by_id(borrowed_id):
        return BorrowedBook.objects.select_related(
            'book__author', 'member__user'
        ).get(id=borrowed_id)
    
    @staticmethod
    def get_active_borrowed_books():
        return BorrowedBook.objects.filter(
            is_returned=False
        ).select_related('book__author', 'member__user')
    
    @staticmethod
    def get_borrowed_books_by_member(member_id):
        return BorrowedBook.objects.filter(
            member_id=member_id
        ).select_related('book__author')
    
    @staticmethod
    def get_active_borrowed_books_by_member(member_id):
        return BorrowedBook.objects.filter(
            member_id=member_id,
            is_returned=False
        ).select_related('book__author')
    
    @staticmethod
    def get_overdue_books():
        today = timezone.now().date()
        return BorrowedBook.objects.filter(
            is_returned=False,
            due_date__lte=today
        ).select_related('book__author', 'member__user')
    
    @staticmethod
    def get_overdue_books_by_member(member_id):
        today = timezone.now().date()
        return BorrowedBook.objects.filter(
            member_id=member_id,
            is_returned=False,
            due_date__lt=today
        )
    
    @staticmethod
    def create_borrowed_book(book, member, borrow_period_days):
        borrowed_date = timezone.now()
        due_date = (borrowed_date + timedelta(days=borrow_period_days)).date()
        
        return BorrowedBook.objects.create(
            book=book,
            member=member,
            borrow_period_days=borrow_period_days,
            due_date=due_date
        )
    
    @staticmethod
    def mark_as_returned(borrowed_book, late_fee=0):
        borrowed_book.is_returned = True
        borrowed_book.returned_date = timezone.now()
        borrowed_book.late_fee = late_fee
        borrowed_book.save()
        return borrowed_book
    
    @staticmethod
    def update_late_fee(borrowed_book, late_fee):
        borrowed_book.late_fee = late_fee
        borrowed_book.save()
        return borrowed_book
    
    @staticmethod
    def mark_as_overdue(borrowed_book):
        borrowed_book.is_overdue = True
        borrowed_book.save()
        return borrowed_book
    
    @staticmethod
    def get_borrowed_books_by_username(username):
        return BorrowedBook.objects.filter(
            member__user__username=username
        ).select_related('book__author', 'member__user')
    
    @staticmethod
    def get_borrowed_books_ordered(order_by='borrowed_date'):
        return BorrowedBook.objects.select_related(
            'book__author', 'member__user'
        ).order_by(order_by)

    @staticmethod
    def return_all_books():
        active_books = BorrowedBook.objects.filter(is_returned=False)
        now = timezone.now()
        
        updated_count = active_books.update(
            is_returned=True,
            returned_date=now
        )
        
        return updated_count, active_books
