from django.db.models import Q, Count
from ..models import Book
from django.db.models import F


class BookRepository:
    @staticmethod
    def get_all_books():
        return Book.objects.select_related('author').all()

    @staticmethod
    def get_book_by_id(book_id):
        return Book.objects.select_related('author').get(id=book_id)

    @staticmethod
    def is_available(book_id):
        return Book.objects.filter(id=book_id, borrowed_copies__lt=F('total_copies')).exists()

    @staticmethod
    def decrease_borrowed_copies(book):
        book.borrowed_copies -= 1
        book.save()
        return book
    
    @staticmethod
    def increase_borrowed_copies(book):
        book.borrowed_copies += 1
        book.save()
        return book
    