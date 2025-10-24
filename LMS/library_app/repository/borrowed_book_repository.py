from django.conf import settings
from django.db.models import Q, F
from django.utils import timezone
from datetime import timedelta
from ..models import BorrowedBook
from django.db.models import F


class BorrowedBookRepository:
    @staticmethod
    def get_all_borrowed():
        return BorrowedBook.objects.select_related('book__author', 'member__user').all()
    
    @staticmethod
    def create_borrow(book, member, period_days):
        borrowed_book = BorrowedBook.objects.create(
            book=book,
            member=member,
            due_date=timezone.now().date() + timedelta(days=period_days),
            borrowed_date=timezone.now().date()
        )
        return borrowed_book
    
    @staticmethod
    def get_by_id(borrowed_id):
        return BorrowedBook.objects.select_related('book__author', 'member__user').get(id=borrowed_id)
    
    @staticmethod
    def return_book(borrowed_book):
        return_date = timezone.now().date()
        borrowed_book.returned_date = return_date

        if return_date > borrowed_book.due_date:
            days_late = (return_date - borrowed_book.due_date).days
            daily_fee = settings.LIBRARY_SETTINGS['DAILY_LATE_FEE']
            borrowed_book.late_fee = days_late * daily_fee

        borrowed_book.save()
        return borrowed_book
    
    @staticmethod
    def get_overdue():
        today = timezone.now().date()
        return BorrowedBook.objects.filter(
            returned_date__isnull=True,  
            due_date__lt=today
        ).select_related('book__author', 'member__user')
    
    @staticmethod
    def get_not_returned():
        return BorrowedBook.objects.filter(returned_date__isnull=True).select_related('book__author', 'member__user')

    @staticmethod
    def get_with_filters(member_id, order_by='borrowed_date'):
        all = BorrowedBook.objects.select_related('member__user').filter(member_id=member_id)
        return all.order_by(order_by)
    
    @staticmethod
    def get_borrowed_by_member(member):
        return BorrowedBook.objects.select_related('book__author', 'member__user').filter(member_id=member.id)