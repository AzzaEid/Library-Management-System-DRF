from django.db.models import Q, Count
from ..models.sqlalchemy_models import Book
from django.db.models import F
from sqlalchemy import select, update
from sqlalchemy.orm import joinedload
from ..context.database import Session


class BookRepository:
    @staticmethod
    def get_all():
        session = Session()
        stmt = select(Book).options(joinedload(Book.author))
        return session.scalars(stmt).unique().all()
    
    @staticmethod
    def get_by_id(book_id):
        session = Session()
        stmt = select(Book).options(joinedload(Book.author)).where(Book.id == book_id)
        return session.scalar(stmt)
    
    @staticmethod
    def is_available(book_id):
        session = Session()
        book = session.get(Book, book_id)
        return book and book.available_copies > 0


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
    def increase_borrowed_copies(book):
        Book.objects.filter(pk=book.pk).update(
            borrowed_copies=F('borrowed_copies') + 1
        )

    @staticmethod
    def decrease_borrowed_copies(book):
        Book.objects.filter(pk=book.pk).update(
            borrowed_copies=F('borrowed_copies') - 1
        )