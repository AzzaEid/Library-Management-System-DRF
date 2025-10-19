from django.db.models import Q, F
from django.utils import timezone
from datetime import timedelta
from ..models import BorrowedBook


class BorrowedBookRepository:
    @staticmethod
    def create_borrow(book, member, period_days):
        return BorrowedBook.objects.create(
            book=book,
            member=member,
            borrow_period_days=period_days
        )
    
    @staticmethod
    def get_borrowed_book(borrowed_id):
        return BorrowedBook.objects.select_related('book__author', 'member__user').get(id=borrowed_id)
    
    @staticmethod
    def get_all_borrowed():
        return BorrowedBook.objects.select_related('book__author', 'member__user').all()
    
    @staticmethod
    def get_overdue():
        today = timezone.now().date()
        return BorrowedBook.objects.filter(
            is_returned=False,
            due_date__lt=today
        ).select_related('book__author', 'member__user')
    
    @staticmethod
    def count_active_borrows(member_id):
        return BorrowedBook.objects.filter(member_id=member_id, is_returned=False).count()
    
    @staticmethod
    def has_overdue(member_id):
        today = timezone.now().date()
        return BorrowedBook.objects.filter(
            member_id=member_id,
            is_returned=False,
            due_date__lt=today
        ).exists()
    
    @staticmethod
    def get_with_filters(username=None, order_by='borrowed_date'):
        qs = BorrowedBook.objects.select_related('book__author', 'member__user')
        if username:
            qs = qs.filter(member__user__username=username)
        return qs.order_by(order_by)