# from ..models.django_orm.book import Book
from ..repository import BookRepository
from rest_framework.exceptions import ValidationError
from .author_management import AuthorManagement
class BookManagement:
    def __init__(self, **kwargs):
        self.book_repo = BookRepository()
        self.author_management = AuthorManagement()
        super().__init__(**kwargs)

    def get_all_books(self):
        return self.book_repo.get_all()
    
    def get_book_by_id(self, book_id):
        try:
            return self.book_repo.get_by_id(book_id=book_id)
        except:
            return ValidationError({'book' : "Doesn't exist"})
    
    def create_book(self, data):
        self.author_management.get_author_by_id(data.author_id)
        return self.book_repo.create(data)
    
    def update_book(self, book_id, data):
        book = self.book_repo.get_by_id(book_id=book_id)
        if not book:
            return None
        return self.book_repo.update(book, data)
    
    def delete_book(self, book_id):
        book = self.book_repo.get_by_id(book_id)
        if not book:
            return False, "Book not found"
        # Check if book has active borrows
        if book.borrowed_copies > 0:
            return False, "Cannot delete book with active borrows"
        book.delete()
        return True, None

