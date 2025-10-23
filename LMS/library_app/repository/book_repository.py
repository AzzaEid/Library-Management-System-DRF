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
    def get_book_for_update(book_id):
        return Book.objects.select_for_update().select_related('author').get(id=book_id)
    
    @staticmethod
    def is_available(book_id):
        book = Book.objects.get(id=book_id)
        return book.available_copies > 0
    @staticmethod
    def increase_borrowed_copies(book):
        Book.objects.filter(pk=book.pk).update(
            borrowed_copies=F('borrowed_copies') + 1
        )

    @staticmethod
    def decrease_borrowed_copies(book):
        Book.objects.filter(pk=book.pk).update(
            borrowed_copies=F('borrowed_copies') - 1
        )