from ..models.book import Book
from ..repository import BookRepository

class BookManagement:

    @staticmethod
    def get_all_books():
        return BookRepository.get_all()
    
    @staticmethod
    def get_book_by_id(book_id):
        try:
            return BookRepository.get_by_id(book_id=book_id)
        except Book.DoesNotExist:
            return None
    
    @staticmethod
    def create_book(data):
        return BookRepository.create(**data)
    
    @staticmethod
    def update_book(book_id, data):
        book = BookManagement.get_book_by_id(book_id=book_id)
        if not book:
            return None
        return BookRepository.update(book, data)
    
    @staticmethod
    def delete_book(book_id):
        book = BookManagement.get_book_by_id(book_id)
        if not book:
            return False, "Book not found"
        # Check if book has active borrows
        if book.borrowed_copies > 0:
            return False, "Cannot delete book with active borrows"
        book.delete()
        return True, None

