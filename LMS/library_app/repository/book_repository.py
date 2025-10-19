from django.db.models import Q, Count
from ..models import Book


class BookRepository:

    @staticmethod
    def get_all_books():
        return Book.objects.select_related('author').all()
    
    @staticmethod
    def get_book_by_id(book_id):
        return Book.objects.select_related('author').get(id=book_id)
    
    @staticmethod
    def get_books_by_author(author_id):
        return Book.objects.filter(author_id=author_id)
    
    @staticmethod
    def get_available_books():
        return Book.objects.filter(available_copies__gt=0).select_related('author')
    
    @staticmethod
    def search_books(query):
            return Book.objects.filter(
            Q(title__icontains=query) | Q(isbn__icontains=query)
        ).select_related('author')
    
    @staticmethod
    def create_book(data):
        return Book.objects.create(**data)
    
    @staticmethod
    def update_book(book, data):
        for key, value in data.items():
            setattr(book, key, value)
        book.save()
        return book
    
    @staticmethod
    def delete_book(book):
        book.delete()
    
    @staticmethod
    def decrease_available_copies(book):
        book.available_copies -= 1
        book.save()
        return book
    
    @staticmethod
    def increase_available_copies(book):
        book.available_copies += 1
        book.save()
        return book
    