from django.db.models import Q, Count
from ..models import Book
from django.db.models import F


class BookRepository:
    @staticmethod
    def get_all():
        return Book.objects.select_related('author').all()

    @staticmethod
    def get_by_id(book_id):
        return Book.objects.select_related('author').get(id=book_id)

    @staticmethod
    def create(data):
        return Book.objects.create(**data)

    @staticmethod
    def get_book_for_update(book_id):
        return Book.objects.select_for_update().select_related('author').get(id=book_id)
    
    @staticmethod
    def update(book, data):
        for key, value in data.items():
            setattr(book, key, value)
        book.save()
        return book
    
    @staticmethod
    def is_available(book):
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